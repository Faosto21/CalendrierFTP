from datetime import timedelta
import json
from tkinter import *
import tkinter.ttk as ttk

from Eleve import Eleve
from Professeur import Professeur
from Calendrier import Calendrier
from Salle import Salle


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

    def __repr__(self):
        return self.nom

    def __str__(self):
        return f"Cours(nom={self.nom}, professeur={self.professeur}, eleves={self.eleves}, duree={self.duree}, materiel={self.materiel})"

    @staticmethod
    def rentrer_cours(resultats):
        for cours, (salle, creneaux) in resultats.items():
            for creneau in creneaux:
                cours.professeur.calendrier[creneau.strftime("%Y-%m-%d %H:%M")] = {
                    "Disponibilité": False,
                    "Caractéristique": cours.nom,
                }
                salle.calendrier[creneau.strftime("%Y-%m-%d %H:%M")] = False
                for eleve in cours.eleves:
                    eleve.calendrier[creneau.strftime("%Y-%m-%d %H:%M")] = {
                        "Disponibilité": False,
                        "Caractéristique": cours.nom,
                    }
    @staticmethod
    def rentrer_cours(resultats):
        for cours, val in resultats.items(): # on n'itere pas sur (salle, creneaux) car peut être None
            if not val:
                continue
            salle, creneaux = val
            for creneau in creneaux:
                key = creneau.strftime("%Y-%m-%d %H:%M")
                # marque professeur occupé
                cours.professeur.calendrier[key] = {
                    "Disponibilité": False,
                    "Caractéristique": cours.nom,
                }
                # marque salle occupée (dict structuré)
                salle.calendrier[key] = {
                    "Disponibilité": False,
                    "Caractéristique": cours.nom,
                    "Capacité": getattr(salle, "capacite", None),
                }
                # marque élèves occupés
                for eleve in cours.eleves:
                    eleve.calendrier[key] = {
                        "Disponibilité": False,
                        "Caractéristique": cours.nom,
                    }

    @staticmethod
    def afficher_choix(resultats: dict):
        win = Toplevel()
        win.title("Resultats recherche créneaux/salles")
        approved = {"value": False}
        ttk.Label(win, text="Résultats trouvés :", font=("Arial", 14, "bold")).pack(
            pady=10
        )

        frame = ttk.Frame(win)
        frame.pack(pady=5)

        for cours, val in resultats.items():
            if not val:
                ttk.Label(
                    frame,
                    text=f"{cours.nom} → Aucun créneau disponible",
                    font=("Arial", 12, "italic"),
                ).pack(anchor="w")
                continue
            salle, creneau_list = val
            start = creneau_list[0].strftime("%Y-%m-%d %H:%M")
            end = (creneau_list[-1] + timedelta(minutes=30)).strftime(
                "%Y-%m-%d %H:%M"
            )
            text = f"{cours.nom} → Salle: {getattr(salle, 'nom', repr(salle))}, Heure de début: {start}, Heure de fin: {end}"
            ttk.Label(frame, text=text, font=("Arial", 12)).pack(anchor="w")

        def approve_and_close():
            approved["value"] = True
            win.destroy()

        def reject_and_close():
            win.destroy()

        ttk.Button(win, text="Approuver", command=approve_and_close).pack(pady=20)
        ttk.Button(win, text="Annuler", command=reject_and_close).pack(pady=20)

        win.grab_set()
        win.wait_window()

        return approved["value"]

    @staticmethod
    def bouton_ajouter_cours(
        liste_eleves: list[Eleve],
        liste_professeurs: list[Professeur],
        liste_salles=list[Salle],
    ):

        root = Tk()
        root.title("Ajout d'un cours")
        prof_dict = {prof.nom: prof for prof in liste_professeurs}
        liste_cours = []

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
            barre, text="Ordinateurs", variable=ordi_var, onvalue=True, offvalue=False
        ).pack(side="left")
        projecteur_var = BooleanVar(barre)
        Checkbutton(
            barre,
            text="Projecteur",
            variable=projecteur_var,
            onvalue=True,
            offvalue=False,
        ).pack(side="left")
        listbox = Listbox(root, height=10, width=40)

        def refresh_listbox():
            listbox.delete(0, END)
            for cours in liste_cours:
                listbox.insert(END, cours.nom)

        def ajouter_cours():
            nouveau_cours = Cours(
                nom_entry.get(),
                prof_dict[professeur_var.get()],
                eleves_participants(),
                mapping_duree[duree_var.get()],
                {"Ordinateurs": ordi_var.get(), "Projecteur": projecteur_var.get()},
            )
            liste_cours.append(nouveau_cours)
            refresh_listbox()

        listbox.pack(pady=10)
        bouton_ajouter_cours = Button(
            root,
            text="Ajouter cours",
            command=ajouter_cours,
        )
        bouton_ajouter_cours.pack()

        def chercher_creneaux():
            from TrouverSalle import TrouverSalle

            resultats = TrouverSalle(liste_salles, liste_cours)

            approved = Cours.afficher_choix(resultats)

            if approved:
                Cours.rentrer_cours(resultats)

        bouton_chercher_cours = Button(
            root,
            text="Chercher créneaux",
            command=chercher_creneaux,
        )
        bouton_chercher_cours.pack()

        root.geometry("1280x720")
        root.mainloop()
