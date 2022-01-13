"""
Que fait ce programme: Creation de l'aspect graphique du jeu.
Qui l'a fait: Tancrede Lici, Mateusz Wlazlowski
Quand a-t-il realise: 16/12/2021

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
        self.__f = tk.Tk()
        self.__f.title("Les zinzins de l'espace Schengen.exe")

        # Initialisation des variables
        self.__nb_score = 0
        self.__nb_vies = 3
        self.__txt_score = tk.StringVar()
        self.__txt_vies = tk.StringVar()
        self.__set_score()
        self.__set_vies()
        self.__frame_time = 33  # ms
        self.__lst_ennemis = []  # Liste contenant les ennemis
        self.__imgs = []  # Liste contenant les images des ennemis

        # Creation des widgets
        self.__lab_score = tk.Label(self.__f, textvariable=self.__txt_score)
        self.__lab_vies = tk.Label(self.__f, textvariable=self.__txt_vies)
        self.__ecran = tk.Frame(self.__f, width=400, height=550, bg="black")
        self.__btn_commencer = ttk.Button(self.__f, text="Commencer", command=self.__commencer)
        self.__quitter = ttk.Button(self.__f, text="Quitter", command=self.__f.destroy)
        self.__btn_menu_princ = ttk.Button(self.__f, text="Menu principal", command=self.__menu_princ)
        self.__btn_rejouer = ttk.Button(self.__ecran, text="rejouer", command=self.__commencer)

        # Initialisation du menu principal
        self.__menu_princ()

        # objet de l'instance du jeu
        self.__ecran_x = self.__ecran.winfo_x()
        self.__ecran_y = self.__ecran.winfo_y()
        self.__ecran.focus_force()

        # on associe les touches du clavier aux evenements
        self.__ecran.bind("<KeyPress>", self.__changer_direction, add=True)

        self.__f.mainloop()

    def __commencer(self) -> None:
        """
        Initialistaion du menu de jeu
        :return:
        """
        # Suppression des widgets inutiles
        self.__quitter.grid_forget()
        self.__btn_commencer.grid_forget()

        # Ajout des widgets utiles
        self.__lab_score.grid(row=0, column=0, sticky='W')
        self.__lab_vies.grid(row=0, column=1, sticky='E')
        self.__btn_menu_princ.grid(row=2, column=0, columnspan=2)

        self.__spawn_entite()

    def __menu_princ(self) -> None:
        """
        Initialisation du menu principal
        :return:
        """
        # Suppression des widgets inutiles
        self.__lab_score.grid_forget()
        self.__lab_vies.grid_forget()
        self.__btn_menu_princ.grid_forget()
        for ennemi in self.__lst_ennemis:
            ennemi.place_forget()

        # Ajout des widgets utiles
        self.__btn_commencer.grid(row=0, column=0, columnspan=2)
        self.__ecran.grid(row=1, column=0, columnspan=2)
        self.__quitter.grid(row=2, column=0, columnspan=2)

    def __defaite(self):
        """
        Initialisation du menu defaite
        :return:
        """
        # Ajout des widgets utiles
        self.__btn_rejouer.pack(side="top")

    def __score(self) -> None:
        """
        Augmentation du score
        :return:
        """
        self.__nb_score += 1
        self.__set_score()

    def __set_score(self) -> None:
        """
        Affichage du score dans le menu
        :return:
        """
        self.__txt_score.set("Score: " + str(self.__nb_score))

    def __vies(self) -> None:
        """
        Diminution du nombre de vie
        :return:
        """
        self.__nb_vies -= 1
        self.__set_score()
        # Appel du menu de defaite quand aucune vie restante
        if self.__nb_vies <= 0:
            self.__defaite()

    def __set_vies(self) -> None:
        """
        Affichage du nombre de vie dans le menu
        :return:
        """
        self.__txt_vies.set("Vies: " + str(self.__nb_vies))

    def __spawn_entite(self) -> None:
        """
        Initialisation des diverses entites
        :return:
        """
        position = vecteur2.Vect2(x=self.__ecran_x / 2, y=self.__ecran_y - 50)
        self.__joueur = EntiteP.Joueur(vectPos=position, vies=3)

        # Lecture du fichier json
        with open('json/stages.json') as j:
            js_ennemis = js.load(j)

        with open('json/types.json') as j:
            types = js.load(j)

        # Affichage des ennemis
        for ennemi in js_ennemis["stage1"]:
            self.__imgs.append(tk.PhotoImage(file=types[ennemi["type"]]["img"]))
            self.__lst_ennemis.append(tk.Label(self.__ecran, image=self.__imgs[-1]))
            self.__lst_ennemis[-1].place(x=ennemi["posX"], y=ennemi["posY"])

        self.__deplac_ennemis()

    def __deplac_ennemis(self) -> None:
        """
        Deplacement des ennemis
        :return:
        """

    def __changer_direction(self, event):
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
            time.sleep(self.__frame_time * 0.001)
            self.__new_tick()

    def __new_tick(self):
        """

        :return:
        """
        for entity in self.__lst_ennemis + [self.__joueur]:
            distance_x = entity.getDeplacament().getX()
            distance_y = entity.getDeplacament().getY()
            position_x = entity.getPosition().getX()
            position_y = entity.getPosition().getY()
            entity.__image.place(x=position_x + distance_x, y=position_y + distance_y)

        # reinitialise la direction a 0
        self.__joueur.changerDirection(vect=vecteur2.Vect2())
