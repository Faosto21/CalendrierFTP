Elèves et profs : Tableau associatif (dico) avec comme première clé la date qui mène vers un autre dico avec comme clés dispo qui est un booléen (1 = disponible et 0 occupé ) et caractéristiques qui est une chaine ou un dico.
Salle : Dico avec comme première clé date qui mène vers un dico aec comme clé le numéro de la salle et qui mène vers le même dico que pour élève et prof.
Intersection pour les dispo s'obtient avec le ET logique de toutes les dispos des élèves/prof puis on check sur chaque dispo en commun les salles dispo.
