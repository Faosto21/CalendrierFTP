import datetime
import json

from Calendrier import Calendrier


class Salle:
    with open("ressources/calendrier_salles.json", encoding="utf-8") as file:
        calendrier = json.load(file)
        
    def __init__(self, nom):
        self.nom = nom
        self.capacite = Salle.calendrier[nom]["2025-11-24 08:00"]["Capacité"]
        self.caracteristiques = Salle.calendrier[nom]["2025-11-24 08:00"]["Caractéristique"]
        self.calendrier = Calendrier(Salle.calendrier[nom])

    def __repr__(self):
        return self.nom

    def __str__(self):
        return f"Salle(nom={self.nom}, capacite={self.capacite}, caracteristiques={self.caracteristiques})"

if __name__ == "__main__":
    salle = Salle("Salle1")
    print(salle.nom)
    print(salle.capacite)
    print(salle.caracteristiques)
    print(salle.calendrier)