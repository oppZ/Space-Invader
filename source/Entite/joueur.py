"""
Entité qui représente le joueur

Auteurs : Mateusz Wlazlowski

Date de création : 16/12/2021
"""

from Entite.entite import Entite
from Entite.boulet import Boulet

class Joueur(Entite):
    def __init__(self, posX, posY, vies):
        Entite.__init__(self, posX, posY, vies)

        self.__score = 0 

    def tirer():
        pass