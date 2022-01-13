"""
Que fait ce programme: Creation de l'aspect graphique du jeu.
Qui l'a fait: Tancrede Lici, Mateusz Wlazlowski
Quand a-t-il realise: 16/12/2021
TODO: Implementer les entites dans le frame.
"""

import tkinter as tk
import json as js
from tkinter import ttk
import time
import threading

import EntiteP
import vecteur2


class Fenetre:
    """
    Classe permettant de creer les differents menu du jeu
    """

    def __init__(self) -> None:
        # Creation de la fenetre
        self.f = tk.Tk()
        self.f.title("Les envahisseurs de l'espace.exe")

        # Initialisation des variables
        self.__nbScore = 0
        self.__nbVies = 3
        self.__txtScore = tk.StringVar()
        self.__txtVies = tk.StringVar()
        self.__set_score()
        self.__set_vies()

        # Creation des widgets
        self.__labScore = tk.Label(self.f, textvariable=self.__txtScore)
        self.__labVies = tk.Label(self.f, textvariable=self.__txtVies)
        self.__ecran = tk.Frame(self.f, width=400, height=550, bg="black")
        self.__btnCommencer = ttk.Button(self.f, text="Commencer", command=self.__commencer)
        self.__quitter = ttk.Button(self.f, text="Quitter", command=self.f.destroy)
        self.__btnMenuPrinc = ttk.Button(self.f, text="Menu principal", command=self.__menu_princ)
        self.__btnRejouer = ttk.Button(self.__ecran, text="rejouer", command=self.__commencer)

        # Initialisation du menu principal
        self.__menu_princ()

        # objet de l'instance du jeu
        self.frameX = self.__ecran.winfo_x()
        self.frameY = self.__ecran.winfo_y()
        self.frame = self.__ecran

    def __commencer(self) -> None:
        """
        Initialistaion du menu de jeu
        :return:
        """
        # Suppression des widgets inutiles
        self.__quitter.grid_forget()
        self.__btnCommencer.grid_forget()

        # Ajout des widgets utiles
        self.__labScore.grid(row=0, column=0, sticky='W')
        self.__labVies.grid(row=0, column=1, sticky='E')
        self.__btnMenuPrinc.grid(row=2, column=0, columnspan=2)


    def __menu_princ(self) -> None:
        """
        Initialisation du menu principal
        :return:
        """
        # Suppression des widgets inutiles
        self.__labScore.grid_forget()
        self.__labVies.grid_forget()
        self.__btnMenuPrinc.grid_forget()

        # Ajout des widgets utiles
        self.__btnCommencer.grid(row=0, column=0, columnspan=2)
        self.__ecran.grid(row=1, column=0, columnspan=2)
        self.__quitter.grid(row=2, column=0, columnspan=2)

    def __defaite(self):
        """
        Initialisation du menu defaite
        :return:
        """
        # Ajout des widgets utiles
        self.__btnRejouer.pack(side="top")

    def __score(self) -> None:
        """
        Augmentation du score
        :return:
        """
        self.__nbScore += 1
        self.__set_score()

    def __set_score(self) -> None:
        """
        Affichage du score dans le menu
        :return:
        """
        self.__txtScore.set("Score: " + str(self.__nbScore))

    def __vies(self) -> None:
        """
        Diminution du nombre de vie
        :return:
        """
        self.__nbVies -= 1
        self.__set_score()
        # Appel du menu de defaite quand aucune vie restante
        if self.__nbVies <= 0:
            self.__defaite()

    def __set_vies(self) -> None:
        """
        Affichage du nombre de vie dans le menu
        :return:
        """
        self.__txtVies.set("Vies: " + str(self.__nbVies))


class Jeu(Fenetre):
    """
    Instance du jeu
    """

    def __init__(self) -> None:
        Fenetre.__init__(self)
        self.__frameTime = 33  # ms
        self.__entityList = []

        self.frame.focus_force()

        # on associe les touches du clavier aux evenements
        self.frame.bind("<KeyPress>", self.changerDirection, add=True)

        self.spawnEntite()

        #mainLoopThread = threading.Thread(target=self.__mainloop())
        #mainLoopThread.start()

        self.f.mainloop()

        #print("err")

    def spawnEntite(self):
        """
        Initialisation des diverses entites
        TODO: Enlever le padding des images
        :return:
        """
        position = vecteur2.Vect2(x=self.frameX / 2, y=self.frameY - 50)
        self.__joueur = EntiteP.Joueur(vectPos=position, vies=3)

        # Lecture du fichier json
        with open('json\stages.json') as j:
            donnees = js.load(j)

        # Affichage d'un ennemi dans le frame
        self.__ennemi = tk.PhotoImage(file="..\img\ennemi1.png")
        __img = tk.Label(self.frame, image=self.__ennemi)
        self.__joueur.__image = __img
        __img.place(x=donnees["stage1"][0]["posX"], y=donnees["stage1"][0]["posY"])

    def changerDirection(self, event):
        """
        Permettre au joueur de changer sa direction
        :param event:
        """
        if event.keysym == "Up":
            vect = vecteur2.Vect2(x=0, y=-0.5)
        elif event.keysym == "Down":
            vect = vecteur2.Vect2(x=0, y=0.5)
        elif event.keysym == "Right":
            vect = vecteur2.Vect2(x=0.5, y=0)
        elif event.keysym == "Left":
            vect = vecteur2.Vect2(x=-0.5, y=0)

        self.__joueur.changerDirection(vect)

    def __mainloop(self):
        """
        Boucle du jeu principale
        :return:
        """
        while True:
            time.sleep(self.__frameTime * 0.001)
            self.__newTick()

    def __newTick(self):
        """

        :return:
        """
        for entity in self.__entityList + [self.__joueur]:
            distanceX = entity.getDeplacament().getX()
            distanceY = entity.getDeplacament().getY()
            positionX = entity.getPosition().getX()
            positionY = entity.getPosition().getY()
            entity.__image.place(x=positionX + distanceX, y=positionY + distanceY)

        # reinitialise la direction a 0
        self.__joueur.changerDirection(vect=vecteur2.Vect2())


Jeu()
