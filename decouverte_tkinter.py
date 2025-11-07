# type: ignore # juste pour enlever l'avertissement 

# Import des modules
from tkinter import *
import webbrowser

def open_usmb_website():
    webbrowser.open_new("https://www.univ-smb.fr/")

# Création de la fenêtre principale
window = Tk()

# Personnalisation de la fenêtre
window.title("Découverte de Tkinter") # titre de la fenetre
window.geometry("1080x720") # taille de la fenetre
window.minsize(480, 360) # taille minimale autorisée
#window.iconbitmap("programme.ico") # icone de la fenetre
window.config(background="#2c3e50") # couleur de fond de la fenetre
#window.config(background="white") # fond blanc

# Creation d'un cadre (frame)
frame = Frame(window, bg="#2c3e50")#, bd=1, relief = SUNKEN) # bd = border (bordure)

# Ajouter un texte
# creation du label
label_title = Label(frame, text = "Bienvenue dans Tkinter", font = ("Helvetica", 40), bg = "#2c3e50", fg = "white") 
label_title.pack(expand = YES) # affichage du label, expand permet de centrer le texte

label_subtitle = Label(frame, text = "Ceci est un sous-tire", font = ("Helvetica", 25), bg = "#2c3e50", fg = "white") 
label_subtitle.pack(expand = YES) # affichage du label, expand permet de centrer le texte

# Ajout d'un bouton
USMB_button = Button(frame, text = "Site USMB", font = ("Helvetica", 25), bg = "white", fg = "#2c3e50", command=open_usmb_website)
USMB_button.pack(pady = 25, fill = X, ) # decalage vertical (pady) et remplissage horizontal (fill = X)

# ajouter le frame a la fenetre
frame.pack(expand = YES)

# Afficher la fenetre
window.mainloop()