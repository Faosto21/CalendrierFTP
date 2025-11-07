from Cours import Cours
import datetime


def CreneauxCommuns(DisponibilitesCommunes: list, cours: Cours):
    """
    Retourne les créneaux communs parmi les disponibilité communes qui ont la bonne durée.
    Les créneaux communs sont sous forme de tuple de longueur 2 ayant commme première valeur
    le début du créneau et en deuxième valeur la fin du créneau.
    Ex : On suppose les disponibilites communes sont celles-ci [09,10,11,13,17] et on
    suppose les creneaux sont en heures et le cours dure 2h.
    CreneauxCommuns([09,10,11,13,17], cours) = [(09,10), (10,11)]
    """
    taille_creneau = 0.5  # 0.5 heure = 30 minutes
    nb_creneau = (
        cours.duree / taille_creneau
    )  # nombre de créneaux de 30 minutes pris par le cours (qui est en heures)
    creneaux = [
        (DisponibilitesCommunes[i + nb_creneau], DisponibilitesCommunes[i])
        for i in range(len(DisponibilitesCommunes) - nb_creneau)
        if datetime.timedelta(
            DisponibilitesCommunes[i + nb_creneau], DisponibilitesCommunes[i]
        )
        + 1
        == cours.duree
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
