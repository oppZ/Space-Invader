"""
Entité qui représente le joueur

Auteurs : Mateusz Wlazlowski

Date de création : 16/12/2021
"""

from source.EntiteP.entite import Entite
from source.EntiteP.boulet import Boulet
from source.vecteur2 import Vect2


class Joueur(Entite):
    def __init__(self, vectPos: Vect2, vies: int) -> None:
        Entite.__init__(self, vectPos, vies)

    def tirer(self):
        pass
