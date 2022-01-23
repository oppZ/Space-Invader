"""
On définit les munitions qui vont être tirés par le joueur ou par les ennemis

Auteurs : Mateusz Wlazlowski et Trancrède Lici

Date de création : 16/12/2021
"""

from source.EntiteP.entite import Entite


class Missile(Entite):
    def __init__(self, vect_pos):
        Entite.__init__(self, vect_pos, vies=1)
