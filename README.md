# Partitionnement de donnees

#### Informations générales :

* [Depôt Github](https://github.com/Wiiz971/partitionnement-de-donnees/)

* Collaborateurs  :
    * [Vincent AZINCOURT](https://github.com/Wiiz971)
    * [Nicolas YAZMAN](https://github.com/jsp)

* Outils utilisés pour le projet :
    * [Python 3.7.9](https://www.python.org/downloads/release/python-379/) (au delà le module pptk n'est pas utilisable)
    * [Spider version 5.2.2](https://www.spyder-ide.org/) 
    * Documentation comparable à [Doxygen](https://en.wikipedia.org/wiki/Doxygen)
    * Importer le module PPTK ’pip install pptk’ pour visualiser le nuage de points
    * Importer le module scipy ’pip install scipy' pour faire la décomposition en valeur singulière (SVD)
    * Importer le module matplotlib ’pip install matplotlib' pour visualiser la courbe pour chaque angle trouvé
    * Importer le module random ’pip install random' pour la géneration aléatoire des données (coordonnées des points, cluster...)
    * Importer le module time´’pip install time' pour utiliser des compteurs temporels
     
 *******
 
 ####  [Tâche 1](https://github.com/Wiiz971/partitionnement-de-donnees/blob/main/Partitionnement%20de%20donnees/Tache1.py) : [UPDATE]
 
* Générer une sphère (de 1000 points) ✔️

* ~~Générer des points (à une certaine distance) sur la surface de la sphère (DBSCAN)~~
* ~~Pour chacun des points, faire une décomposition en valeur singulière (SVD)~~
* ~~Faire une matrice 3x3 en angle Eulérien~~
* ~~Prendre une des trois composantes du vecteur B (de la matrice 3x3) et convertir en degrés (a × 180/π)~~
* ~~Incrémenter de 1 pour chaque angle trouvé pour en déduire une densité de probabilité~~

* Pour chaque point du nuage de point, regarder ceux qui sont en dessous d'une certaine distance parmi tous les points de la sphère (distance euclidienne/DBSCAN) ✔️
* Si c'est inférieur à un seuil, on les ajoute à un ensemble ✔️
* Faire une [SVD](https://en.wikipedia.org/wiki/D%C3%A9composition_en_valeurs_singuli%C3%A8res) sur cet ensemble une fois que tous les points ont été traité ✔️
* Prendre la matrice V (si c'est Nx3 l'ensemble) et transformer [les coordonnées en angles euleriens](https://learnopencv.com/rotation-matrix-to-euler-angles/) ✔️
* Prendre l'azimuth en radians (premiere coordonnée du vecteur) et * 180 / pi. ✔️
* Round le nombre au plus proche et incrémenter compteur[angle]++ ✔️

_Premier essai :_

_repartition des angles (de 0 à 360°):_
![image](https://user-images.githubusercontent.com/47423231/161948353-8d79017f-791b-43fa-8c42-92476a8d915a.png)

![image](https://user-images.githubusercontent.com/47423231/161948220-9aeba6e2-0dee-476f-86f2-5bccee6a5382.png)

_Deuxième essai :_

_repartition des angles (de 0 à 360°) :_
![image](https://user-images.githubusercontent.com/47423231/161949080-c2748c1a-db8c-4e35-8602-166f4ebf0f26.png)

![image](https://user-images.githubusercontent.com/47423231/161948952-ebf96fc0-5b8c-44fc-bb4d-5ae0019859c4.png)

_suivant l'azimuth (angle θ)_





 ####  [Tâche 2](https://github.com/Wiiz971/partitionnement-de-donnees/blob/main/Partitionnement%20de%20donnees/Tache2.py):

* Réaliser une [triangulation de Delaunay](https://en.wikipedia.org/wiki/Delaunay_triangulation) sur l'ensemble des points ✔️
* Une fois que les points sont utilisés, remplacer leur valeur par des zones négatives ( ≠ 1) ✔️
* Compléter [un algorithme](https://tousu.in/qa/?qa=753100/) permettant de faire plusieurs triangulations de Delaunay en parallèle (afin de réduire l'ordre de complexité de l'algorithme) ✔️
* Utiliser un timer entre deux triangulations puis entre chaque itération ✔️

![image](https://user-images.githubusercontent.com/47423231/161955815-89afb13a-322b-4224-bd7d-d01bed7a6824.png)
![image](https://user-images.githubusercontent.com/47423231/161955787-498769b7-5b70-4773-ad24-597978e6c0c3.png)
![image](https://user-images.githubusercontent.com/47423231/161956011-d537bd3e-cfcf-4994-9585-023eaf286470.png)

_Et lorsque l'on compare les deux manieres d'appliquer une triangulation de Delaunay, on obtient ceci :_
![image](https://user-images.githubusercontent.com/47423231/161956109-069e1270-dbde-4c83-928e-bda6fa8d4290.png)

Si l'on fait une serie de 10 tests et qu'on en deduit une _moyenne_ de l'optimisation du temps d'exécution, on obtient un facteur x129.8

 ####  [Tâche 3](https://github.com/Wiiz971/partitionnement-de-donnees/blob/main/Partitionnement%20de%20donnees/Tache3.py):
 
* Faire un grille d'occupation spatiale
* 
![image](https://user-images.githubusercontent.com/47423231/163413928-93dc99b2-b51f-4bd6-bb89-250d01b6d9f2.png)
![image](https://user-images.githubusercontent.com/47423231/163413894-28a0a1f1-582e-433d-9db1-1ffce64878e0.png)

* Faire une triangulation de Delaunay de manière séquentielle sur chaque sous ensemble
* Optionnel : Faire un point
* Faire en parallèle le calcul des Delaunays successives
* Comparer les résultats des deux méthodes : Delaunay parallèle et Delaunay sur l'ensemble des points.

