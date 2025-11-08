import json
from Calendrier import Calendrier


class Eleve:
    with open("./ressources/calendrier_eleves.json", "r", encoding="utf-8") as file:
        calendrier = json.load(file)

    def __init__(self, nom: str):
        self.nom = nom
        self.calendrier = Calendrier(Eleve.calendrier[nom])
