# Conduite autonome de drone
Code par Romain AMÉDÉE et Yassine BOUSSAFIR.
Cassiopée 2023

Notre projet a pour but de permettre la conduite autonome d’un drone. Le drone est capable d’effectuer des mouvements simples pour se positionner par rapport à une cible, et être capable de suivre cette même cible en mouvement, le tout en toute autonomie. Pour cela, nous disposons d’un drone Bebop Power 2 de la marque Parrot et nous proposons d’utiliser YOLOv4, un outil d’analyse d’image, afin de gérer la détection de la cible (une personne dans notre cas) sur le flux vidéo du drone.

## Config

OS :  Ubuntu 18.04.6 LTS (Bionic Beaver). Il semble que cela soit l'OS à privilégier pour que cela fonctionne (travail infructueux sous Debian 11)

Python : 3.6.9

Une VM clone de notre environnement de travail a été faite avec virtual box.

<br/>

## Pré-requis 
Le fichier ```requirements.txt``` contient tous les packages à installer pour faire fonctionner YOLO. Pour tout installer, executez la commande suivante : 
``` bash
~$ pip install -r requirements.txt
```

<br/>

## Fonctionnement 

La partie pratique du travail se trouve dans le fichier ```launch.py```. C'est dans se fichier que s'effectue la connection au drone ainsi que les prises de décisions sur les mouvements de ce dernier. C'est le fichier privilégié pour modifier les paramètres de vol. On peut y définir : 
- la durée du vol
- l'altitude du drone
- le comportement du drone
- la fréquence de traitement des images du drone

Les dessins sur l'image (rectangle, barycentre, centre du champ de vision) sont gérés dans le fichier ```core/utils.py```. La zone à modifier pour changer les paramètres de dessin y est clairement définie par des commentaires.

## Mise en marche

1. Allumer le drone
2. Se connecter au wifi du drone
3. Lancer la commande ```python3 launch.py```
Le drone décole et vole pendant la durée déterminée dans launch.py. Si une personne se trouve dans son champ de vision, le drone suit / se stabilise par rapport à cet individu en fonction de son mouvement. Le drone attérit tout seul au bout du temps imparti dans le fichier launch.py

### Quelques sources utiles

1. Pour comprendre Yolo :  [Yolo](https://pjreddie.com/darknet/yolo/)
2. Github dont on s'est inspiré pour la détection des personnes : [Yolo detection](https://github.com/DoranLyong/yolov4-tiny-tflite-for-person-detection)
3. Documentation pyparrot pour le controle du drone : [pyparrot](https://pyparrot.readthedocs.io/en/latest/)
4. Travail de stagiaires de l'ENSTA sur le sujet : [github](https://github.com/pedrobranco0410/Bebop-with-Reinforcement-Learning)
