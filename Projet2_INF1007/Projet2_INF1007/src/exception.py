

class ErreurProjet(Exception):
    """Classe de base de toutes les erreurs du projet."""

class ModeleNonEntraineError(ErreurProjet, RuntimeError):
    """On essaie de prédire ou sauvegarder avant d'avoir entraîné le modèle."""



class DonneeInvalideError(ErreurProjet, ValueError):
    """Le CSV est vide, ou il manque des colonnes nécessaires."""



class EntreeInvalideError(ErreurProjet, ValueError):
    """Les caractéristiques données à predire() sont hors des valeurs permises."""

class LectureEcritureError(ErreurProjet,OSError):
    """Une lecture ou une écriture du fichier à échoué (conversion TSV vers CSV,etc.)."""