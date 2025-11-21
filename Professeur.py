import json

from Calendrier import Calendrier


class Professeur:
    with open("./ressources/calendrier_profs.json", "r", encoding="utf-8") as file:
        calendrier = json.load(file)

    def __init__(self, nom: str):
        self.nom = nom
        self.calendrier = Calendrier(Professeur.calendrier[nom])

    def __repr__(self):
        return f"Professeur : {self.nom}"

if __name__ == "__main__":
    prof = Professeur("Maria")
    print(f"Calendrier du professeur {prof.nom} : {prof.calendrier}")