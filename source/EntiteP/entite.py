"""
On définit ici la classe des entités. Chaque joueur, ennemi et boulet sont des entités.
Auteurs : Mateusz Wlazlowski et Tancrède Lici
Date de création : 16/12/2021
"""

import vecteur2


class Entite:
    def __init__(self, vect: vecteur2.Vect2, taille: vecteur2.Vect2, vies: int, image=None) -> None:
        # vecteurs positions et déplacement de l'entite
        self.__vecteur_position = vect
        self.__vecteur_deplacement = vecteur2.Vect2()
        self.__vecteur_position_2eme_cote = self.__vecteur_position + taille

        # constantes
        self.__vies = vies
        self.__image = image
        self.__image_brute = ""

    def changer_direction(self, vect: vecteur2.Vect2):
        """
        Fonction qui permet de déplacer une entité sur la fenêtre.
        Change les coordonées de l'entité.
        """
        self.__vecteur_deplacement = vect

    def get_deplacement(self):
        """
        Retourner le vecteur deplacement
        """
        return self.__vecteur_deplacement

    def get_position(self):
        """
        Retourner le vecteur position
        """
        return self.__vecteur_position

    def get_position_etendue(self):
        """
        Retourner la position etendue
        """
        return self.__vecteur_position_2eme_cote

    def set_position(self, pos: vecteur2.Vect2):
        self.__vecteur_position = pos

    def set_position_etendue(self, position):
        """
        Definir la position etendu
        """
        self.__vecteur_position_2eme_cote = position

    def get_image(self):
        return self.__image

    def set_image(self, image, image_brute):
        """
        Definir l'image
        """
        self.__image = image
        self.__image_brute = image_brute

    def rm_img(self):
        """
        Detruire l'image du jeu
        """
        self.__image.destroy()

