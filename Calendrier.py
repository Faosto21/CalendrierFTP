from __future__ import annotations
from collections import defaultdict
from typing import List


class Calendrier(defaultdict):
    """
    Classe qui hérite de la classe de defaultdict.
    Les clés primaires sont des dates sous format iso et la valeur est un dictionnaire.
    Dont les deux clés sont Disponibilité et Caractéristiques
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            lambda: {"Disponibilité": True, "Caractéristiques": {}}, *args, **kwargs
        )

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
