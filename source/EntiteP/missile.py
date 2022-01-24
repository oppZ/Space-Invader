"""
Definition des munitions tirees par le joueur ou par les ennemis
Auteurs : Mateusz Wlazlowski et Tancrède Lici
Date de création : 16/12/2021
"""

from EntiteP.entite import Entite


class Missile(Entite):
    def __init__(self, vect_pos, taille):
        Entite.__init__(self, vect_pos, taille, vies=1)

