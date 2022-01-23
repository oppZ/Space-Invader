"""
Que fait ce programme: Creation de l'aspect graphique du jeu.
Qui l'a fait: Tancrede Lici, Mateusz Wlazlowski
Quand a-t-il ete realise: 16/12/2021
"""
import tkinter as tk
import json as js
from tkinter import ttk
import time
import threading
from random import randint

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
        self.__lst_blocs = []  # Liste contenant les blocs
        self.__imgs = []  # Liste contenant les images des ennemis
        self.__largeur = 400  # Largeur du canvas
        self.__hauteur = 550  # Hauteur du canvas
        self.__mvt_ennemis = vecteur2.Vect2(x=2, y=0)
        self.__tir_en_cours = False
        self.__t_bonus = randint(3000, 4000)  # Nb de tick ou le bonus apparait
        self.__i_bonus = 0  # Nb de tick ayant passe
        self.__pos_bonus = (self.__largeur + 100, -10)

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
        self.__f.bind("<KeyPress>", self.__appuie_touche, add=True)

        self.__f.mainloop()

    def __commencer(self) -> None:
        """
        Initialistaion du menu de jeu
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

        self.__ecran.focus_force()

        main_loop_thread = threading.Thread(target=self.__mainloop)
        main_loop_thread.start()

    def __menu_princ(self) -> None:
        """
        Initialisation du menu principal
        """
        # Suppression des widgets inutiles
        self.__lab_score.grid_forget()
        self.__lab_vies.grid_forget()
        self.__btn_menu_princ.grid_forget()
        for entite in self.__lst_entites:
            entite.rm_img()
        for entite in self.__lst_blocs:
            entite.rm_img()
        self.__continuer = False

        # Ajout des widgets utiles
        self.__btn_commencer.grid(row=0, column=0, columnspan=2)
        self.__ecran.grid(row=1, column=0, columnspan=2)
        self.__quitter.grid(row=2, column=0, columnspan=2)

    def __defaite(self) -> None:
        """
        Initialisation du menu defaite
        """
        # Ajout des widgets utiles
        self.__btn_rejouer.pack(side="top")

    def __quitte(self) -> None:
        time.sleep(self.__tps_att * 0.001)
        self.__f.destroy()

    def __score(self) -> None:
        """
        Augmentation du score
        """
        self.__nb_score += 1
        self.__set_score()

    def __set_score(self) -> None:
        """
        Affichage du score dans le menu
        """
        self.__txt_score.set("Score: " + str(self.__nb_score))

    def __vies(self) -> None:
        """
        Diminution du nombre de vie
        """
        self.__nb_vies -= 1
        self.__set_score()
        # Appel du menu de defaite quand aucune vie restante
        if self.__nb_vies <= 0:
            self.__defaite()

    def __set_vies(self) -> None:
        """
        Affichage du nombre de vie dans le menu
        """
        self.__txt_vies.set("Vies: " + str(self.__nb_vies))

    def __spawn_entite(self) -> None:
        """
        Initialisation des diverses entites
        """
        # Lecture du fichier json
        with open('json/ennemis_stages.json') as j:
            js_ennemis = js.load(j)

        with open('json/blocs_stages.json') as j:
            js_blocs = js.load(j)

        with open('json/types.json') as j:
            types = js.load(j)

        self.__lst_entites = [None] * (len(js_ennemis["stage1"]) + 3)
        i = 3
        for ennemi in js_ennemis["stage1"]:
            pos = vecteur2.Vect2(x=ennemi["pos_x"], y=ennemi["pos_y"])
            ennemi_tmp = EntiteP.Ennemi(vect_pos=pos, vies=types[ennemi["type"]]["vie"])
            self.__creation_img(ennemi_tmp, types[ennemi["type"]]["img"])
            self.__lst_entites[i] = ennemi_tmp
            i += 1

        self.__lst_blocs = [None] * len(js_blocs["stage1"])
        i = 0
        for bloc in js_blocs["stage1"]:
            pos = vecteur2.Vect2(x=bloc["pos_x"], y=bloc["pos_y"])
            bloc_tmp = EntiteP.Ennemi(vect_pos=pos, vies=types[bloc["type"]]["vie"])
            self.__creation_img(bloc_tmp, types[bloc["type"]]["img"])
            x, y = bloc_tmp.get_position().get_x(), bloc_tmp.get_position().get_y()
            bloc_tmp.get_image().place(x=x, y=y)
            self.__lst_blocs[i] = bloc_tmp
            i += 1

        pos = vecteur2.Vect2(x=self.__largeur / 2, y=self.__hauteur - 50)
        self.__joueur = EntiteP.Joueur(vect_pos=pos, vies=3)
        self.__creation_img(self.__joueur, "../img/joueur.png")
        self.__lst_entites[0] = self.__joueur

        pos = vecteur2.Vect2(x=-100, y=0)
        self.__missile = EntiteP.Missile(vect_pos=pos)
        self.__missile.changer_direction(vecteur2.Vect2(x=0, y=-5))
        self.__creation_img(self.__missile, "../img/missile.png")
        self.__lst_entites[1] = self.__missile

        pos = vecteur2.Vect2(x=self.__pos_bonus[0], y=self.__pos_bonus[1])
        self.__bonus = EntiteP.Ennemi(vect_pos=pos, vies=3)
        self.__creation_img(self.__bonus, "../img/ennemi2.png")
        self.__lst_entites[2] = self.__bonus

    def __creation_img(self, objet: EntiteP, chemin: str) -> None:
        """
        Fonction rassemblant les lignes permettant la creation des images
        :param objet:
        :param chemin:
        """
        image_brute = tk.PhotoImage(file=chemin)
        image = tk.Label(self.__ecran, image=image_brute)
        objet.set_image(image, image_brute)

    def __deplac_ennemis(self) -> None:
        """
        Fonction permettant le deplacement des ennemis et du missile
        """
        # Ennemis
        for ennemi in self.__lst_entites[3:]:
            x = ennemi.get_position().get_x() + self.__mvt_ennemis.get_x()
            if not (0 <= x and x + 40 <= self.__largeur):
                self.__mvt_ennemis.set_x(-self.__mvt_ennemis.get_x())
                break

        for ennemi in self.__lst_entites[3:]:
            ennemi.changer_direction(self.__mvt_ennemis)

        # missile
        if self.__lst_entites[1].get_position().get_y() >= -16:
            self.__lst_entites[1].changer_direction(vecteur2.Vect2(x=0, y=-10))
            self.__tir_en_cours = True
        else:
            self.__tir_en_cours = False

        if self.__t_bonus <= self.__i_bonus:
            self.__lst_entites[2].changer_direction(vecteur2.Vect2(x=-2, y=0))
        if self.__lst_entites[2].get_position().get_x() < -50:
            self.__i_bonus = 0
            pos = vecteur2.Vect2(x=self.__pos_bonus[0], y=self.__pos_bonus[1])
            self.__lst_entites[2].set_position(pos)

    def __appuie_touche(self, event) -> None:
        """
        Appel des fonctions lors de l'appuie d'une touche
        :param event:
        """
        if self.__continuer:
            vect = self.__joueur.get_deplacement()
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
            elif event.keysym == "space" and not self.__tir_en_cours:
                self.__tirer()
                vect = self.__joueur.get_deplacement()

            self.__joueur.changer_direction(vect)
        else:
            if event.keysym == "Escape":
                self.__quitte()
            elif event.keysym == "Return":
                self.__commencer()

    def __tirer(self) -> None:
        """
        Fonction permettant au joueur de tirer
        """
        # x, y = self.__joueur.get_position().get_x() + 17, self.__joueur.get_position().get_y() - 15
        # pos = vecteur2.Vect2(x=x, y=y)
        # self.__missile.set_position(pos)
        position_relative = vecteur2.Vect2(x=17, y=-15)
        position_missile = self.__joueur.get_position() + position_relative
        self.__missile.set_position(position_missile)

    def __destruction(self, bloc) -> None:
        bloc.rm_img()

    def __mainloop(self) -> None:
        """
        Boucle du jeu principale
        TODO: Regler l'erreur lorsqu'on quitte la partie
        :return:
        """
        while self.__continuer:
            time.sleep(self.__tps_att * 0.001)
            try:
                self.__new_tick()
            except tk.TclError:
                print("Faut regler ca")

    def __new_tick(self) -> None:
        """

        :return:
        """
        self.__deplac_ennemis()
        for entity in self.__lst_entites:
            distance = entity.get_deplacement()
            position = entity.get_position()
            nouvelle_position = position + distance
            entity.set_position(pos=nouvelle_position)
            entity.get_image().place(x=nouvelle_position.get_x(), y=nouvelle_position.get_y())

            # on reinitialise le vecteur direction a (x, y) = (0, 0)
            entity.changer_direction(vecteur2.Vect2())


        self.__i_bonus += 1
        
    def colision_test(self, entity1: EntiteP.Entite, entity2: EntiteP.Entite):
        """
        Tests de collisions entre les coordonnées des entités
        
        Entrée:
            entity1: Entite
            entity2: Entite
        Sortie:
            Bool
        """
        
        # cote haut droit
        if entity1.get_position().get_x() <= entity2.get_position().get_x() <= entity1.get_position_etendu().get_x() \
            and entity1.get_position().get_y() <= entity2.get_position().get_y() <= entity1.get_position_etendu().get_y():
            return True
        # cote bas droit
        elif entity2.get_position().get_x() <= entity1.get_position().get_x() <= entity2.get_position_etendu().get_x() \
            and entity2.get_position().get_y() <= entity1.get_position().get_y() <= entity2.get_position_etendu().get_y():
            return True
        # cote haut gauche
        elif entity1.get_position().get_x() <= entity2.get_position().get_x() <= entity1.get_position_etendu().get_x() \
            and entity1.get_position().get_y() <= entity2.get_position_etendu().get_y() <= entity1.get_position_etendu().get_y():
            return True
        # cote bas gauche
        elif entity1.get_position().get_x() <= entity2.get_position().get_x() <= entity1.get_position_etendu().get_x() \
                and entity1.get_position().get_y() <= entity2.get_position_etendu().get_y() <= entity1.get_position_etendu().get_y():
            return True
        else:
            return False

          
