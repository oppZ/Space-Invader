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
        self.__tps_att = 33  # ms
        self.__lst_ennemis = []  # Liste contenant les ennemis
        self.__imgs = []  # Liste contenant les images des ennemis
        self.__largeur = 400
        self.__hauteur = 550

        # Creation des widgets
        self.__lab_score = tk.Label(self.__f, textvariable=self.__txt_score)
        self.__lab_vies = tk.Label(self.__f, textvariable=self.__txt_vies)
        self.__ecran = tk.Frame(self.__f, width=self.__largeur, height=self.__hauteur, bg="black")
        self.__btn_commencer = ttk.Button(self.__f, text="Commencer", command=self.__commencer)
        self.__quitter = ttk.Button(self.__f, text="Quitter", command=self.__quitte)
        self.__btn_menu_princ = ttk.Button(self.__f, text="Menu principal", command=self.__menu_princ)
        self.__btn_rejouer = ttk.Button(self.__ecran, text="rejouer", command=self.__commencer)

        # Initialisation du menu principal
        self.__menu_princ()

        # objet de l'instance du jeu
        self.__ecran.focus_force()

        # on associe les touches du clavier aux evenements
        self.__f.bind("<KeyPress>", self.__changer_direction, add=True)

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

        self.continuer = True

        main_loop_thread = threading.Thread(target=self.__mainloop)
        main_loop_thread.start()

    def __menu_princ(self) -> None:
        """
        Initialisation du menu principal
        TODO: Supprimer les entites
        :return:
        """
        # Suppression des widgets inutiles
        self.__lab_score.grid_forget()
        self.__lab_vies.grid_forget()
        self.__btn_menu_princ.grid_forget()

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

    def __quitte(self):
        self.continuer = False
        time.sleep(self.__frame_time * 0.001)
        self.__f.destroy()

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
        TODO: Enlever le padding des images
        :return:
        """
        position = vecteur2.Vect2(x=self.__largeur / 2, y=self.__hauteur - 50)
        self.__joueur = EntiteP.Joueur(vect_pos=position, vies=3)

        image_brute = tk.PhotoImage(file="../img/joueur.png")
        image = tk.Label(self.__ecran, image=image_brute)
        self.__joueur.set_image(image, image_brute)

        # Lecture du fichier json
        with open('json/stages.json') as j:
            js_ennemis = js.load(j)

        with open('json/types.json') as j:
            types = js.load(j)

        for ennemi in js_ennemis["stage1"]:
            pos = vecteur2.Vect2(x=ennemi["pos_x"], y=ennemi["pos_y"])
            self.__lst_ennemis.append(EntiteP.Ennemi(vect_pos=pos, vies=types[ennemi["type"]]["vie"]))
        self.__deplac_ennemis()

    def __deplac_ennemis(self) -> None:
        """
        Deplacement des ennemis
        TODO: Faire en sorte que les ennemis se deplacent + detection des collisions
        :return:
        """
        for ennemi in self.__lst_ennemis:
            dep = vecteur2.Vect2(x=10, y=0)
            if ennemi.get_position().get_x()+dep.get_x()+40 <= self.__hauteur:
                ennemi.changer_direction(dep)

    def __changer_direction(self, event) -> None:
        """
        Permettre au joueur de changer sa direction
        :param event:
        """
        if event.keysym == "Up":
            vect = vecteur2.Vect2(x=0, y=-2)
        elif event.keysym == "Down":
            vect = vecteur2.Vect2(x=0, y=2)
        elif event.keysym == "Right":
            vect = vecteur2.Vect2(x=2, y=0)
        elif event.keysym == "Left":
            vect = vecteur2.Vect2(x=-2, y=0)
        else:
            vect = self.__joueur.get_deplacament()
        print(vect)

        self.__joueur.changer_direction(vect)

    def __mainloop(self):
        """
        Boucle du jeu principale
        :return:
        """
        while self.continuer:
            time.sleep(self.__frame_time * 0.001)
            self.__new_tick()

    def __new_tick(self):
        """

        :return:
        """
        for entity in [self.__joueur]:
            distance_x = entity.get_deplacement().get_x()
            distance_y = entity.get_deplacement().get_y()
            position_x = entity.get_position().get_x()
            position_y = entity.get_position().get_y()
            entity.get_image().place(x=position_x + distance_x, y=position_y + distance_y)

        # reinitialise la direction a 0
        self.__joueur.changer_direction(vect=vecteur2.Vect2())
