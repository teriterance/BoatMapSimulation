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
