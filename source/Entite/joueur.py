"""
Entité qui représente le joueur

Auteurs : Mateusz Wlazlowski

Date de création : 16/12/2021
"""

from entite import Entite
from boulet import Boulet


class Joueur(Entite):
    def __init__(self, vectPos, vies):
        Entite.__init__(self, vectPos, vies)

    def tirer(self):
        pass
