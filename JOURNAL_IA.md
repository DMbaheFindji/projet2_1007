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



| 4 |ChatGPT|Comment faire pour que dans l'interface ce ne soit pas directement le nom des variables d'entrées écrit, mais des noms plus compréhensible ? |Il suffit d’utiliser un dictionnaire qui associe chaque nom interne (celui du modèle) au nom affiché dans l’interface. Les noms internes ne changent pas, seulement ce que l’utilisateur voit.|Nous sommes allez regarder les notes de cours du cours 1007 chapitre 4 section 4 pour revoir cette structure de donnée pour pouvoir être en mesure de mieux analyser si elle conviendrait dans cette partie du code. |Gardé : Après avoir exécuter le code avec le dictionnaire implémenté, nous nous sommes rendu compte que cela marchait très bien et nous avons décidé de garder cette proposition.


| 5 | ChatGPT| Dans une application qui utiliserait un modèle entraîné, comment pourrions-nous intégrer l'utilisation d'un décodeur ?| Il nous a conseillé mesurer le temps d'entraînement du modèle. | Après avoir relu l'énoncé de ce projet, nous avons remarqué qu'à la page 4, le chronomètre était bel et bien une des propositions fournit. Donc, nous avons fait la fonction, nous l'avons testé et nous avons vu que tout marchait bien.| Gardé : Nous avons alors décidé de garder cette proposition .


| 6 | Claude | Quel serait le meilleur moyen d'ajouter une image dans l'interface si nous utilisons PyQt6 ?|Il nous a conseillé d'utiliser QPixmap.| Nous sommes allé regarder la documenttation de QPixmap pour en apprendre plus sur cette classe. 
Lien : https://doc.qt.io/qt-6/qpixmap.html
|Gardé: nous avons décidé de gardé cette idée et d'utiliser QPixmap pour l'intégration de nos graphiques dans l'interface.

| 7 | ChatGPT | Comment m'assurer de prévoir toutes les exception dans la classe l'interface lorsque l'utilisateur saisie quelque chose d'invalide ?| Il nous a conseillé d' utiliser un valueError .| Nous avons relu les consignes de l'énoncé et avons vu qu'il fallit essayer d'utiliser des exceptionn spécial.
|Gardé:Nous avons décider de spécialiser nos exception plus que de simple Value Error

| 8 | Claude | Comment vérifier que notre projet est prêt à être remis et corriger les problèmes trouvés ? | Il a proposé de tester un clone neuf, de placer les fichiers à la racine du dépôt et de modifier un test pour qu'il attende `LectureEcritureError`. | Nous avons lancé `python -m pytest` (15 tests réussis) et vérifié que la CI était verte sur GitHub. | Gardé : nous avons réorganisé le dépôt et modifié le test. |


