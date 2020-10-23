import gym
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ReinforcementBoatRoadSelection(gym.Env):
  #metadata = {'render.modes': ['human']}

    def __init__(self, dbFilleName='default', lat=None, lon=None,cog=None, sog=None, refDeepth=1):
        # This function will initialise the sounding point position list
        # These points will be used to compute the result of your algorithm
        self.pointDataFrame = pd.read_csv(dbFilleName)
    
        # This list of point containt the point and it's list or deepth
        # We remove the point who are not enterely define 
        self.pointDataFram.dropna(axis=0, inplace=True)
    
        # Initialise the direction and position of our boat
        # We need to avoid that our Boat are near to the ground or near to a soundin point less 
        # Than it reference value
        if lat==None and lon==None and cog==None and sog==None:
            # The default values will be
            lat, lon, cog, sog = 1, 1, 1, 1
            # Sog Will be converted to rad nomalized form
        elif lat==None or lon==None or cog==None or sog==None:
            # The user have forgot to write one of the needed values
            return lat, lon, cog, sog, False
       
        # Assign vaalue to the self values
        self.lat, self.lon, self.cog, self.sog = lat, lon, cog, sog

        return lat, lon, cog, sog, refDeepth, True
    
    def projection(self, lat, long, squareSize):
        # This function project the value of lat, lon, cog and sog to the plane view
        
        return

    def step(self, action):
        pass
    
    def reset(self, dbFilleName='default', lat=None, lon=None,cog=None, sog=None, refDeepth=1):
       # Reinitialise the simulation data
       return self.__init__(dbFilleName, lat, lon, cog, sog, refDeepth)

    def render(self, mode='human', close=False):
        pass