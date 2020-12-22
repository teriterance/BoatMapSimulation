
import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding

try:
    import gym_boat
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install HFO dependencies with 'pip3 install gym[boat].)'".format(e))

import logging
logger = logging.getLogger(__name__)

class BoatEnv(gym.Env, utils.EzPickle):
  metadata = {'render.modes': ['human']}

  def __init__(self, dbFilleName='default', lat=None, lon=None,cog=None, sog=None, refDeepth=1, ):
    # This function will initialise the sounding point position list
    # These points will be used to compute the result of your algorithm
    self.pointDataFrame = pd.read_csv(dbFilleName)
    
    # This list of point containt the point and it's list or deepth
    # We remove the point who are not enterely define 
    self.pointDataFram.dropna(axis=0, inplace=True)
    
    # Initialise the direction and position of our boat
    # We need to avoid that our Boat are near to the ground or near to a soundin point less 
    # Than it reference value
    self.viewer = None
    self.server_process = None
    self.server_port = None
    self.boat_path = gym_boat.get_boat_path()
    self._configure_environment()
    self.env = gym_boat.BOATEnvironment()
    self.env.connectToServer(config_dir=gym_boat.get_config_path())
    self.observation_space = spaces.Box(low=-1, high=1,
                                        shape=(self.env.getStateSize()))
    # Action space omits the Tackle/Catch actions, which are useful on defense
    self.action_space = spaces.Tuple((spaces.Discrete(3),
                                      spaces.Box(low=0, high=100, shape=1),
                                      spaces.Box(low=-180, high=180, shape=1),
                                      spaces.Box(low=-180, high=180, shape=1),
                                      spaces.Box(low=0, high=100, shape=1),
                                      spaces.Box(low=-180, high=180, shape=1)))
    self.status = gym_boat.IN_GAME
  
  def __del__(self):
    """
    To Quit env
    """
    self.env.act(gym_boat.QUIT)
    self.env.step()
    os.kill(self.server_process.pid, signal.SIGINT)
    if self.viewer is not None:
        os.kill(self.viewer.pid, signal.SIGKILL)

  def _configure_environment(self):
    """
    Provides a chance for subclasses to override this method and supply
    a different server configuration. By default, we initialize one
    offense agent against no defenders.
    """
    self._start_boat_server()

  def _start_boat_server(self, frames_per_trial=500,
                      untouched_time=100, offense_agents=1,
                      defense_agents=0, offense_npcs=0,
                      defense_npcs=0, sync_mode=True, port=6000,
                      offense_on_ball=0, fullstate=True, seed=-1,
                      ball_x_min=0.0, ball_x_max=0.2,
                      verbose=False, log_game=False,
                      log_dir="log"):
    """
    Starts the Half-Field-Offense server.
    frames_per_trial: Episodes end after this many steps.
    untouched_time: Episodes end if the ball is untouched for this many steps.
    offense_agents: Number of user-controlled offensive players.
    defense_agents: Number of user-controlled defenders.
    offense_npcs: Number of offensive bots.
    defense_npcs: Number of defense bots.
    sync_mode: Disabling sync mode runs server in real time (SLOW!).
    port: Port to start the server on.
    offense_on_ball: Player to give the ball to at beginning of episode.
    fullstate: Enable noise-free perception.
    seed: Seed the starting positions of the players and ball.
    ball_x_[min/max]: Initialize the ball this far downfield: [0,1]
    verbose: Verbose server messages.
    log_game: Enable game logging. Logs can be used for replay + visualization.
    log_dir: Directory to place game logs (*.rcg).
    """
    self.server_port = port
    cmd = self.boat_path + \
          " --headless --frames-per-trial %i --untouched-time %i --offense-agents %i"\
          " --defense-agents %i --offense-npcs %i --defense-npcs %i"\
          " --port %i --offense-on-ball %i --seed %i --ball-x-min %f"\
          " --ball-x-max %f --log-dir %s"\
          % (frames_per_trial, untouched_time, offense_agents,
              defense_agents, offense_npcs, defense_npcs, port,
              offense_on_ball, seed, ball_x_min, ball_x_max,
              log_dir)
    if not sync_mode: cmd += " --no-sync"
    if fullstate:     cmd += " --fullstate"
    if verbose:       cmd += " --verbose"
    if not log_game:  cmd += " --no-logging"
    print('Starting server with command: %s' % cmd)
    self.server_process = subprocess.Popen(cmd.split(' '), shell=False)
    time.sleep(10) # Wait for server to startup before connecting a player

  def _start_viewer(self):
    """
    Starts the SoccerWindow visualizer. Note the viewer may also be
    used with a *.rcg logfile to replay a game.
    """
    cmd = gym_boat.get_viewer_path() +\
          " --connect --port %d" % (self.server_port)
    self.viewer = subprocess.Popen(cmd.split(' '), shell=False)

  def _step(self, action):
    self._take_action(action)
    self.status = self.env.step()
    reward = self._get_reward()
    ob = self.env.getState()
    episode_over = self.status != gym_boat.IN_GAME
    return ob, reward, episode_over, {}

  def _take_action(self, action):
    """ Converts the action space into an HFO action. """
    action_type = ACTION_LOOKUP[action[0]]
    if action_type == gym_boat.DASH:
        self.env.act(action_type, action[1], action[2])
    elif action_type == gym_boat.TURN:
        self.env.act(action_type, action[3])
    elif action_type == gym_boat.KICK:
        self.env.act(action_type, action[4], action[5])
    else:
        print('Unrecognized action %d' % action_type)
        self.env.act(gym_boat.NOOP)

  def _get_reward(self):
    """ Reward is given for scoring a goal. """
    if self.status == gym_boat.GOAL:
        return 1
    else:
        return 0

  def _reset(self):
    """ Repeats NO-OP action until a new episode begins. """
    while self.status == gym_boat.IN_GAME:
      self.env.act(gym_boat.NOOP)
      self.status = self.env.step()
    while self.status != gym_boat.IN_GAME:
      self.env.act(gym_boat.NOOP)
      self.status = self.env.step()
    return self.env.getState()

  def _render(self, mode='human', close=False):
    """ Viewer only supports human mode currently. """
    if close:
      if self.viewer is not None:
        os.kill(self.viewer.pid, signal.SIGKILL)
    else:
      if self.viewer is None:
        self._start_viewer()

ACTION_LOOKUP = {
    0 : gym_boat.PSIDE,#babord
    1 : gym_boat.SBOARD,#tribod
    2 : gym_boat.ACC,#acceleration
    3 : gym_boat.brake,#freine 
  }