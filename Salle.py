import json

from Calendrier import Calendrier


class Salle:
    with open("ressources/PlanningSalles.json", encoding="utf-8") as file:
        planning_salles = json.load(file)

    def __init__(self, nom):
        self.nom = nom
        self.capacite = Salle.planning_salles[nom]["Capacité"]
        self.caracteristiques = Salle.planning_salles[nom]["Caractéristiques"]
        self.calendrier = Salle.planning_salles[nom]["Disponibilité"]

    def __repr__(self):
        return self.nom

    def __str__(self):
        return f"Salle(nom={self.nom}, capacite={self.capacite}, caracteristiques={self.caracteristiques})"
