"""Tests de la logique du modèle (modele.py), sans interface graphique."""
import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score

import modele
from exception import EntreeInvalideError, ModeleNonEntraineError
from modele import (Modele,
                    calculerReference, chargerMetadonnees,
                    chargerModele, encoderEntrees, exactitudeNumpy,
                    separerDonnees)


@pytest.fixture
def df():
    """Petit jeu de données synthétique : la force dépend surtout de la longueur."""
    rng = np.random.default_rng(0)
    n = 600
    longueur = rng.integers(4, 31, size=n)
    nbMaj = np.minimum(rng.integers(0, 4, size=n), longueur)
    nbChiffre = np.minimum(rng.integers(0, 4, size=n), longueur - nbMaj)
    nbSpecial = np.minimum(rng.integers(0, 3, size=n), longueur - nbMaj - nbChiffre)
    premier = rng.choice(['lettre', 'chiffre', 'special'], size=n)
    strength = np.where(longueur < 10, 0, np.where(longueur < 18, 1, 2))
    return pd.DataFrame({
        'password': ['x'] * n,
        'longueur': longueur,
        'nbMajuscule': nbMaj,
        'nbChiffre': nbChiffre,
        'nbSpecial': nbSpecial,
        'premierCaractere': premier,
        'strength': strength,
    })


@pytest.fixture
def modeleEntraine(df):
    m = Modele()
    m.entrainer(df)
    return m


# ----------  encodage ---------

def test_encoderEntrees_one_hot():
    X = pd.DataFrame({
        'longueur': [8], 'nbMajuscule': [1], 'nbChiffre': [2],
        'nbSpecial': [0], 'premierCaractere': ['chiffre'],
    })
    encode = encoderEntrees(X)
    assert encode.loc[0, 'premierCaractere_chiffre'] == 1
    assert encode.loc[0, 'premierCaractere_lettre'] == 0
    assert encode.loc[0, 'premierCaractere_special'] == 0
    assert 'premierCaractere' not in encode.columns


# ---------- métrique NumPy et référence ----------

def test_exactitudeNumpy_coincide_avec_sklearn():
    yReel = pd.Series([0, 1, 2, 2, 1, 0, 1, 2])
    yPredit = np.array([0, 1, 2, 1, 1, 0, 0, 2])
    assert exactitudeNumpy(yReel, yPredit) == pytest.approx(
        accuracy_score(yReel, yPredit))


def test_exactitudeNumpy_cas_limites():
    yReel = pd.Series([0, 1, 2])
    assert exactitudeNumpy(yReel, np.array([0, 1, 2])) == pytest.approx(1.0)
    assert exactitudeNumpy(yReel, np.array([1, 2, 0])) == pytest.approx(0.0)



# ---------- entraînement et prédiction ----------

def test_entrainer_batte_la_reference(modeleEntraine):
    m = modeleEntraine.metriques
    assert modeleEntraine.entraine is True
    assert m['exactitude'] > m['exactitudeReference']
    assert m['exactitudeNumpy'] == pytest.approx(m['exactitude'])


def test_predire_cas_usuel(modeleEntraine):
    etiquette, probas = modeleEntraine.predire(25, 2, 2, 1, 'lettre')
    assert etiquette in ('Faible', 'Moyen', 'Fort')
    assert sum(probas.values()) == pytest.approx(1.0)
    assert etiquette == max(probas, key=probas.get)


def test_predire_avant_entrainement_leve_une_erreur():
    with pytest.raises(ModeleNonEntraineError):
        Modele().predire(10, 1, 1, 1, 'lettre')


@pytest.mark.parametrize('args', [
    (0, 0, 0, 0, 'lettre'),      # longueur < 1
    (10, -1, 0, 0, 'lettre'),    # valeur négative
    (5, 3, 3, 0, 'lettre'),      # total (6) > longueur (5)
    (10, 1, 1, 1, 'emoji'),      # catégorie inconnue
])
def test_predire_entrees_invalides(modeleEntraine, args):
    with pytest.raises(EntreeInvalideError):
        modeleEntraine.predire(*args)


# ---------- sauvegarde et chargement ----------

def test_sauvegarder_puis_recharger(modeleEntraine, df, tmp_path, monkeypatch):
    dossier = tmp_path / 'modeles'
    monkeypatch.setattr(modele, 'DOSSIER_MODELES', str(dossier))
    monkeypatch.setattr(modele, 'cheminModele', str(dossier / 'modele.joblib'))
    monkeypatch.setattr(modele, 'cheminMetadonnees', str(dossier / 'metadonnees.json'))

    modeleEntraine.sauvegarder(df)

    meta = chargerMetadonnees(str(dossier / 'metadonnees.json'))
    assert meta['colonneCible'] == 'strength'
    assert meta['variables']['longueur']['min'] == int(df['longueur'].min())
    assert meta['variables']['longueur']['max'] == int(df['longueur'].max())

    recharge = chargerModele(Modele, str(dossier / 'modele.joblib'))
    assert recharge.predire(25, 2, 2, 1, 'lettre') == modeleEntraine.predire(25, 2, 2, 1, 'lettre')


