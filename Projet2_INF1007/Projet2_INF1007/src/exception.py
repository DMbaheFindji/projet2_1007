


class ModeleNonEntraineError(ErreurProjet, RuntimeError):
    """On essaie de prédire ou sauvegarder avant d'avoir entraîné le modèle."""
