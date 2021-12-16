"""
On définit un vecteur position ou un vecteur direction en 2 dimensions

Auteurs : Mateusz Wlazlowski et Tancrède Lici

Date de création : 16/12/2021
"""

class Vect2():
    def __init__(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
    
    def __mul__(self, other):
        return Vect2(self.__x * other.__x, self.__y * other.__y)

    def __add__(self, other):
        return Vect2(self.__x + other.__x, self.__y + other.__y)

    def __str__(self):
        return str(self.__x) + " " + str(self.__y)

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y

    def setX(self, x):
        if isinstance(x, int):
            self.__x = x

    def setY(self, y):
        if isinstance(y, int):
            self.__y = y

