from pyparrot.Bebop import Bebop  # Importe la classe Bebop du module pyparrot
from pyparrot.DroneVision import DroneVision  # Importe la classe DroneVision du module pyparrot
import threading  # Importe le module threading pour prendre en charge le multi-threading
import cv2  # Importe le module cv2 pour le traitement d'images
import time  # Importe le module time pour la gestion du temps
import run_person_detector as detector  # Importe le module run_person_detector comme détecteur d'objets
import numpy as np  # Importe le module numpy pour le calcul numérique


isAlive = False

class UserVision:
    def __init__(self, vision, bebop):
        self.index = 0  # Variable pour le suivi de l'index des images
        self.vision = vision  # Initialise l'objet vision
        self.last_picture_time = time.time()  # Initialise le temps de la dernière image capturée avec le temps actuel
        self.drone = bebop  # Initialise l'objet drone

    def save_pictures(self, args):
        current_time = time.time()  # Obtient le temps actuel
        time_diff = current_time - self.last_picture_time  # Calcule la différence de temps depuis la dernière image capturée
        if time_diff < 0.5:
            # Attendre x secondes depuis la dernière image avant de traiter une nouvelle image
            return
        self.last_picture_time = current_time # Met à jour le temps de la dernière image capturée avec le temps actuel

        img = self.vision.get_latest_valid_picture() # Obtient la dernière image valide de la vision

        if img is not None: #si l'image existe
            result, coordinates, barycenter = detector.run_object_detection(img) # Exécute la détection de personne sur l'image
            self.index += 1

            print(coordinates, barycenter) # Affiche les coordonnées et le barycentre (optionnel, pratique pour debugage et tests)

            if (coordinates != [0,0,0,0]):
                bx = barycenter[0] # Coordonnée x du barycentre
                by = barycenter[1] # Coordonnée y du barycentre

                rapport = (coordinates[1] - coordinates[0]) / (coordinates[3] - coordinates[2]) # Calcul rapport longueur / largeur avec les coordonnées du rectangle de détection
                print(rapport) #affichache du rapport l/L (optionnel)

                # ==================== Algorithme de comportement du drone ===========
                if(bx > 448):
                    print("rotate right")
                    self.drone.move_relative(0,0,0,0.1) # rotation de 0.1 radian en sens horaire
                elif(bx < 408):
                    print("rotate left")
                    self.drone.move_relative(0,0,0,-0.1) # rotation de 0.1 radian en sens trigo
                elif (rapport >= 2 and by < 220):
                    print("move frontward")
                    self.drone.move_relative(.15,0,0,0) # translation de 15 cm vers l'avant

                elif (by > 260):
                    print("move backward")
                    self.drone.move_relative(-.15,0,0,0) # translation de 15 cm vers l'arrière
                
                # =================== Fin de l'algorithme =============================

            cv2.imshow("Image", result.astype(np.uint8)) #affiche l'image résultante (avec rectangle de détection, barycentre et centre du champ de vision du drone)
            cv2.waitKey(1) # Ajoute un petit délai pour permettre à l'interface graphique de se mettre à jour

bebop = Bebop() # Crée une instance de l'objet Bebop

success = bebop.connect(5) # se connecter au bebop
bebop.set_max_altitude(2) # on fixe l'altitude max à 2m

if success: # si la connection au drone est bien étbie

    bebopVision = DroneVision(bebop, is_bebop=True)  # Crée une instance de l'objet DroneVision

    userVision = UserVision(bebopVision, bebop)  # Crée une instance de l'objet UserVision
    bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)  # Définit la fonction de rappel utilisateur
    success = bebopVision.open_video()  # Ouvre la vidéo du drone

    bebop.safe_takeoff(10) # le drone décole
    bebop.move_relative(0,0,-1.3,0) # on fixe l'altitude à environ 2m
    bebop.pan_tilt_camera(-30,0) # on tourne la caméra de 30 radian vers le bas pour bien visualiser les individus


    if success:
        print("Vision successfully started!")

        bebop.smart_sleep(60) #durée du vol (ici 60 secondes)
        bebop.safe_land(10) # au bout des 60 secondes, le drone attérit

        bebopVision.close_video() # ferme le flux vidéo du drone

    
    bebop.disconnect() # déconnecte proprement le drone afin de ne pas avoir à le redémarrer
else:
    print("Error connecting to bebop. Retry") # Affiche un message d'erreur si la connexion au drone a échoué
