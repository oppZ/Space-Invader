"""
On définit les munitions qui vont être tirés par le joueur ou par les ennemis

Auteurs : Mateusz Wlazlowski et Trancrède Lici

Date de création : 16/12/2021
"""

from EntiteP.entite import Entite


class Missile(Entite):
    def __init__(self, vect_pos):
        Entite.__init__(self, vect_pos, vies=1)

    def get_coord(self) -> tuple:
        x, y = self.get_position().get_x(), self.get_position().get_y()
        return x, y, x+5, y+15
