Projet INF1007 — A2026.

## Rappels de l'énoncé

- Au moins **5 entrées**, même si vous n'avez presque pas utilisé d'IA (dans ce cas, écrivez-le).
- Au moins **une entrée montre une vérification qui a changé votre décision**.
- Colonnes obligatoires : Outil · Ce que vous avez demandé · Réponse reçue · Vérification faite (documentation, test, exécution) · Décision (gardé, modifié, rejeté).


| # | Outil | Ce que nous avons demandé | Réponse reçue | Vérification faite | Décision |
|---|-------|---------------------------|---------------|--------------------|---------|

| 1 | Claude | Quelles métriques d'évaluation pourrions-nous utiliser pour notre modèle de classification de mots de passe ? | Plusieurs métriques ont été proposées, notamment l'exactitude, la précision, le rappel et le F1-score. | Nous avons comparé les métriques proposées à notre problème de classification en trois catégories. Nous avons également vérifié leur fonctionnement dans la documentation de scikit-learn. | Gardé : exactitude f1 macros |



| 2 | ChatGPT | Quelle est la différence entre un arbre de décision et une forêt aléatoire ? | L'arbre de décision est plus simple à interpréter, tandis que la forêt aléatoire combine plusieurs arbres pour effectuer ses prédictions. | Nous avons consulté la documentation de scikit-learn pour comprendre le fonctionnement des deux modèles. | Gardé : arbre de décision, puisqu'il est plus simple à expliquer. |


| 3 | ChatGPT | Comment éviter le surapprentissage avec un arbre de décision ? | Limiter la profondeur maximale de l'arbre est une façon de réduire le surapprentissage. | Nous avons vérifié le paramètre `max_depth` dans la documentation de `DecisionTreeClassifier`. | Gardé : utilisation de `max_depth = 10`. |


4 et 5 