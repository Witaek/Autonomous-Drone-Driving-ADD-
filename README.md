# Conduite autonome de drone
Code par Romain AMÉDÉE et Yassine BOUSSAFIR.
Cassiopée 2023

Notre projet a pour but de permettre la conduite autonome d’un drone. Le drone est capable d’effectuer des mouvements simples pour se positionner par rapport à une cible, et être capable de suivre cette même cible en mouvement, le tout en toute autonomie. Pour cela, nous disposons d’un drone Bebop Power 2 de la marque Parrot et nous proposons d’utiliser YOLOv4, un outil d’analyse d’image, afin de gérer la détection de la cible (une personne dans notre cas) sur le flux vidéo du drone.


Pour plus de détail, le rapport du projet est fourni dans ```rapport.pdf```

## Config

OS :  Ubuntu 18.04.6 LTS (Bionic Beaver). Il semble que cela soit l'OS à privilégier pour que cela fonctionne (travail infructueux sous Debian 11)

Python : 3.6.9

Machine utilisée : 

- Nom de l'appareil	LAPTOP-KIFGEJ7G

- Processeur	11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz   2.42 GHz

- Mémoire RAM installée	16,0 Go (15,7 Go utilisable)

- Type du système	Système d’exploitation 64 bits, processeur x64


Une VM clone de notre environnement de travail a été faite avec virtual box. Si toutefois vous vouliez reproduire manuellement l'environnement de travail que nous avons utilisé, une copie des packages utilisé est fournie dans le dossier ```packages```.


Afin d'installer les packages contenues dans cette archive : 

1. Faire attention d'être sous le même OS que nous, les détails sont contenus dans le fichier ```version.txt```.
2. Installer le package apt-clone : 
  ```bash
~$ sudo apt install apt-clone
```
3. Réinstaller tous les packages à partir de l'archive :
```bash
~$ sudo apt-clone restore ~/packages/apt-clone-state-cassiopee-VivoBook-ASUSLaptop-X513EA-K513EA.tar.gz
```
Pour plus de détails, voir [ici](https://github.com/mvo5/apt-clone).
<br/>

## Pré-requis 
Le fichier ```requirements.txt``` contient tous les packages Python à installer pour faire fonctionner notre travail. Pour tout installer, executez la commande suivante : 
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
