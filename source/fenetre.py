"""
Que fait ce programme: Creation de l'aspect graphique du jeu.
Qui l'a fait: Tancrede Lici, Mateusz Wlazlowski
Quand a-t-il realise: 16/12/2021
TODO: Implementer les entites dans le frame.
"""
import tkinter
from tkinter import *

import Entite


class Fenetre:
    def __init__(self) -> None:
        self.__f = Tk()
        self.__f.title("Les envahisseurs de l'espace.exe")

        self.__nbScore = 0
        self.__nbVies = 3
        self.__txtScore = StringVar()
        self.__txtVies = StringVar()
        self.__setScore()
        self.__setVies()

        self.__labScore = Label(self.__f, textvariable=self.__txtScore)
        self.__labVies = Label(self.__f, textvariable=self.__txtVies)

        self.__ecran = Frame(self.__f, width=400, height=550, background="black")
        self.__btnCommencer = Button(self.__f, text="Commencer", command=self.__commencer)
        self.__quitter = Button(self.__f, text="Quitter", command=self.__f.destroy)
        self.__btnMenuPrinc = Button(self.__f, text="Menu principal", command=self.__menuPrinc)
        self.__btnRejouer = Button(self.__ecran, text="rejouer", command=self.__commencer)

        self.__menuPrinc()

        # objet de l'instance du jeu
        jeu = Jeu(self.__ecran.winfo_x(), self.__ecran.winfo_y(), frame=self.__ecran)

        self.__f.mainloop()

    def __commencer(self) -> None:
        self.__quitter.grid_forget()
        self.__btnCommencer.grid_forget()

        self.__labScore.grid(row=0, column=0, sticky=W)
        self.__labVies.grid(row=0, column=1, sticky=E)
        self.__btnMenuPrinc.grid(row=2, column=0, columnspan=2)

    def __menuPrinc(self) -> None:
        self.__labScore.grid_forget()
        self.__labVies.grid_forget()
        self.__btnMenuPrinc.grid_forget()

        self.__btnCommencer.grid(row=0, column=0, columnspan=2)
        self.__ecran.grid(row=1, column=0, columnspan=2)
        self.__quitter.grid(row=2, column=0, columnspan=2)

    def __defaite(self):
        self.__btnRejouer.pack(side=TOP)

    def __score(self) -> None:
        self.nbScore += 1
        self.__setScore()

    def __setScore(self) -> None:
        self.__txtScore.set("Score: " + str(self.__nbScore))

    def __vies(self) -> None:
        self.nbVies -= 1
        self.__setScore()
        if self.nbVies <= 0:
            pass

    def __setVies(self) -> None:
        self.__txtVies.set("Vies: " + str(self.__nbVies))


"""
Instance du jeu
"""


class Jeu(Fenetre):
    def __init__(self, frameX, frameY, frame: tkinter.Frame):
        self.__frameX = frameX
        self.__frameY = frameY
        self.__frame = frame

        self.__frameTime = 33  # ms

        # on associe les touches du clavier aux evenements
        self.__frame.bind("<Key>", self.__bouger, add=True)
        #self.__frame.bind("<Motion>", self.__bouger, add=True)


    def __spawnEntite(self):
        self.__joueur = Entite.Joueur(posX=self.__frameX/2, posY=self.__frameY - 50, vies=3)

    def __bouger(self, event):
        print(event)
        pass


Fenetre()
