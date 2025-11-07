from Cours import Cours
from datetime import timedelta, datetime


def CreneauxCommuns(DisponibilitesCommunes: list, cours: Cours):
    """
    Retourne les créneaux communs parmi les disponibilité communes qui ont la bonne durée.
    Les créneaux communs sont renvoyés avec seulement l'heure de début du créneau
    Ex : On suppose les disponibilites communes sont celles-ci [09,10,11,13,17] et on
    suppose les creneaux sont en heures et le cours dure 2h.
    CreneauxCommuns([09,10,11,13,17], cours) = [9,10]
    """
    taille_creneau = timedelta(minutes=30)  # 0.5 heure = 30 minutes
    nb_creneau = int(
        cours.duree / taille_creneau
    )  # nombre de créneaux de 30 minutes pris par le cours (qui est en heures)

    def creneaux_consecutifs_disponibles(debut):
        """
        Vérifie si tout les créneaux depuis début jusqu'à début + nb_creneau sont disponibles donc dans DisponibiliteCommunes
        """
        for i in range(1, nb_creneau):
            if not (debut + i * taille_creneau in DisponibilitesCommunes):
                return False
        return True

    creneaux = [
        disponibilite
        for disponibilite in DisponibilitesCommunes
        if creneaux_consecutifs_disponibles(disponibilite)
    ]
    return creneaux


def TrouverSalle(
    CalendrierSalles: dict, DisponibilitesCommunes: list[str], ListeCours: list[Cours]
):
    """
    Trouve une salle disponible pour une date commune avec une capacité suffisante pour accueillir tous les invités
    ainsi que le matériel nécessaire pour le cours. Renvoie le planning des salles modifié.
    """
    # on créé un dictionnaire pour stocker les salles dispo selon les cours
    dict_salles = {}  # cours en clé et les salles en valeurs
    for cours in ListeCours:
        dict_salles[cours] = []
        creneaux_communs = CreneauxCommuns(DisponibilitesCommunes, cours)
        for (
            salle
        ) in CalendrierSalles.keys():  # les clés du calendrier sont les objets salle
            # on vérifie que la salle peut accueillir le cours (capacité et matériel nécessaire)
            if not (
                all(
                    salle.caracteristiques.get(item, False) == besoin
                    for item, besoin in cours.materiel.items()
                )
                and salle.capacite < len(cours.eleves)
            ):
                break
            dict_salles[cours] = (
                []
            )  # on créé la clé "cours" et on initialise avec une liste vide qu'on remplira avec les salles valides
            for creneau in creneaux_communs:
                # on garde les créneaux communs aux créneaux communs (issues de calendrier_professeur et calendrier_eleves)
                # et aux créneaux disponibles dans le calendrier_salles
                for calendrier in CalendrierSalles.values():
                    # on vérifie que le début et la fin du créneau sont disponibles dans notre calendrier
                    if (
                        calendrier[creneau[0]]["Disponibilité"]
                        and calendrier[creneau[1]]["Disponibilité"]
                    ):
                        dict_salles[cours].append(salle)
    return dict_salles


if __name__ == "__main__":
    cours = Cours("Maths", "Maria", [], timedelta(hours=1), {})
    dispo_communes = [
        datetime(2025, 11, 7, 9, 0),
        datetime(2025, 11, 7, 9, 30),
        datetime(2025, 11, 7, 11, 0),
        datetime(2025, 11, 7, 12, 0),
        datetime(2025, 11, 7, 14, 30),
        datetime(2025, 11, 7, 15, 0),
    ]
    print(CreneauxCommuns(dispo_communes, cours))
