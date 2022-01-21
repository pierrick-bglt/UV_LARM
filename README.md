 Challenge 3 - Groupe Pourpre

Bienvenue sur la branche Git dédiée au challenge 3 de l'UV LARM du groupe pourpre composé de Pierrick Bougault et Hugo Lim, tous les deux en FISE 2023.

## Présentation du projet 

Le but de ce projet est de combiner le challenge 1 et le challenge 2 pour rendre le robot autonome dans son fonctionnement.

## Notre stratégie

Pour la stratégie de mouvement nous avons adopté une stratégie de tirage aléatoire de direction. Lorsque le robot rencontre un obstacle il y a équiprobabilité quil tourne à gauche ou à droite. 
 
Pour la stratégie de vision, nous avons essayé de trouver la méthode optimale pour reconnaître les bouteilles, sans se soucier de son déplacement (vu lors du challenge 1). Ainsi, la méthode adoptée est celle de Viola-Jones (Haar) qui consiste à prendre différentes photos de la bouteille à repérer sous différents angles, luminosités et des photos ne contenant pas la bouteille afin d’obtenir un jeu de photos d’entraînement pour la machine permettant de distinguer la présence ou non de la bouteille dans son champ de vision.


## Installation

Récupérez notre code en clonant notre git :
```git
git clone https://github.com/pierrick-bglt/UV_LARM
```

Basculez sur la branche challenge3 :
```git
git checkout challenge3
```


## Mise en garde

Avant de lancer le test, il est nécessaire d’installer sur votre machine mb6-tbot pour que tout puisse fonctionner correctement.
Tout est disponible ici : https://bitbucket.org/imt-mobisyst/mb6-tbot/src/master/


## Phase de tests pour l'évaluation

Avant de commencer, copiez ces commandes dans le catkin workspace (compiler et sourcer) :
```git
catkin_make
source devel/setup.bash
```

Pour lancer la démonstration :
```git
roslaunch grp-pourpre challenge2.launch
```

Cette commande active donc le launch qui lance à la fois les scripts Python, rviz (avec la configuration préalablement établie), gmapping ainsi que le rosbag.
Évidemment, nous pouvons essayer avec d'autres fichiers rosbag préalablement installés dans le dossier bagfiles, en modifiant l’argument dans le launch file.


## Composition des scripts

Nous avons codé deux scripts différents move_avoid_collision.py et vision.py.

move_avoid_collision.py est le scripts dédié aux mouvements du robot dont le fonctionemment est spécifié au-dessus;

vision.py concentre la plus grosse partie de notre travail avec différents callbacks, la détection de l’objet et le lancement des retours vidéo, le tout en mettant en œuvre la méthode de Viola et Jones, à partir du fichier cascade.xml. 
Nous avons aussi codé une classe cube qui nous permets de manipuler et de publier des marqueurs plus facilement dans rviz.


## Commentaires de nos résultats

Nos déplacements sont corrects, le robot se déplace fluidement dans son environnement sans heurter des obstacles. 
Notre aspect vision n’est pas optimal. En effet, bien qu’il puisse bien distinguer les bouteilles, il est également sensible l’environnement autour et effectue des fausses alarmes (tout ce qui semble être d’une couleur proche à nos bouteilles surtout le pied des délimitations de la zone qui est également de couleur noire). Pour avons essayé de faire un filtre de couleur qui fonctionne cependant nous n'avons réussi à le coordonner avec notre programme.
De plus, pour placer un marqueur nous avons un publisher pour lire les datas de profondeur de la caméra.

## Difficultés rencpontrés lors du module 

Durant l'UV LARM nous avons rencontré quelques difficultés à prendre en main le logiciel ROS, et à maîtriser les notions vu lors des tutorials. 
De plus, nous avons eu un accès limité à linux nous empêchant de pouvoir travailler depuis chez nous. 