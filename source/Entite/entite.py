"""
On définit ici la classe des entités. Chaque joueur, ennemi et boulet sont des entités.
Auteurs : Mateusz Wlazlowski et Tancrède Lici
Date de création : 16/12/2021
TODO: faire entité une sous classe de fenêtre 
"""

from .. import vecteur2

class Entite():
    def __init__(self, vect: vecteur2.Vect2, vies: int):
        self.__vecteurPosition = vect
        self.__vecteurDeplacement = vecteur2.Vect2()

        self.__vies = vies

    def __seDeplacer(self, vect: vecteur2.Vect2):
        """
        Fonction qui permet de déplacer une entité sur la fenêtre.
        Change les coordonées de l'entité.
        TODO: déplacer vraiment, vérifier si on dépasse pas le canvas

        Entrées:
            vect: Vect2
        Le vecteur direction de la classe Vect2
        """
        self.__vecteurPosition += vect

