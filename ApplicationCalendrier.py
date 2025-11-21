from tkinter import *
import tkinter.ttk as ttk
from tksheet import Sheet
import json
from datetime import datetime, timedelta, date

from Calendrier import Calendrier
from Eleve import Eleve
from Professeur import Professeur
from Salle import Salle
from Cours import Cours


class ApplicationCalendrier:
    """
    Classe de l'application du calendrier
    """

    slots = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30)]

    def __init__(self, fenetre, date=datetime.today()):
        self.fenetre = fenetre
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitter_application)
        self.fenetre.title("Planning")
        self.liste_eleves = list(map(Eleve, Eleve.calendrier.keys()))
        self.liste_professeurs = list(map(Professeur, Professeur.calendrier.keys()))
        self.liste_salles = list(map(Salle, Salle.calendrier.keys()))
        self.personnes = {
            **{e.nom: e for e in self.liste_eleves},
            **{p.nom: p for p in self.liste_professeurs},
            **{s.nom: s for s in self.liste_salles}
        }
        self.date = date
        self.setup_boutons_tableau()

    # Fonctions

    def lundi(self):
        """Renvoie le lundi de la semaine de la date donnée"""
        return self.date - timedelta(days=self.date.weekday())

    # JOUR_MIN = date.today() - timedelta(
    #     days=62
    # )  # On peut voir au max deux mois dans le passé
    # JOUR_MAX = date.today() + timedelta(
    #     days=93
    # )  # On peut voir au max 3 mois dans le futur
    # SEMAINE_MIN = lundi(JOUR_MIN)
    # SEMAINE_MAX = lundi(JOUR_MAX)

    def remplir_planning(self, personne: str):
        """Remplit le tableau pour eleve sur la semaine courante (Lun→Ven)"""
        # Vider le tableau
        dico = self.personnes[personne].calendrier
        for r in range(len(ApplicationCalendrier.slots)):
            for c in range(5):
                self.sheet.set_cell_data(r, c, "")
        jours = [self.lundi() + timedelta(days=i) for i in range(5)]

        # Remplir le tableau
        for r, slot in enumerate(ApplicationCalendrier.slots):
            for c, d in enumerate(jours):
                key = f"{d.strftime('%Y-%m-%d')} {slot}"
                if key in dico and not dico[key]["Disponibilité"]:
                    if not dico[key]["Caractéristique"] == {}:
                        self.sheet.set_cell_data(r, c, dico[key]["Caractéristique"])
                    else:
                        self.sheet.set_cell_data(r, c, "Occupé")

        self.sheet.refresh()

    def gestion_semaine(self):
        """Met à jour les en-têtes et désactive les boutons aux bornes"""
        jours = [self.lundi() + timedelta(days=i) for i in range(5)]
        label_jours_semaine = ["Lun", "Mar", "Mer", "Jeu", "Ven"]
        headers = [
            f"{label_jours_semaine[i]} {jours[i].strftime('%d/%m')}" for i in range(5)
        ]

        self.sheet.headers(headers)
        self.sheet.refresh()

        week_end = self.lundi() + timedelta(days=6)
        self.label_semaine.config(
            text=f"Semaine du {self.lundi().strftime('%d/%m/%Y')} au {week_end.strftime('%d/%m/%Y')}"
        )
        if self.personne_var.get():
            self.remplir_planning(self.personne_var.get())

    def changer_personne(self, event=None):
        """Met à jour l'emploi du temps quand on change de personne"""
        if self.personne_var.get():
            self.remplir_planning(self.personne_var.get())

    def clique_precedent(self):
        """Passe à la semaine précédente"""
        self.date -= timedelta(days=7)
        self.gestion_semaine()

    def clique_suivant(self):
        """Passe à la semaine suivante"""
        self.date += timedelta(days=7)
        self.gestion_semaine()

    def setup_boutons_tableau(self):
        """
        Création des boutons et du tableau
        """
        self.personne_var = StringVar(
            value=(self.liste_eleves[0].nom if self.liste_eleves else "")
        )
        # Barre de navigation
        barre = Frame(self.fenetre)
        barre.pack(fill="x")

        btn_precedent = Button(barre, text="Semaine précédente")
        self.label_semaine = Label(barre, text="", font=("Helvetica", 10))
        btn_suivant = Button(barre, text="Semaine suivante")
        btn_ajout_cours = Button(barre, text="Ajouter un cours")

        btn_precedent.pack(side="left", padx=6)
        self.label_semaine.pack(side="left", padx=10)
        btn_suivant.pack(side="left", padx=6)
        btn_ajout_cours.pack(side="right", padx=6)

        Label(barre, text="  Personne :").pack(side="left")
        listes_personnes = [eleve.nom for eleve in self.liste_eleves] + [
            professeur.nom for professeur in self.liste_professeurs
        ] + [salle.nom for salle in self.liste_salles]
        menu_personne = ttk.Combobox(
            barre,
            textvariable=self.personne_var,
            values=listes_personnes,
            state="readonly",
            width=12,
        )
        menu_personne.pack(side="left", padx=6)
        self.sheet = Sheet(
            self.fenetre,
            data=[[""] * 5 for _ in ApplicationCalendrier.slots],
            headers=["Lun", "Mar", "Mer", "Jeu", "Ven"],
            row_index=ApplicationCalendrier.slots,
        )

        self.sheet.set_all_column_widths(200)
        self.sheet.set_row_heights([25] * len(ApplicationCalendrier.slots))
        self.sheet.pack(expand=True, fill="both")

        btn_precedent.config(command=self.clique_precedent)
        btn_suivant.config(command=self.clique_suivant)
        btn_ajout_cours.config(
            command=lambda: Cours.bouton_ajouter_cours(
                self.liste_eleves, self.liste_professeurs, self.liste_salles
            )
        )
        menu_personne.bind("<<ComboboxSelected>>", self.changer_personne)
        self.gestion_semaine()

    def quitter_application(self):
        """
        Sauvegarder les dictionnaires modifiés dans leurs json associés
        """
        calendrier_eleve = {eleve.nom: eleve.calendrier for eleve in self.liste_eleves}
        with open("./ressources/calendrier_eleves.json", "w", encoding="utf-8") as file:
            json.dump(calendrier_eleve, file, ensure_ascii=False, indent=4)
        calendrier_prof = {prof.nom: prof.calendrier for prof in self.liste_professeurs}
        with open("./ressources/calendrier_profs.json", "w", encoding="utf-8") as file:
            json.dump(calendrier_prof, file, ensure_ascii=False, indent=4)
        calendrier_salles = {salle.nom: salle.calendrier for salle in self.liste_salles}
        with open("./ressources/calendrier_salles.json", "w", encoding="utf-8") as file:
            json.dump(calendrier_salles, file, ensure_ascii=False, indent=4)
        self.fenetre.destroy()


if __name__ == "__main__":
    fenetre = Tk()
    app = ApplicationCalendrier(fenetre)
    fenetre.geometry("1280x720")
    fenetre.mainloop()
