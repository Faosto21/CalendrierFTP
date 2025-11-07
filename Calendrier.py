from __future__ import annotations
from typing import List


class Calendrier(dict):
    """
    Classe qui hérite de la classe de base dict.
    Les clés primaires sont des dates sous format iso et la valeur est un dictionnaire.
    Dont les deux clés sont disponibilie
    """

    def __init_subclass__(cls):
        return super().__init_subclass__()

    @staticmethod
    def DisponibilitesCommunes(listes_eleves: List["Eleve"], professeur: "Professeur"):
        """
        Fonction qui renvoie la liste des disponibilités communes entre une liste d'élèves et un professeur
        La renvoie sous la forme d'une liste des horaires de disponibilité en commun
        """
        dispo_commune = Calendrier()
        for date in professeur.calendrier:
            dispo = professeur.calendrier[date]["Disponibilité"]
            dispo_commune[date] = dispo
            if dispo:
                for eleve in listes_eleves:
                    if not eleve.calendrier[date]["Disponibilité"]:
                        dispo_commune[date] = False
                        break
        return [date for date in dispo_commune if dispo_commune[date]]
