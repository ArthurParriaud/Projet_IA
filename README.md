# Projet d'Intelligence Artificielle - Computer Vision pour la lecture automatique de factures

En nous plaçant dans la perspective d’une boîte de conseil, nous devons offrir à
un client un système lui permettant d’extraire le total de factures prises en
photos et nous sommes accompagnés d’un consultant : aucun set d’image de
factures nous est fourni, donc on utilisera notre propre set d’une qualité
volontairement basse pour augmenter son efficacité. On se place dans de la
lecture d’image, autrement appelée « OCR » (Optical Character Recognition).

De nos jours, les meilleurs systèmes de reconnaissance de caractères tels que
Google ou Amazon fonctionnent à partir d’un modèle d’apprentissage : nous
devrons cela dit passer par une méthode plus classique. Nous avons
commencé par développer notre projet en suivant les travaux fournis par notre
consultant pour arriver à lire une première image. Ensuite, nous avons cherché
à lire des images supplémentaires de notre dataset en faisant varier nos
paramètres. L’idée en finalité était d’arriver à trouver un moyen d’automatiser
le traitement de chaque image bien que chacune d’entre elle nécessitait des
paramètres personnalisés : la solution que l’on propose passe par un processus
de traitement d’image pour faciliter les étapes suivantes, puis par de
l’extraction de texte ainsi que du traitement de texte pour chercher le total. On
a choisi de réaliser plusieurs itérations avec à chaque fois des paramètres
différents pour chaque méthode de traitement d’image : le résultat de chaque
itération est stocké dans un tableau et on prend la valeur non nulle la plus
occurrente dans celui-ci. Ceci nous a permis d’obtenir des résultats corrects
mais incomparable face aux solutions utilisant des modèles d’apprentissages :
cela souligne le challenge de passer par une méthode classique. Nos résultats
nous permettent d’assurer une lecture efficace sur des images de bonnes
qualités. À l’avenir, si nous devions continuer de travailler sur le projet, nous
chercherions de nouvelles idées pour augmenter la précision de notre solution
sur notre set de données de basse qualité. De plus, nous essaierions d’extraire
d’autres informations en guise de détails, de réduire le temps de lectures des
images ainsi que de développer une API pour faciliter l’utilisation de notre
programme.


## Solution Proposée

La première étape de notre solution concerne notre dataset. En effet, on
rappelle que notre client ne pouvait pas nous en fournir pour des raisons
réglementaires. Ainsi, nous sommes partis de notre propre dataset composé
de plusieurs photos de reçus. Ce dernier est volontairement de basses
qualités : les reçus ne sont pas centrés ou encore la photo est de mauvaise
qualité. Cela nous permet de garantir l’efficacité de notre solution face aux
réelles photos que notre client voudra lire automatiquement. Tout au long du
développement de notre solution, nous avons utilisé exclusivement les images
de notre dataset.

Pour pouvoir travailler sur des images, nous avons choisi d’utiliser la
bibliothèque OpenCV2 : elle nous permet non seulement d’ouvrir une image,
mais également d’y appliquer plusieurs traitements que l’on verra par la suite.
Nous avons choisi de créer la classe imageToRead nous permettant de créer un
objet image et d’y stocker toutes nos méthodes.

La première véritable étape de notre solution consiste à traiter l’image que
l’on reçoit : cela facilitera grandement la lecture à la suite. En utilisant la
libraire OpenCV2, nous appliquons tous ces traitements :

- **Réduction de la taille de l’image** : on réduit notre image dans le but de
réduire le bruit présent. De plus, cela permet également d’augmenter la
performance de notre projet.

- **Passage en noir et blanc** : nous choisissons d’enlever les couleurs de
notre image. Cela permet de se débarrasser d’information inutile : ainsi,
nous rajoutons de la performance mais également de l’efficacité à notre
projet qui pourra lire plus facilement.

- **Flou appliquée sur l’image** : en rajoutant du flou, nous diminuons
grandement le bruit présent sur la photo, garantissant une meilleure
extraction de texte.

Après ces trois premiers traitements, on cherche à détecter le contour de
notre reçu dans le but de rogner notre image sur les bords de ce dernier. Pour
cela, nous appliquons ces étapes toujours à l’aide de la bibliothèque OpenCV2 :

- **Dilatation de l’image** : un grand classique dans le traitement de l’image,
après avoir appliqué du flou ou de l’érosion. En effet, pour rendre le
texte plus lisible mais surtout pour faciliter la détection des contours du
reçu, on dilate l’image.

- **Détection des contours** : on cherche le contour du reçu. Cette étape
nous a posé quelques difficultés. En effet, d’une image à une autre, le
traitement d’image n’est pas réellement le même et détecter un contour
avec de mauvais traitements est délicat. C’est pour cela que notre
programme suit ce procédé : si le rapport entre le contour détecté et la
taille de l’image est assez grand, alors on le garde. Sinon, on passe
l’étape suivante pour éviter de cadrer l’image sur un mauvais contour.

- **Changement de perspective** : une fois que l’on a trouvé le contour du
reçu, nous changeons de perspectives : l’image devient le reçu
directement, sans rien autour, garantissant une lecture optimale.

Une fois que le traitement d’image est terminé, nous passons à la deuxième
étape consistant à extraire le texte. On utilise la librairie Tesseract pour
extraire l’entièreté du texte lisible de notre image.

Maintenant que l’on a le texte, notre objectif est de connaître le montant total
de la facture : on passe à la troisième étape de notre solution, le traitement de
texte. Pour savoir comment obtenir ce qui nous intéresse, voilà comment nous
avons procédé :
- Le total est dans tous les reçus un nombre à virgule.
- Le total n’excède jamais une certaine valeur.
- Le total est dans la très grande majorité des cas le plus grand nombre à virgule écrit sur le reçu.

À partir de ces trois conditions, nous avons appliqué à notre texte un filtre
pour prendre le plus grand nombre à virgule inférieur à 1000.
Malheureusement, cette technique a ses défauts. En effet, prenons les États-Unis : il s’agit d’un pays où en plus du total, un client se doit de donner un
pourboire variant autour de 15 pourcents. Ainsi, certains reçus possèdent un
tableau avec la somme total additionnée à un pourcentage. Notre programme
dans ce cas prendra la valeur avec le pourboire le plus élevé.

Les trois étapes que nous avons abordées ci-dessus nous permettent ainsi dans
une majorité de cas d’extraire la bonne valeur. Mais nous ne pouvons pas nous
permette de nous arrêter là : en effet, étant parti d’un dataset de basse
qualité, chaque image nécessite un traitement personnalisé. C’est ici
qu’intervient la quatrième étape. Pour rendre le traitement d’image valable
pour la totalité des images, nous avons choisi de procédé comme suit :

- Chaque étape de traitement prend des valeurs en paramètre,
notamment sur l’intensité du flou ou de la dilatation par exemple. Ainsi,
au lieu de retenir qu’une seule valeur pour chaque paramètre, nous
prenons plusieurs valeurs que nous plaçons dans un tableau.

- Le programme va s’exécuter avec toutes les combinaisons de
paramètres possible. Pour chacune d’entre elles, on place dans un
tableau le total retenu. Notons qu’il n’est pas rare que le programme ne
parvienne pas à lire de valeur valable : dans ce cas, le total retenu prend
la valeur « None ».

- Une fois que toutes les combinaisons de paramètres ont été effectuées,
nous avons un tableau avec plusieurs potentiels totaux : nous
retiendrons en finalité le total non nul qui a été le plus lu par notre code.
Il n’est pas impossible que chacune des itérations ait renvoyé un total
nul et donc que le tableau final soit composé exclusivement de
« None ». Dans ce cas, notre programme renvoie une valeur nulle.

Cette quatrième étape gère un problème que nous n’avons pas abordé : la
détection de contour peut être délicate pour la plupart des images. Ainsi, pour
chaque itération, notre programme essayera de trouver le contour du reçu et
procédera de toute manière aux étapes suivantes.

Désormais, pour tester notre programme, nous avons lu la totalité des images
de notre dataset de basse qualité et nous avons écrit les résultats dans un
tableur Excel (disponible dans le Github sous le nom de score_test1.xlsx) :

Nous avons utilisé les services de l’Etat de l’Art tel que Google ou Amazon
fonctionnant à base de modèles d’apprentissages contrairement à notre
solution. Ainsi, nous avons pu avoir un comparatif.

À partir de cela, nous avons choisi de faire une seconde version de notre
programme pour augmenter notre précision : notre principal objectif était de
régler au mieux la détection des contours. C’est pour cela que nous avons
rajouter à notre classe imageToRead des méthodes pour ajouter des bandes
horizontales ou verticales : l’idée derrière cette méthode est que si la totalité
du contour ne se situe pas dans l’image en entier, on vient rajouter des bandes
pour simuler de l’arrière-plan et faciliter la détection de notre reçu.

Une autre idée que l’on a eue et qui nous a permis de gagner en précision par
rapport à notre première version est de rajouter la méthode SplitImage qui va
venir couper l’image en deux et garder que la partie du bas : en effet, le total à
lire dans les images est toujours situé dans la partie basse. Cela nous a permis
d’enlever beaucoup de détails inutiles et faciliter la lecture de notre texte.
