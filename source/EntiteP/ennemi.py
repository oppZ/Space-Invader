"""
Classe qui représente les ennemis dans le jeu

Auteurs : Mateusz Wlazlowski et Tancrède Lici

Date de création : 16/12/2021
"""

from source.EntiteP.entite import Entite


class Ennemi(Entite):
    def __init__(self, vect_pos, vies):
        Entite.__init__(self, vect_pos, vies)
