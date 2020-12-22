import os, subprocess, time, signal
import numpy as np


class Boat:
    #Cette classe indique commment va se comporter un bateau, elle contient ses paramettres
    def __init__(self, lat = 47.719138, long =  -3.357664, speed = 30, cog = 180, boat_weight = 660):
        """
        Explication des paramettres:
        lat and long : latitude et longitude du point de depart du bateau, notre reference est prise dans la baie de la 
        ville de Lorient
        speed : La vitesse du bateau en Km/h
        cog: direction par rapport au nord magnetique
        boat_weight : masse du bateau
        """
        self.lat = lat
        self.long = long
        self.speed = speed
        self.cog = cog
        self.weight = boat_weight
        self.earth_radius = 6378 # en Km
        self.delta_cog = 0
    
    def step(self, delta_t, acceleration, cog_orientation):
        """
        Ici on calcul l'evolution du bateau dans le temps:
        delta_t: temps passe depuis la derniere valeur
        acceleration: acceleration de notre bateau, pour etre sur de la nouvelle vitesse
        cog_variation: variation du cap (une variation brusque du cap est inconcevable, les valeurs sont babord et tribord

        Example:
        self.step(0.1, -0.1, 'T')
        self.step(0.1, -0.1, 'B')
        """
        self.speed = self.speed + delta_t * acceleration # on cosidere une approximation sur le temps
        if cog_orientation ==  'B': 
            self.cog = self.cog + 360 / self.weight #evolution inversement proportionel au poids 
        elif cog_orientation == 'T':
            self.cog = self.cog + 360 / self.weight #evolution inversement proportionel au poids
        else:
            #cas ou il n'y a auccune direction on va tout droit
            pass

        ## Correction des billets d'angle    
        if self.cog >= 360.0:
            self.cog = self.cog - 360
        if self.cog <= 0.0:
            self.cog = self.cog + 360
        
        ## Evolution de la latitude et de la longitude
        d = self.speed * delta_t #distance en cartesien
        bearing = np.deg2rad(self.cog)
        self.lat = np.deg2rad(self.lat)
        self.long = np.deg2rad(self.long)

        lat2 = np.arcsin(np.sin(self.lat) * np.cos(d) + np.cos(self.lat) * np.sin(d) * np.cos(bearing))
        dlon = np.atan2(np.sin(bearing) * np.sin(d) * np.cos(self.lat), np.cos(d) - np.sin(self.lat) * np.sin(lat2))
        self.lon2 = np.mod( self.long - dlon + np.pi, 2 * np.pi ) - np.pi
        self.lat = lat2

        self.lat = np.rad2deg(self.lat)
        self.long = np.rad2deg(self.long)
    
    def getParameter(self):
        """
        Return state status of Boat
        """
        output  = [self.lat, self.long, self.speed, self.cog]
        return output


if __name__ == "__main__":
    pass