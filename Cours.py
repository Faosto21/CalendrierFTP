from datetime import timedelta
from tkinter import *
import tkinter.ttk as ttk

from Eleve import Eleve
from Professeur import Professeur
from Calendrier import Calendrier


class Cours:
    def __init__(
        self,
        nom: str,
        professeur: Professeur,
        eleves: list[Eleve],
        duree: timedelta,
        materiel: dict,
    ):
        self.nom = nom
        self.eleves = eleves
        self.professeur = professeur
        self.salle = None
        self.duree = duree
        self.materiel = materiel

    def __str__(self):
        return f"Cours(nom={self.nom}, professeur={self.professeur}, eleves={self.eleves}, duree={self.duree}, materiel={self.materiel})"

    def placer_cours(self):
        # Juste pour tester pour l'instant
        print(self)

    @staticmethod
    def bouton_ajouter_cours(
        liste_eleves: list[Eleve], liste_professeurs: list[Professeur]
    ):
        root = Tk()
        root.title("Ajout d'un cours")

        nom_label = Label(root, text="Nom du cours :")
        nom_entry = Entry(root)
        nom_label.pack()
        nom_entry.pack()

        eleves_label = Label(root, text="Elèves participant au cours")
        eleves_label.pack()
        vars = {}
        for eleve in liste_eleves:
            vars[eleve] = BooleanVar(root)
            Checkbutton(
                root, text=eleve.nom, variable=vars[eleve], onvalue=True, offvalue=False
            ).pack()

        def eleves_participants():
            participants = [
                eleve for eleve, participation in vars.items() if participation.get()
            ]
            return participants

        barre = Frame(root)
        barre.pack(fill="x")
        professeur_label = Label(barre, text="Professeur :").pack(side="left")
        professeur_var = StringVar(barre)
        menu_professeur = ttk.Combobox(
            barre,
            textvariable=professeur_var,
            values=[professeur.nom for professeur in liste_professeurs],
            state="readonly",
            width=12,
        )
        menu_professeur.pack(side="left", padx=6)

        mapping_duree = {
            "1h": timedelta(hours=1),
            "1h30": timedelta(hours=1, minutes=30),
            "2h": timedelta(hours=2),
        }
        duree_label = Label(barre, text="Durée :").pack(side="left")
        duree_var = StringVar(barre)
        menu_duree = ttk.Combobox(
            barre,
            textvariable=duree_var,
            values=[duree for duree in mapping_duree],
            state="readonly",
            width=12,
        )
        menu_duree.pack(side="left", padx=6)

        ordi_var = BooleanVar(barre)
        Checkbutton(
            barre, text="Ordinateur", variable=ordi_var, onvalue=True, offvalue=False
        ).pack(side="left")
        retro_var = BooleanVar(barre)
        Checkbutton(
            barre,
            text="Rétroprojecteur",
            variable=retro_var,
            onvalue=True,
            offvalue=False,
        ).pack(side="left")
        bouton_creer_cours = Button(
            root,
            text="Chercher créneau",
            command=lambda: Cours(
                nom_entry.get(),
                Professeur(professeur_var.get()),
                eleves_participants(),
                mapping_duree[duree_var.get()],
                {"Ordinateur": ordi_var.get(), "Rétroprojecteur": retro_var.get()},
            ).placer_cours(),
        )
        bouton_creer_cours.pack()
        # A finir en rajoutant des widgets pour le matériel

        root.geometry("1280x720")
        root.mainloop()
