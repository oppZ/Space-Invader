class Entite():
    def __seDeplacer(self, direction, distance):
        if direction == "haut":
            self.__posY -= distance
        elif direction == "bas":
            self.__posY += distance
        elif direction == "droite":
            self.__posX += distance
        elif direction == "gauche":
            self.__posX -= distance

    

    self.__posX = 0
    self.__posY = 0

    self.__apparence = ""
    self.__nom = ""

    