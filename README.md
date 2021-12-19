# Challenge 1 - Groupe Pourpre

Bienvenue sur la branche Git dédiée au challenge 1 de l'UV LARM du groupe pourpre composé de Pierrick Bougault et Hugo Lim, tous les deux en FISE 2023.

## Présentation du projet 

Le but de ce projet est de faire se déplacer un robot dans une zone restreinte avec des obstacles, à la fois via une simulation virtuelle mais aussi avec un Turtlebot réel. Pour cela, nous utilisons l'environnement ROS (Robot Operating System) et avons créé des launchs ainsi que des scripts Python.
Un lancement de riviz est aussi programmé à chaque lancement de roslaunch grp-pourpre + fichier.launch

## Notre stratégie

Notre stratégie se base sur une rotation aléatoire de la rotation droite ou gauche.
A chaque fois que le robot arrive devant un mur sa probabilité de tourner à droite ou gauche est de 50%.
Avec cette stratégie, le robot finira par explorer tout son environnement.

## Installation

Récupérez notre code en clonant notre git :
```git
git clone https://github.com/pierrick-bglt/UV_LARM
```

Basculez sur la branche challenge1 :
```git
git checkout challenge1
```

## Phase de tests pour l'évaluation

Pour lancer la simulation ou la démo avec le Turtlebot, copiez ces commandes dans le catkin workspace (compiler et sourcer) :
```git
catkin_make
source devel/setup.bash
```

Pour lancer la simulation :
```git
roslaunch grp-pourpre challenge1_simulation.launch
```

Pour lancer la démo avec le Turtlebot :
```git
roslaunch grp-pourpre challenge1_turtlebot.launch
```








