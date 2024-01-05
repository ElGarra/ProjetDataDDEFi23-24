

# Livrable intermédiaire sur l'Extraction de Données d'Offres d'Emploi

1. **Contexte et Besoin Business :**
   L'extraction des données de l'API Pôle Emploi est une étape stratégique pour construire une base de données essentielle à la création d'un modèle de Machine Learning robuste. L'objectif ultime est de développer un modèle ML capable de prédire avec précision le secteur d'emploi d'une offre d'emploi. Ce modèle utilisera les données obtenues pour analyser les tendances et les modèles du marché du travail, permettant ainsi de catégoriser efficacement les nouvelles offres d'emploi dans leurs secteurs respectifs.

2. **Objectif de Modélisation :**
   L'objectif principal de ce projet est le développement d'un modèle d'apprentissage automatique qui peut prédire le secteur d'emploi pour une offre d'emploi. Cela implique le traitement et l'interprétation de diverses caractéristiques des offres d'emploi, y compris les titres, les descriptions et les compétences requises.

3. **Approche :**
   La méthodologie pour atteindre cet objectif comprend :
   - Extraction des Données : Utilisation de l'API Pôle Emploi pour collecter des offres d'emploi.
   - Nettoyage et Prétraitement des Données : Mise l'accent sur la standardisation, le traitement des données manquantes et le nettoyage des informations textuelles.
   - Ingénierie des Caractéristiques : Identification des caractéristiques clés des offres d'emploi pour le modèle ML.
   - Sélection et Formation du Modèle : Utilisation d'algorithmes appropriés pour former le modèle.
   - Évaluation : Évaluation de l'efficacité du modèle à l'aide de métriques pertinentes.
   - Déploiement : Application du modèle pour catégoriser de nouvelles offres d'emploi.

4. **Observations / Tests Initiaux :**
   Un examen initial des données révèle une riche variété d'attributs, les champs critiques étant le titre de l'emploi, la description et les compétences. Cependant, actuellement, nous sommes confrontés à une limitation avec la limite de taux de l'API, qui nous restreint à 20 requêtes avant de rencontrer un échec, résultant en un total de seulement 3150 offres d'emploi. Ce nombre est bien inférieur aux 30 000 offres souhaitées pour une formation et un test complets du modèle. Pour y remédier, il pourrait être nécessaire d'explorer des stratégies de collecte de données efficaces dans les contraintes de l'API ou de rechercher des sources alternatives pour augmenter notre jeu de données. La complexité des données textuelles nécessitera des techniques avancées de PNL pour extraire efficacement des caractéristiques, ce qui est crucial pour la précision du modèle dans la prédiction des secteurs d'emploi.


## Lien vers le Repo Contenant le Code

Vous trouverez ci-dessous le lien vers le dépôt qui contient le code pour le projet :

[Github Repo of the project](https://github.com/ElGarra/ProjetDataDDEFi23-24)

## Extrait d'une Offre d'Emploi Après une Requête

Voici un exemple d'offre d'emploi obtenue après avoir effectué une requête à l'API Pôle Emploi :

```json
{
        "id": "167GHBR",
        "intitule": "Opérateur Régleur de Machine de Fonderie de Métal (h/f)",
        "description": "ADECCO Bernay, recrute pour l'un de ses clients un(e) PLIEUR REGLEUR SUR MACHINE A COMMANDE NUMERIQUE H/F\n\nIntégré au pôle pliage, vous êtes chargé de la transformation des pièces sur plieuse a commande numérique.\n\nVotre rôle :\n\n\n - Garant des objectifs et impératifs de production (qualité, délai de l'opération)\n - Analyser les documents liés aux opérations de fabrication\n - Définir les moyens d'exécution des tâches\n - Programmer, régler et mettre en place des outils sur plieuse AMADA\n - Produire des pièces à plier selon gammes de fabrication\n\nVos compétences :\n\n\n - Lecture de documents techniques et plans\n - L'Utilisation d'outils de contrôle de mesure (pied à coulisse, jauge de profondeur, rapporteur...)\n - Contrôle dimensionnel à l'aide d'appareils de métrologie tels que pied à coulisse, jauge de profondeur, rapporteur d'angle...).\n\n\n\n\n\nVotre profil ;\n\n\n - Sans des responsabilités\n - Souci de la qualité\n - Autonomie\n - Réactivité\n - Rapidité de compréhension\nVous êtes de niveau CAP / BEP à BAC ( Bac Professionnel, Brevet Professionnel) en mécanique, productique ou travail des métaux.\n\nSi ce poste vous intéresse merci de postuler sur ADECCO&MOI",
        "dateCreation": "2024-01-05T19:15:07.000Z",
        "dateActualisation": "2024-01-05T19:15:09.000Z",
        "lieuTravail": {
            "libelle": "27 - ST MARDS DE BLACARVILLE",
            "latitude": 49.374514,
            "longitude": 0.510695,
            "codePostal": "27500",
            "commune": "27563"
        },
        "romeCode": "H2903",
        "romeLibelle": "Conduite d'équipement d'usinage",
        "appellationlibelle": "Opérateur(trice)-régleur(se) machine-outil usinage métaux",
        "entreprise": {
            "nom": "ADECCO FRANCE",
            "description": "Premier réseau d'agences d'emploi en France, Adecco a développé un savoir-faire unique de proximité et met toutes ses compétences à votre service.Nos équipes sont présentes sur tout le territoire, avec plus de 900 agences. Quel que soit le contrat que vous cherchez : CDI, CDD, Intérim, CDI Intérimaire, CDI Apprenant ou alternance, nos experts travaillent chaque jour, pour vous guider vers ce qui vous correspond. Dès maintenant, devenez acteur de votre vie !",
            "logo": "https://entreprise.pole-emploi.fr/static/img/logos/ccCJ1rOjn0xPf3L3vdY3xEZCuIleuXqb.png",
            "entrepriseAdaptee": false
        },
        "typeContrat": "MIS",
        "typeContratLibelle": "Mission intérimaire - 6 Mois",
        "natureContrat": "Contrat travail",
        "experienceExige": "D",
        "experienceLibelle": "Débutant accepté",
        "competences": [
            {
                "code": "100822",
                "libelle": "Techniques d'usinage",
                "exigence": "S"
            },
            {
                "code": "300135",
                "libelle": "Monter et régler une installation, une machine",
                "exigence": "S"
            },
            {
                "code": "300175",
                "libelle": "Piloter la gestion de la production, de l'exploitation",
                "exigence": "S"
            },
            {
                "code": "300185",
                "libelle": "Réaliser un diagnostic technique",
                "exigence": "S"
            },
            {
                "code": "300256",
                "libelle": "Contrôler la qualité et la conformité d'un livrable",
                "exigence": "S"
            }
        ],
        "salaire": {
            "libelle": "Horaire de 12,00 Euros sur 12 mois"
        },
        "dureeTravailLibelle": "35H Travail en journée",
        "dureeTravailLibelleConverti": "Temps plein",
        "alternance": false,
        "contact": {
            "nom": "ADECCO FRANCE - Mme BENEDICTE NAVEAU",
            "coordonnees1": "https://tnl2.jometer.com/v2/job?jz=5st1f78054903350b286de7de55461cdc8458AEADECAAAADAAAAAAAAAAAAAAAAC4ZESAI&utm_source=ADS&utm_medium=PoleEmplois&Source=30",
            "urlPostulation": "https://tnl2.jometer.com/v2/job?jz=5st1f78054903350b286de7de55461cdc8458AEADECAAAADAAAAAAAAAAAAAAAAC4ZESAI&utm_source=ADS&utm_medium=PoleEmplois&Source=30"
        },
        "nombrePostes": 1,
        "accessibleTH": false,
        "qualificationCode": "6",
        "qualificationLibelle": "Employé qualifié",
        "codeNAF": "78.20Z",
        "secteurActivite": "78",
        "secteurActiviteLibelle": "Activités des agences de travail temporaire",
        "origineOffre": {
            "origine": "1",
            "urlOrigine": "https://candidat.pole-emploi.fr/offres/recherche/detail/167GHBR"
        },
        "offresManqueCandidats": false
    }
```
