import json

from Calendrier import Calendrier


class Professeur:
    with open("./ressources/calendrier_profs.json", "r", encoding="utf-8") as file:
        calendrier = json.load(file)

    def __init__(self, nom: str):
        self.nom = nom
        self.calendrier = Calendrier(Professeur.calendrier[nom])
