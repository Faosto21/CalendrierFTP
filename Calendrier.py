from __future__ import annotations
from typing import List
from datetime import datetime, timedelta, date


class Calendrier(dict):
    """
    Classe qui hérite de la classe de dict.
    Les clés primaires sont des dates sous format ISO et la valeur est un dictionnaire.
    Dont les deux clés sont Disponibilité et Caractéristiques
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def DisponibilitesCommunes(listes_eleves: List["Eleve"], professeur: "Professeur"):
        """
        Fonction qui renvoie la liste des disponibilités communes entre une liste d'élèves et un professeur
        entre le lendemain de la date actuelle et 8 semaines plus tard.
        La renvoie sous la forme d'une liste des horaires de disponibilité en commun.

        """
        slots = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30)]

        date_dispo = date(2025, 11, 22)
        dispo_commune = []
        for _ in range(4):
            date_dispo += timedelta(
                days=1
            )  # On commence à chercher à partir du lendemain
            if date_dispo.weekday() >= 5:  # Si c'est samedi ou dimanche on passe
                continue
            for slot in slots:
                creneau = date_dispo.strftime("%Y-%m-%d") + " " + slot
                if (
                    creneau in professeur.calendrier
                    and not professeur.calendrier[creneau]["Disponibilité"]
                ):
                    continue
                dispo = True
                for eleve in listes_eleves:
                    if (
                        creneau in eleve.calendrier
                        and not eleve.calendrier[creneau]["Disponibilité"]
                    ):
                        dispo = False
                        break
                if dispo:
                    dispo_commune.append(datetime.fromisoformat(creneau))
        return dispo_commune
