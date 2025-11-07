# type: ignore  # juste pour enlever l'avertissement

# Import des modules
from tkinter import *
import tkinter.ttk as ttk
from tksheet import Sheet
from datetime import datetime, date, timedelta
import json

# Chargement des dispo depuis le fichier JSON
chemin_json = "edt_eleves.json"  # ton fichier JSON

with open(chemin_json, "r", encoding="utf-8") as f:
    dispo = json.load(f)

# Fonction 
def lundi(d):
    """Renvoie le lundi de la semaine de la date donnée"""
    return d - timedelta(days=d.weekday())

JOUR_MIN = date(2025, 9, 1)
JOUR_MAX = date(2025, 12, 31)
SEMAINE_MIN = lundi(JOUR_MIN)
SEMAINE_MAX = lundi(JOUR_MAX)

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Planning")

# Noms des élèves
noms = sorted(dispo.keys())
personne_var = StringVar(value=(noms[0] if noms else ""))

# Barre de navigation
barre = Frame(fenetre)
barre.pack(fill="x")

btn_precedent = Button(barre, text="Semaine précédente")
label_semaine = Label(barre, text="", font=("Helvetica", 10))
btn_suivant = Button(barre, text="Semaine suivante")

btn_precedent.pack(side="left", padx=6)
label_semaine.pack(side="left", padx=10)
btn_suivant.pack(side="left", padx=6)

Label(barre, text="  Personne :").pack(side="left")
menu_personne = ttk.Combobox(barre, textvariable=personne_var, values=noms, state="readonly", width=12)
menu_personne.pack(side="left", padx=6)

# Création du tableau 
slots = [f"{h:02d}:{m:02d}" for h in range(8, 19) for m in (0, 30)]

sheet = Sheet(
    fenetre,
    data=[[""] * 5 for _ in slots],
    headers=["Lun", "Mar", "Mer", "Jeu", "Ven"],
    row_index=slots
)

sheet.set_all_column_widths(200)
sheet.set_row_heights([25] * len(slots))
sheet.pack(expand=True, fill="both")

# Gestion des semaines
semaine_courante = lundi(date(2025, 9, 1))

def remplir_planning_eleve(nom: str):
    """Remplit le tableau pour 'nom' sur la semaine courante (Lun→Ven)"""
    # Vider le tableau
    for r in range(len(slots)):
        for c in range(5):
            sheet.set_cell_data(r, c, "")

    dico = dispo.get(nom, {})
    jours = [semaine_courante + timedelta(days=i) for i in range(5)]

    # Remplir le tableau
    for r, slot in enumerate(slots):
        for c, d in enumerate(jours):
            key = f"{d.strftime('%Y-%m-%d')} {slot}"
            if dico.get(key) is True:
                sheet.set_cell_data(r, c, "Cours")

    sheet.refresh()

def gestion_semaine():
    """Met à jour les en-têtes et désactive les boutons aux bornes"""
    jours = [semaine_courante + timedelta(days=i) for i in range(5)]
    label_jours_semaine = ["Lun", "Mar", "Mer", "Jeu", "Ven"]
    headers = [f"{label_jours_semaine[i]} {jours[i].strftime('%d/%m')}" for i in range(5)]

    sheet.headers(headers)
    sheet.refresh()

    week_end = semaine_courante + timedelta(days=6)
    label_semaine.config(
        text=f"Semaine du {semaine_courante.strftime('%d/%m/%Y')} au {week_end.strftime('%d/%m/%Y')}"
    )

    btn_precedent.config(state=("disabled" if semaine_courante <= SEMAINE_MIN else "normal"))
    btn_suivant.config(state=("disabled" if semaine_courante >= SEMAINE_MAX else "normal"))

    if personne_var.get():
        remplir_planning_eleve(personne_var.get())

def changer_eleve(event=None):
    """Met à jour l'emploi du temps quand on change de personne"""
    if personne_var.get():
        remplir_planning_eleve(personne_var.get())

menu_personne.bind("<<ComboboxSelected>>", changer_eleve)

def clique_precedent():
    """Passe à la semaine précédente"""
    global semaine_courante
    semaine_precedente = semaine_courante - timedelta(days=7)
    if semaine_precedente >= SEMAINE_MIN:
        semaine_courante = semaine_precedente
        gestion_semaine()

def clique_suivant():
    """Passe à la semaine suivante"""
    global semaine_courante
    semaine_suivante = semaine_courante + timedelta(days=7)
    if semaine_suivante <= SEMAINE_MAX:
        semaine_courante = semaine_suivante
        gestion_semaine()

btn_precedent.config(command=clique_precedent)
btn_suivant.config(command=clique_suivant)

# Lancement du programme
gestion_semaine()

fenetre.geometry("1280x720")
fenetre.mainloop()
