"""
On définit ici la classe des entités. Chaque joueur, ennemi et boulet sont des entités.
Auteurs : Mateusz Wlazlowski et Tancrède Lici
Date de création : 16/12/2021
TODO: faire entité une sous classe de fenêtre 
"""

from source import vecteur2


class Entite:
    def __init__(self, vect: vecteur2.Vect2, vies: int, image=None) -> object:
        """
        Initialise l'entite de base

        Entrees:
            vect: Vect2
        Le vecteur position de l'entité
            vies: int
        Le nombre de vies que l'entité possède
        """
        self.__vecteur_position = vect
        self.__vecteur_deplacement = vecteur2.Vect2()

        self.__vies = vies
        self.__image = image

    def changer_direction(self, vect: vecteur2.Vect2):
        """
        Fonction qui permet de déplacer une entité sur la fenêtre.
        Change les coordonées de l'entité.
        TODO: déplacer vraiment, vérifier si on dépasse pas le canvas

        Entrées:
            vect: Vect2
        Le vecteur direction de la classe Vect2
        """
        self.__vecteur_position += vect

    def get_deplacement(self):
        return self.__vecteur_deplacement

    def get_position(self):
        return self.__vecteur_position
