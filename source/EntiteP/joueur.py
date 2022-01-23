"""
Entité qui représente le joueur

Auteurs : Mateusz Wlazlowski

Date de création : 16/12/2021
"""

from source.EntiteP.entite import Entite
from source.EntiteP.missile import Missile
from source.vecteur2 import Vect2


class Joueur(Entite):
    def __init__(self, vect_pos: Vect2, vies: int) -> None:
        Entite.__init__(self, vect_pos, vies)

    def tirer(self):

        pass
