"""
Classe qui représente les ennemis dans le jeu

Auteurs : Mateusz Wlazlowski et Tancrède Lici

Date de création : 16/12/2021
"""

from source.EntiteP.entite import Entite


class Ennemi(Entite):
    def __init__(self, vect_pos, vies, score):
        Entite.__init__(self, vect_pos, vies)

        self.__score = 0

    def get_score(self):
        """
        Retourne le score a ajouter au joueur lorsque l'ennemi est abbatu
        :return:
            int
        """
        return self.__score
