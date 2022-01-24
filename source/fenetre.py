"""
Que fait ce programme: Creation de l'aspect graphique du jeu.
Qui l'a fait: Mateusz Wlazlowski et Tancrède Lici
Quand a-t-il ete realise: 16/12/2021
"""
import tkinter
import tkinter as tk
import json as js
from tkinter import ttk, messagebox
import time
import threading
from random import randint

import EntiteP
import vecteur2


class Fenetre:
    """
    Classe permettant de creer les differents menus du jeu
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
        self.__largeur = 635  # Largeur du canvas
        self.__hauteur = 635  # Hauteur du canvas
        self.__mvt_ennemis = vecteur2.Vect2(x=2, y=0)
        self.__tir_en_cours = False
        self.__t_bonus = 0  # Nb de tick ou le bonus apparait
        self.__i_bonus = 0  # Nb de tick ayant passe
        self.__pos_bonus = (self.__largeur + 10, 10)

        # Creation des widgets
        self.__lab_score = tk.Label(self.__f, textvariable=self.__txt_score)
        self.__lab_vies = tk.Label(self.__f, textvariable=self.__txt_vies)
        self.__frame = tk.Frame(self.__f, width=self.__largeur, height=self.__hauteur, bg="black")
        self.__btn_commencer = ttk.Button(self.__f, text="Commencer", command=self.__commencer)
        self.__quitter = ttk.Button(self.__f, text="Quitter", command=self.__quitte)
        self.__btn_menu_princ = ttk.Button(self.__f, text="Menu principal", command=self.__menu_princ)
        self.__btn_rejouer = ttk.Button(self.__frame, text="rejouer", command=self.__commencer)
        self.__chemin_schengen = tk.PhotoImage(file="../img/schengen.png")
        self.__img_schengen = tk.Label(self.__frame, image=self.__chemin_schengen)

        # Creation d'un menu a propos
        menubar = tkinter.Menu(self.__f)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="A propos", command=self.apropos)
        menubar.add_cascade(label="A propos", menu=filemenu)
        self.__f.config(menu=menubar)

        # Initialisation du menu principal
        self.__menu_princ()

        # objet de l'instance du jeu
        self.__frame.focus_force()

        # on associe les touches du clavier aux evenements
        self.__f.bind("<KeyPress>", self.__appuie_touche, add=True)

        self.__f.mainloop()

    def apropos(self):
        # message a propos en utilisant une pile
        message = []
        message.append("LICI Tancrède & WLAZLOWSKI Mateusz")
        message.append("Ce Space Invadeur a été créé par :")
        message_complet = message[-1] + '\n'
        message.pop()
        message_complet += message[-1]
        message.pop()

        tkinter.messagebox.showinfo(title="A propos", message=message_complet)

    def __commencer(self) -> None:
        """
        Initialistaion du menu de jeu
        """
        # Suppression des widgets inutiles
        self.__quitter.grid_forget()
        self.__btn_commencer.grid_forget()
        self.__img_schengen.pack_forget()

        # Ajout des widgets utiles
        self.__lab_score.grid(row=0, column=0, sticky='W')
        self.__lab_vies.grid(row=0, column=1, sticky='E')
        self.__btn_menu_princ.grid(row=2, column=0, columnspan=2)

        self.__spawn_entite()

        self.__continuer = True
        self.__t_bonus = randint(500, 1000)  # Nb de tick ou le bonus apparait

        self.__frame.focus_force()

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
        self.__frame.grid(row=1, column=0, columnspan=2)
        self.__quitter.grid(row=2, column=0, columnspan=2)
        self.__img_schengen.pack()

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
            # initialisation de l'ennemi
            pos = vecteur2.Vect2(x=ennemi["pos_x"], y=ennemi["pos_y"])
            ennemi_tmp = EntiteP.Ennemi(vect_pos=pos, taille=vecteur2.Vect2(x=40, y=40), vies=types[ennemi["type"]]["vie"])
            # on enregistre l'ennemi avec une image dans une liste d'ennemis
            self.__creation_img(ennemi_tmp, types[ennemi["type"]]["img"])
            self.__lst_entites[i] = ennemi_tmp
            i += 1

        self.__lst_blocs = [None] * len(js_blocs["stage1"])
        i = 0
        for bloc in js_blocs["stage1"]:
            # initialisation du bloc protecteur avec l'image
            pos = vecteur2.Vect2(x=bloc["pos_x"], y=bloc["pos_y"])
            bloc_tmp = EntiteP.Ennemi(vect_pos=pos, taille=vecteur2.Vect2(x=40, y=40), vies=types["bloc"]["vie"])
            x, y = bloc_tmp.get_position().get_x(), bloc_tmp.get_position().get_y()
            self.__creation_img(bloc_tmp, types["bloc"]["img"])
            bloc_tmp.get_image().place(x=x, y=y)
            # ajout du bloc protecteur dans la liste d'objects
            self.__lst_blocs[i] = bloc_tmp
            i += 1

        # initialisation du joueur
        pos = vecteur2.Vect2(x=self.__largeur / 2, y=self.__hauteur - 50)
        self.__joueur = EntiteP.Joueur(vect_pos=pos, taille=vecteur2.Vect2(x=40, y=40), vies=3)
        self.__creation_img(self.__joueur, "../img/joueur.png")
        self.__lst_entites[0] = self.__joueur

        # initialisation du missile
        pos = vecteur2.Vect2(x=-100, y=0)
        self.__missile = EntiteP.Missile(vect_pos=pos, taille=vecteur2.Vect2(x=5, y=15))
        self.__missile.changer_direction(vecteur2.Vect2(x=0, y=-5))
        self.__creation_img(self.__missile, "../img/missile.png")
        self.__lst_entites[1] = self.__missile

        # initialisation de l'ennemis 'bonus' a la position 2
        pos = vecteur2.Vect2(x=self.__pos_bonus[0], y=self.__pos_bonus[1])
        self.__bonus = EntiteP.Ennemi(vect_pos=pos, taille=vecteur2.Vect2(x=15, y=15), vies=3)
        self.__creation_img(self.__bonus, "../img/ennemi2.png")
        self.__lst_entites[2] = self.__bonus

    def __creation_img(self, objet: EntiteP, chemin: str) -> None:
        """
        Fonction rassemblant les lignes permettant la creation des images
        :param objet:
        :param chemin:
        """
        image_brute = tk.PhotoImage(file=chemin)
        image = tk.Label(self.__frame, image=image_brute)
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

        # Missile
        if self.__lst_entites[1].get_position().get_y() >= -16 and self.__lst_entites[1].get_deplacement().get_y() != -1000:
            self.__lst_entites[1].changer_direction(vecteur2.Vect2(x=0, y=-10))
            self.__tir_en_cours = True
        else:
            self.__tir_en_cours = False

        # Bonus
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
            # touches pour changer sa direction de deplacement
            if event.keysym == "Right":
                vect = vecteur2.Vect2(x=4, y=0)
            elif event.keysym == "Left":
                vect = vecteur2.Vect2(x=-4, y=0)

            elif event.keysym == "Escape":
                self.__menu_princ()
            # tirer un missile
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
        position_relative = vecteur2.Vect2(x=17, y=-15)
        position_missile = self.__joueur.get_position() + position_relative
        self.__missile.set_position(position_missile)

    def __mainloop(self) -> None:
        """
        Boucle du jeu principale
        :return:
        """
        while self.__continuer:
            time.sleep(self.__tps_att * 0.001)
            try:
                self.__new_tick()
            except tk.TclError:
                # on ignore le tick si on essaye de deplacer un object qui n'existe plus
                pass

    def __new_tick(self) -> None:
        """
        Fonction appele a chaque tick
        """
        self.__deplac_ennemis()
        for entity in self.__lst_entites:
            # on recupere et definit tous les positions
            distance = entity.get_deplacement()
            position = entity.get_position()
            position_etendue = entity.get_position_etendue()
            nouvelle_position = position + distance
            # on enregistre les nouvelles positions dans les objects
            entity.set_position(pos=nouvelle_position)
            entity.set_position_etendue(position=position_etendue + distance)
            # on deplace les images
            entity.get_image().place(x=nouvelle_position.get_x(), y=nouvelle_position.get_y())

            # Reinitialisation du vecteur direction
            entity.changer_direction(vecteur2.Vect2())

        ennemis_restants = []
        # Appele de la fonction de test des collisions
        for i, ennemi in enumerate(self.__lst_entites[2:]):
            if self.colision_test(self.__missile, ennemi):
                ennemi.rm_img()
                self.__missile.changer_direction(vecteur2.Vect2(x=0, y=-1000))
                self.__score()
                # si on est a la position bonus
                # defaut : peut detecter les ennemis normaux comme 'bonus'
                if i == 2:
                    self.__i_bonus -= 1
            else:
                ennemis_restants.append(ennemi)

        blocs_restants = []
        for bloc in self.__lst_blocs:
            if self.colision_test(self.__missile, bloc):
                bloc.rm_img()
                self.__missile.changer_direction(vecteur2.Vect2(x=0, y=-1000))
                self.__score()
            else:
                blocs_restants.append(bloc)

        # on reactualise les listes avec les blocs et ennemis encore existants
        self.__lst_blocs = blocs_restants
        self.__lst_entites = self.__lst_entites[:2] + ennemis_restants

        self.__i_bonus += 1
        
    def colision_test(self, entity1, entity2):
        """
        Tests de collisions entre les coordonnées des entités

        Exemple du cote haut droit
        x = entity1, + = entity2
        x1, +1 --> position
        x2, +2 --> position + taille (position_entendue)

           +1-------
           |       |
        x1-|---    |
        |  ---|----+2
        ------x2

        Grace a deux arretes de chaque entite on peut tester si on a une collision

        Entrée:
            entity1: Entite
            entity2: Entite
        Sortie:
            Bool
        """
        
        # cote haut droit
        if entity1.get_position().get_x() <= entity2.get_position().get_x() <= entity1.get_position_etendue().get_x() \
            and entity1.get_position().get_y() <= entity2.get_position().get_y() <= entity1.get_position_etendue().get_y():
            return True
        # cote bas droit
        elif entity2.get_position().get_x() <= entity1.get_position().get_x() <= entity2.get_position_etendue().get_x() \
            and entity2.get_position().get_y() <= entity1.get_position().get_y() <= entity2.get_position_etendue().get_y():
            return True
        # cote haut gauche
        elif entity1.get_position().get_x() <= entity2.get_position().get_x() <= entity1.get_position_etendue().get_x() \
            and entity1.get_position().get_y() <= entity2.get_position_etendue().get_y() <= entity1.get_position_etendue().get_y():
            return True
        # cote bas gauche
        elif entity1.get_position().get_x() <= entity2.get_position().get_x() <= entity1.get_position_etendue().get_x() \
                and entity1.get_position().get_y() <= entity2.get_position_etendue().get_y() <= entity1.get_position_etendue().get_y():
            return True
        # pas de colision
        else:
             return False

          
