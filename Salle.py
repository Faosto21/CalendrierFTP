from Calendrier import Calendrier


class Salle:
    def __init__(self):
        self.nom: str
        self.capacite: int
        self.caracteristiques: list
        self.calendrier: Calendrier  # la disponibilité sera gérée via le calendrier

    def __str__(self):
        return f"Salle(nom={self.nom}, capacite={self.capacite}, caracteristiques={self.caracteristiques})"
