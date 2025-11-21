from datetime import timedelta, datetime

from Cours import Cours
from Calendrier import Calendrier
from Salle import Salle


def CreneauxCommuns(DisponibilitesCommunes: list, cours: Cours):
    """
    Retourne les créneaux communs parmi les disponibilité communes qui ont la bonne durée.
    Les créneaux communs sont renvoyés avec seulement l'heure de début du créneau
    Ex : On suppose les disponibilites communes sont celles-ci [09,10,11,13,17] et on
    suppose les creneaux sont en heures et le cours dure 2h.
    CreneauxCommuns([09,10,11,13,17], cours) = [9,10]
    """
    taille_creneau = timedelta(minutes=30)  # 0.5 heure = 30 minutes
    duree = cours.duree
    nb_creneau = int(
        duree / taille_creneau
        ) # nombre de créneaux de 30 minutes pris par le cours (qui est en heures)
    def creneaux_consecutifs_disponibles(debut):
        """
        Vérifie si tout les créneaux depuis début jusqu'à début + nb_creneau sont disponibles donc dans DisponibiliteCommunes
        Version temporaire mais si on garde la même idée il faudrait que DisponibilitesCommunes soit un set pour avoir un test d'appartenance plus rapide
        """
        for i in range(1, nb_creneau):
            if not (debut + i * taille_creneau in DisponibilitesCommunes):
                return False
        return True

    creneaux = [
        [disponibilite + i * taille_creneau for i in range(nb_creneau)]
        for disponibilite in DisponibilitesCommunes
        if creneaux_consecutifs_disponibles(disponibilite)
    ]
    return creneaux


def TrouverSalle(liste_salles: list[Salle], liste_cours: list[Cours]):
    """
    Trouve une salle disponible pour une date commune avec une capacité suffisante pour accueillir tous les invités
    ainsi que le matériel nécessaire pour le cours.
    Retourne un dictionnaire avec en clé les cours et en valeur les salles disponibles pour chaque cours.
    Par exemple : {cours1 : [(salle1, [9, 930]), (salle2, [10, 1030])], cours2 : [(salle2, [10, 1030]), (salle3, [11, 1130])]}
    """
    # on créé un dictionnaire pour stocker les salles dispo selon les cours
    dict_salles = {}  # cours en clé et les salles en valeurs
    for cours in liste_cours:
        dict_salles[cours] = []
        dispo = Calendrier.DisponibilitesCommunes(cours.eleves, cours.professeur)
        creneaux_communs = CreneauxCommuns(dispo, cours)
        for salle in liste_salles:
            # on vérifie que la salle peut accueillir le cours (capacité et matériel nécessaire)
            # si la salle n'a pas la capacité ou le matériel requis, on passe à la suivante
            if salle.capacite < len(cours.eleves):
                continue
            check = True
            for besoin, booleen in cours.materiel.items():
                if booleen and not salle.caracteristiques[besoin]:
                    check = False
                    break
            # dict_salles[cours] a été initialisé plus haut ; on ajoute les (salle, creneau) valides
            if not check:
                continue
            for creneau in creneaux_communs:
                # on garde les créneaux communs (prof/élèves) qui sont aussi disponibles dans le calendrier de cette salle
                if all(
                    salle.calendrier[creneau[i].strftime("%Y-%m-%d %H:%M")]["Disponibilité"] 
                    for i in range(len(creneau)) if creneau[i].strftime("%Y-%m-%d %H:%M") in salle.calendrier
                ):
                    dict_salles[cours].append((salle, creneau))

    def ChoisirSalle(dict_salles: dict):
        """
        Choisit pour chaque cours la première salle/creneau candidat qui ne crée pas de conflit
        (même salle/creneau déjà prise, élèves pris sur ce créneau, ou professeur pris sur ce créneau).
        Retourne un nouveau dict mapping cours -> (salle, creneau) ou None si aucun choix possible.
        """
        choix = {}

        # structures pour détecter les conflits rapidement
        prises_salles_creneaux = set()  # set of (salle, tuple(creneau))
        prises_eleves_par_instant = {}  # instant -> set(eleves)
        prises_profs_par_instant = {}  # instant -> set(profs)

        for cours, candidates in dict_salles.items():
            chosen = None
            for salle, creneau in candidates:
                # normaliser le creneau pour le mettre dans des sets (tuple d'instants)
                creneau_key = tuple(creneau)
                conflict = False

                # 1) Vérifier si (salle, creneau) est déjà pris
                if (salle, creneau_key) in prises_salles_creneaux:
                    conflict = True

                # 2) Vérifier conflit élèves et profs : aucun élève du cours ou le prof du cours ne doit être pris sur un des instants
                if not conflict:
                    eleves_set = set(cours.eleves)
                    for instant in creneau_key:
                        if not prises_eleves_par_instant.get(instant, set()).isdisjoint(
                            eleves_set
                        ) or cours.professeur in prises_profs_par_instant.get(
                            instant, set()
                        ):
                            conflict = True
                            break

                if not conflict:
                    # on choisit cette salle/creneau
                    chosen = (salle, creneau)
                    prises_salles_creneaux.add((salle, creneau_key))
                    for instant in creneau_key:
                        prises_eleves_par_instant.setdefault(instant, set()).update(
                            eleves_set
                        )
                        prises_profs_par_instant.setdefault(instant, set()).add(
                            cours.professeur
                        )
                    break

            choix[cours] = chosen

        return choix

    resp = ChoisirSalle(dict_salles)
    return resp

if __name__ == "__main__":
    import json
    from Professeur import Professeur
    from Eleve import Eleve
    eleves = ["Alice", "Bob", "Charlie"]
    
    cal_eleve_link = "ressources/calendrier_eleves.json"
    cal_profs_link = "ressources/calendrier_profs.json"
    cal_salles_link = "ressources/calendrier_salles.json"
    with open(cal_eleve_link, "r", encoding="utf-8") as f:
        calendrier_eleves = Calendrier(json.load(f))
    with open(cal_profs_link, "r", encoding="utf-8") as f:
        calendrier_profs = Calendrier(json.load(f))
    with open(cal_salles_link, "r", encoding="utf-8") as f:
        calendrier_salles = Calendrier(json.load(f))
    eleves1 = [
        Eleve("Faosto"),
        Eleve("Phoebus")
    ]
    eleves2 = [
        Eleve("Faosto"),
        Eleve("Thomas")
    ]
    professeur = Professeur("Gledel")
    besoins_materiel1 = {"Projecteur": True, "Ordinateurs": False}
    besoins_materiel2 = {"Projecteur": True, "Ordinateurs": True}
    cours1 = Cours(nom ="Maths", eleves = eleves1, professeur=professeur, materiel=besoins_materiel1, duree=timedelta(hours=1))
    cours2 = Cours(nom ="Physique", eleves = eleves2, professeur=professeur, materiel=besoins_materiel2, duree=timedelta(hours=1))
    liste_cours = [cours1, cours2]
    liste_salles = [Salle(salle) for salle in calendrier_salles.keys()]
    salle_choisie = TrouverSalle(liste_salles=liste_salles, liste_cours=liste_cours)
    print(f"Salles choisies pour les cours : {salle_choisie}")