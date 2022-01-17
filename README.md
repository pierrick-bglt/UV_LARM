 Challenge 2 - Groupe Pourpre

Bienvenue sur la branche Git dédiée au challenge 2 de l'UV LARM du groupe pourpre composé de Pierrick Bougault et Hugo Lim, tous les deux en FISE 2023.

## Présentation du projet 

Le but de ce projet est de démontrer que le robot est capable de générer une cartographie de son environnement en prenant en compte la localisation des différentes bouteilles (nukacola). Pour cela, nous utilisons toujours l'environnement ROS (Robot Operating System) avec des fichiers launchs et Python, incluant le lancement de rviz et de gmapping.


## Notre stratégie

Dans ce projet, nous nous intéressons plus spécifiquement sur l’aspect vision du robot, dans le sens où nous essayons de trouver la méthode optimale pour reconnaître les bouteilles, sans se soucier de son déplacement (vu lors du challenge 1).
Ainsi, la méthode adoptée est celle de Viola-Jones (Haar) qui consiste à prendre différentes photos de la bouteille à repérer sous différents angles, luminosités et des photos ne contenant pas la bouteille afin d’obtenir un jeu de photos d’entraînement pour la machine permettant de distinguer la présence ou non de la bouteille dans son champ de vision.


## Installation

Récupérez notre code en clonant notre git :
```git
git clone https://github.com/pierrick-bglt/UV_LARM
```

Basculez sur la branche challenge2 :
```git
git checkout challenge2
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

Il y a différents scripts mais deux nous intéressent spécialement : mymarker.py et vision.py.

mymarker.py instaure la classe Cube qui correspond au marker que l’on va mettre en place à chaque fois qu’une bouteille sera repérée en initialisant différents paramètres comme la couleur ou l’échelle. Il y a également un publisher et une fonction qui permet de définir la position du cube.

vision.py concentre la plus grosse partie de notre travail avec différents callbacks, la détection de l’objet et le lancement des retours vidéo, le tout en mettant en œuvre la méthode de Viola et Jones, à partir du fichier cascade.xml.


## Commentaires de nos résultats

Notre aspect vision n’est pas optimal. En effet, bien qu’il puisse bien distinguer les bouteilles, il est également très sensible à l’environnement autour et repère de manière intempestive, tout ce qui semble être d’une couleur proche à nos bouteilles (surtout le pied des délimitations de la zone qui est également de couleur noire). Pour remédier à cela, nous aurions pu soit employer une autre méthode, soit insister sur la couleur en mettant en place un histogramme de couleurs.
Par ailleurs, nous avons été confrontés à un problème technique lié à ROS la fin de journée du vendredi, en effet, la caméra ne se lançait plus et nous n'avions donc aucun retour vidéo pour analyser ce qui était repéré par la machine.

De plus, nous pouvons affiner notre placement de cube sur rviz en récupérant la profondeur z du capteur et de la placer dans les coordonnées cartésiennes du robot. 

Tous ces éléments sont des objectifs pour notre rendu final.
