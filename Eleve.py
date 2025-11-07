import json
from Calendrier import Calendrier


class Eleve:
    with open("./ressources/calendrier_eleves.json", "r", encoding="utf-8") as file:
        calendrier = json.load(file)

    def __init__(self, identifiant: int, nom: str):
        self.identifiant = identifiant
        self.nom = nom
        self.calendrier = Calendrier(Eleve.calendrier[str(identifiant)])
