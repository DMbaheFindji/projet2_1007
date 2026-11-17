from exception import DonneeInvalideError, EntreeInvalideError
from modele import (Modele, chargerDonnees, cheminFichierCsv,
                    cheminMatriceConfusion, sauvegarderMatriceConfusion,
                    separerDonnees)


def main() -> None:
    # 1. Charger et nettoyer les données
    try:
        df = chargerDonnees(cheminFichierCsv)
    except (FileNotFoundError, DonneeInvalideError) as erreur:
        print(f'Erreur : {erreur}')
        return
    print(f'{len(df)} lignes chargées')

    # 2. Séparer, entraîner et évaluer
    XTrain, XTest, yTrain, yTest = separerDonnees(df)
    modele = Modele()
    metriques = modele.entrainer(XTrain, yTrain, XTest, yTest)
    print(modele)
    print(f"Exactitude : {metriques['exactitude']:.3f}")
    print(f"Référence  : {metriques['exactitudeReference']:.3f}")
    print(f"F1 macro   : {metriques['f1Macro']:.3f}")

    # 3. Sauvegarder le modèle, les métadonnées et la matrice de confusion
    modele.sauvegarder(df)
    sauvegarderMatriceConfusion(yTest, modele.predireLot(XTest), cheminMatriceConfusion)
    print('Fichiers écrits dans le dossier modeles/')

    # 4. Prédiction normale
    etiquette, probas = modele.predire(12, 1, 1, 0)
    print(f'Prédiction : {etiquette} {probas}')

    # 5. Saisie invalide : doit afficher un message, pas planter
    try:
        modele.predire(0, 1, 1, 0)
    except EntreeInvalideError as erreur:
        print(f'Saisie refusée : {erreur}')


if __name__ == '__main__':
    main()