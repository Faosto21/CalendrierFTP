import tkinter as tk
import json

from Calendrier import Calendrier
from Eleve import Eleve
from Professeur import Professeur


class ApplicationCalendrier:
    """
    Classe de l'application du calendrier
    """


if __name__ == "__main__":
    root = tk.Tk()
    Faosto = Eleve(1, "Faosto")
    Phoebus = Eleve(2, "Phoebus")
    Thomas = Eleve(3, "Thomas")

    Gledel = Professeur(1, "Gledel")
    print(Calendrier.DisponibilitesCommunes([Faosto, Phoebus, Thomas], Gledel))
