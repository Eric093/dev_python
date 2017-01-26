 
from tkinter import *

import messagebox 

root = Tk()   ## Fenêtre principale 

def Affiche(): messagebox.showinfo("Exemple d'un Menu Tkinter") 
def About(): messagebox.showinfo("A propos", "Version 1.0") 

mainmenu = Menu(root)  ## Barre de menu 
menuExample = Menu(mainmenu)  ## Menu fils menuExample 
menuExample.add_command(label="Affiche", command=Affiche)  ## Ajout d'une option au menu fils menuFile 
menuExample.add_command(label="Quitter", command=root.quit) 

menuHelp = Menu(mainmenu) ## Menu Fils 
menuHelp.add_command(label="A propos", command=About) 

mainmenu.add_cascade(label = "Exemple", menu=menuExample) 
mainmenu.add_cascade(label = "Aide", menu=menuHelp) 

root.config(menu = mainmenu) 

root.mainloop()