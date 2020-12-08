
import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding

try:
    import hfo_py
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install HFO dependencies with 'pip3 install gym[boat].)'".format(e))

import logging
logger = logging.getLogger(__name__)

class BoatEnv(gym.Env):
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
  
  def step(self, action):
    pass
  
  def reset(self):
    pass
  
  def render(self, mode='human'):
    pass
  
  def close(self):
    pass