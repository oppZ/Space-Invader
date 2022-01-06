"""
On définit les munitions qui vont être tirés par le joueur ou par les ennemis

Auteurs : Mateusz Wlazlowski et Trancrède Lici

Date de création : 16/12/2021
"""

from entite import Entite

class Boulet(Entite):
    def __init__(self, vectPos):
        Entite.__init__(posX, posY, vies = 1)

    