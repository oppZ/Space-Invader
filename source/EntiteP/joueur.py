"""
Entité qui représente le joueur
Auteurs : Mateusz Wlazlowski et Tancrède Lici
Date de création : 16/12/2021
"""

from EntiteP.entite import Entite
from vecteur2 import Vect2


class Joueur(Entite):
    def __init__(self, vect_pos: Vect2, vies: int) -> None:
        Entite.__init__(self, vect_pos, vies)
