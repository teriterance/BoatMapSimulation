
import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
from boat import Boat

import logging
logger = logging.getLogger(__name__)

#posgres sql for sounding point data management
import psycopg2 
from psycopg2 import Error

import pandas as pd

class BoatEnv(gym.Env, utils.EzPickle):
  metadata = {'render.modes': ['human']}

  def __init__(self, dbFilleName='default', dataDistant=False, lat=None, lon=None,cog=None, sog=None, ep_length=100, refDeepth=1):
    # This function will initialise the sounding point position list
    # These points will be used to compute the result of your algorithm
    if dataDistant == False:
      #We thing that the dataset have the good stucture
      self.pointDataFrame = pd.read_csv(dbFilleName+str('.csv'))
      self.pointDataFram.dropna(axis=0, inplace=True)
    else:
      try:
        # Connect to an existing database
        #change to your database credential
        self.connection = psycopg2.connect(user="postgres",
                                      password="pynative@#29",
                                      host="127.0.0.1",
                                      port="5432",
                                      database=dbFilleName)
        # Create a cursor to perform database operations
        self.cursor = self.connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(self.connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        self.cursor.execute("SELECT version();")
        # Fetch result
        record = self.cursor.fetchone()
        print("You are connected to - ", record, "\n")
      except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        exit()
    #dim
    self.boat = Boat()
    dim = 5 #dimenstion de l'espace de travail
    self.action_space = spaces.Discrete(dim)
    self.observation_space = self.action_space
    self.ep_length = ep_length
    self.dim = dim
    self.reset()

  def reset(self):
    """
    Reset function 
    """
    self.current_step = 0
    self._choose_next_state()
    return self.state

  def step(self, action):
    "step function"
    reward = self._get_reward(action)
    self._choose_next_state()
    self.current_step += 1
    done = self.current_step >= self.ep_length
    return self.state, reward, done, {}
  
  def _choose_next_state(self):
    self.state = self.action_space.sample()

  def status(self):

    pass

  def _get_reward(self):
    """ Reward is given for scoring a goal. """
    if self.status():
      return self.current_step/self.ep_length # the reward is proportional to the
      #duration  
    else:
      return 0

  def render(self, mode='human', close=False):
    """ Viewer only supports human mode currently. """
    if close:
      if self.viewer is not None:
        os.kill(self.viewer.pid, signal.SIGKILL)
    else:
      if self.viewer is None:
        self._start_viewer()

ACTION_LOOKUP = {
    0 : "PSIDE",#babord
    1 : "SBOARD",#tribod
    2 : "ACC",#acceleration
    3 : "BRAKE",#frein
  }