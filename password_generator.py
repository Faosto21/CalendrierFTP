# type: ignore # juste pour enlever l'avertissement 

from tkinter import *
from turtle import st
import string
from random import randint, choice

def generate_password():
    password_min = 6
    password_max = 12
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(choice(all_chars) for x in range(randint(password_min, password_max)))
                       
    password_entry.delete(0, END)  # Effacer le champ de saisie
    password_entry.insert(0, password)  # Insérer le mot de passe généré

# creation de la fenêtre principale
window = Tk()
window.title("Générateur de mot de passe")
window.geometry("1280x720")
window.config(background="#34495e")

# Créer la frame principale
frame = Frame(window, bg="#34495e")

# Création d'image
width = 512
height = 512
image = PhotoImage(file = "connexion.png").zoom(35).subsample(32) # redimensionner l'image
canvas = Canvas(frame, width=width, height=height, bg="#34495e", bd=0, highlightthickness=0)
canvas.create_image(width/2, height/2, image=image)
canvas.grid(row = 0, column = 0, sticky=W)  # placer l'image à gauche

# Créer une sous boite
right_frame = Frame(frame, bg="#34495e")


# Créer un titre
label_title = Label(right_frame, text="Mot de passe", font=("Helvetica", 20), bg="#34495e", fg="white")
label_title.pack()

# Créer un champ de saisie
password_entry = Entry(right_frame, font=("Helvetica", 20), bg="#34495e", fg="white")
password_entry.pack()

# Créer un bouton
generate_password_button = Button(right_frame, text="Générer", font=("Helvetica", 20), command = generate_password)
generate_password_button.pack(fill=X)

# on place la sous boite à droite de la frame principale
right_frame.grid(row = 0, column = 1, sticky = W)  

# Afficher la frame
frame.pack(expand=YES)

# Creation d'une barre de menu
menu_bar = Menu(window)

# Création d'un menu Fichier
file_menu = Menu(menu_bar, tearoff=0) 
file_menu.add_command(label="Nouveau", command=generate_password)
file_menu.add_command(label="Quitter", command=window.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

# Configuration de la fenêtre pour afficher la barre de menu
window.config(menu=menu_bar)

# Affichage
window.mainloop()