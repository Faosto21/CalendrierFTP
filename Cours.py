from datetime import timedelta


class Cours:
    def __init__(
        self, nom: str, professeur: str, eleves: list, duree: timedelta, materiel: dict
    ):
        self.nom = nom
        self.eleves = eleves
        self.professeur = professeur
        self.salle = None
        self.duree = duree
        self.materiel = materiel

    def __str__(self):
        return f"Cours(nom={self.nom}, professeur={self.professeur}, eleves={self.eleves}, duree={self.duree}, materiel={self.materiel})"
