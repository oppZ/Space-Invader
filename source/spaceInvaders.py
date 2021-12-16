from tkinter import *

class fenetre():
    def __init__(self) -> None:
        self.__f = Tk()
        self.__f.title("Les envahisseurs de l'espace.html")

        self.__ecran = Canvas(self.__f)
        self.__ecran.pack()

        self.__quitter = Button(self.__f, text = "Quitter", command = self.__f.destroy)
        self.__quitter.pack()

        self.__f.mainloop()

fenetre()
