"""
Que fait ce programme: Creation de l'aspect graphique du jeu.
Qui l'a fait: Tancrede Lici, Mateusz Wlazlowski
Quand a-t-il ete realise: 16/12/2021
"""
import tkinter
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
        self.__lst_entites = []  # Liste contenant les ennemis
        self.__imgs = []  # Liste contenant les images des ennemis
        self.__largeur = 400
        self.__hauteur = 550
        self.__mvt_ennemis = vecteur2.Vect2(x=2, y=0)
        self.tir_en_cours = False

        # Creation des widgets
        self.__lab_score = tk.Label(self.__f, textvariable=self.__txt_score)
        self.__lab_vies = tk.Label(self.__f, textvariable=self.__txt_vies)
        self.__ecran = tk.Canvas(self.__f, width=self.__largeur, height=self.__hauteur, bg="black")
        self.__btn_commencer = ttk.Button(self.__f, text="Commencer", command=self.__commencer)
        self.__quitter = ttk.Button(self.__f, text="Quitter", command=self.__quitte)
        self.__btn_menu_princ = ttk.Button(self.__f, text="Menu principal", command=self.__menu_princ)
        self.__btn_rejouer = ttk.Button(self.__ecran, text="rejouer", command=self.__commencer)

        # Initialisation du menu principal
        self.__menu_princ()

        # objet de l'instance du jeu
        self.__ecran.focus_force()

        # on associe les touches du clavier aux evenements
        self.__f.bind("<KeyPress>", self.__appuie_touche, add=True)

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

        self.__continuer = True

        main_loop_thread = threading.Thread(target=self.__mainloop)
        main_loop_thread.start()

    def __menu_princ(self) -> None:
        """
        Initialisation du menu principal
        :return:
        """
        # Suppression des widgets inutiles
        self.__lab_score.grid_forget()
        self.__lab_vies.grid_forget()
        self.__btn_menu_princ.grid_forget()
        for entite in self.__lst_entites:
            entite.rm_img()
        self.__continuer = False

        # Ajout des widgets utiles
        self.__btn_commencer.grid(row=0, column=0, columnspan=2)
        self.__ecran.grid(row=1, column=0, columnspan=2)
        self.__quitter.grid(row=2, column=0, columnspan=2)

    def __defaite(self) -> None:
        """
        Initialisation du menu defaite
        :return:
        """
        # Ajout des widgets utiles
        self.__btn_rejouer.pack(side="top")

    def __quitte(self) -> None:
        time.sleep(self.__tps_att * 0.001)
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
        :return:
        """
        # Lecture du fichier json
        with open('json/stages.json') as j:
            js_ennemis = js.load(j)

        with open('json/types.json') as j:
            types = js.load(j)

        self.__lst_entites = [None]*(len(js_ennemis["stage1"])+2)
        i = 2
        for ennemi in js_ennemis["stage1"]:
            pos = vecteur2.Vect2(x=ennemi["pos_x"], y=ennemi["pos_y"])
            ennemi_tmp = EntiteP.Ennemi(vect_pos=pos, vies=types[ennemi["type"]]["vie"])
            self.__creation_img(ennemi_tmp, types[ennemi["type"]]["img"])
            self.__lst_entites[i] = ennemi_tmp
            i += 1

        pos = vecteur2.Vect2(x=self.__largeur/2, y=self.__hauteur-50)
        self.__joueur = EntiteP.Joueur(vect_pos=pos, vies=3)
        self.__creation_img(self.__joueur, "../img/joueur.png")
        self.__lst_entites[0] = self.__joueur

        pos = vecteur2.Vect2(x=-100, y=0)
        self.__missile = EntiteP.Missile(vect_pos=pos)
        self.__creation_img(self.__missile, "../img/missile.png")
        self.__lst_entites[1] = self.__missile

    def __creation_img(self, objet: EntiteP, chemin: str) -> None:
        """
        Fonction rassemblant les lignes permettant la creation des images
        :param objet:
        :param chemin:
        :return:
        """
        image_brute = tk.PhotoImage(file=chemin)
        image = tk.Label(self.__ecran, image=image_brute)
        objet.set_image(image, image_brute)

    def __deplac_ennemis(self) -> None:
        """
        Deplacement des ennemis
        :return:
        """
        for ennemi in self.__lst_entites[2:]:
            x = ennemi.get_position().get_x()+self.__mvt_ennemis.get_x()
            if not (0 <= x and x+40 <= self.__largeur):
                self.__mvt_ennemis.set_x(-self.__mvt_ennemis.get_x())
                break

        for ennemi in self.__lst_entites[2:]:
            ennemi.changer_direction(self.__mvt_ennemis)

        if self.__lst_entites[1].get_position().get_y() >= -16:
            self.__lst_entites[1].changer_direction(vecteur2.Vect2(x=0, y=-10))
            self.tir_en_cours = True
            #coord = self.__ecran.coords(self.__lst_entites[1].get_image())
            #coll = self.__ecran.find_overlapping(coord[0], coord[1], coord[2], coord[3])
            #print(coll)
        else:
            self.tir_en_cours = False

    def __appuie_touche(self, event) -> None:
        """
        Permettre au joueur de changer sa direction
        :param event:
        """
        if self.__continuer:
            if event.keysym == "Up":
                vect = vecteur2.Vect2(x=0, y=-2)
            elif event.keysym == "Down":
                vect = vecteur2.Vect2(x=0, y=2)
            elif event.keysym == "Right":
                vect = vecteur2.Vect2(x=2, y=0)
            elif event.keysym == "Left":
                vect = vecteur2.Vect2(x=-2, y=0)
            elif event.keysym == "Escape":
                self.__menu_princ()
                vect = self.__joueur.get_deplacement()
            elif event.keysym == "space" and not self.tir_en_cours:
                self.__tirer()
                vect = self.__joueur.get_deplacement()
            else:
                vect = self.__joueur.get_deplacement()
            self.__joueur.changer_direction(vect)
        else:
            if event.keysym == "Escape":
                self.__quitte()
            elif event.keysym == "Return":
                self.__commencer()

    def __tirer(self) -> None:
        x, y = self.__joueur.get_position().get_x()+17, self.__joueur.get_position().get_y()-15
        pos = vecteur2.Vect2(x=x, y=y)
        self.__missile.set_position(pos)

    def __mainloop(self):
        """
        Boucle du jeu principale
        TODO: Regler l'erreur lorsqu'on quitte la partie
        :return:
        """
        while self.__continuer:
            time.sleep(self.__tps_att*0.001)
            try:
                self.__new_tick()
            except tk.TclError:
                print("Faut regler ca")

    def __new_tick(self):
        """

        :return:
        """
        self.__deplac_ennemis()
        for entity in self.__lst_entites:
            distance_x = entity.get_deplacement().get_x()
            distance_y = entity.get_deplacement().get_y()
            position_x = entity.get_position().get_x()
            position_y = entity.get_position().get_y()
            entity.get_image().place(x=position_x + distance_x, y=position_y + distance_y)

        # reinitialise la direction a 0
        self.__joueur.changer_direction(vect=vecteur2.Vect2())
