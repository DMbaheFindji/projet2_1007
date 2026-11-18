"""Tests de la classe JeuDeDonnees (conversion TSV -> CSV et caractéristiques)."""
import matplotlib
matplotlib.use("Agg")

import pandas as pd

from JeuDeDonnees import JeuDeDonnees


def creerTsv(dossier, lignes):
    """Écrit un petit fichier TSV (avec en-tête) et renvoie un JeuDeDonnees."""
    contenu = 'password\tstrength\n' + ''.join(f'{p}\t{s}\n' for p, s in lignes)
    (dossier / 'brut.tsv').write_text(contenu, encoding='utf-8')
    return JeuDeDonnees(str(dossier), 'brut.tsv', 'donnees.csv')


def test_convertir_calcule_les_caracteristiques(tmp_path):
    jeu = creerTsv(tmp_path, [('Abc123!', 2)])
    df = pd.read_csv(jeu.convertirETdevelopper())
    ligne = df.iloc[0]
    assert ligne['longueur'] == 7
    assert ligne['nbMajuscule'] == 1
    assert ligne['nbChiffre'] == 3
    assert ligne['nbSpecial'] == 1
    assert ligne['premierCaractere'] == 'lettre'
    assert ligne['strength'] == 2


def test_convertir_premier_caractere(tmp_path):
    jeu = creerTsv(tmp_path, [('abc', 0), ('1abc', 1), ('#abc', 2)])
    df = pd.read_csv(jeu.convertirETdevelopper())
    assert list(df['premierCaractere']) == ['lettre', 'chiffre', 'special']


def test_convertir_respecte_la_limite_de_lignes(tmp_path):
    (tmp_path / 'brut.tsv').write_text(
        'password\tstrength\n' + ''.join(f'mot{i}\t1\n' for i in range(10)),
        encoding='utf-8')
    jeu = JeuDeDonnees(str(tmp_path), 'brut.tsv', 'donnees.csv', limiteLigne=3)
    df = pd.read_csv(jeu.convertirETdevelopper())
    assert len(df) == 3


def test_convertir_fichier_absent_renvoie_chaine_vide(tmp_path):
    jeu = JeuDeDonnees(str(tmp_path), 'inexistant.tsv', 'donnees.csv')
    assert jeu.convertirETdevelopper() == ""
    assert not (tmp_path / 'donnees.csv').exists()