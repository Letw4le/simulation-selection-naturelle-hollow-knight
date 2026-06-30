from random import *
from math import *
import pygame

class virus_jaune:
    def __init__(self, indice):
        self.indice = indice
        self.vitesse=5
        self.vitesse_speed_up = self.vitesse
        self.pos_x= randint(50,1150)
        self.pos_y= randint(50,750)
        self.image=pygame.image.load("infection.png")
        self.hitbox = self.image.get_rect(topleft=(self.pos_x, self.pos_y))  #on crée un rectangle pour l'image qui servira d'hitbox et facilitera les collisions
        self.angle=uniform(0,2 * pi) # on initialise un angle en radians

    def deplacement_aleatoire(self):

        # si l'image touche un bord de l'écran on fait rebondir l'image
        if self.hitbox.left <= 0 or self.hitbox.right >= 1200:
            self.angle = pi - self.angle # on inverse la valeur de l'angle horizontal

        if self.hitbox.top <= 0 or self.hitbox.bottom >= 800:
            self.angle = -self.angle  # on inverse la valeur de l'angle vertical
        
        self.pos_x += self.vitesse_speed_up * cos(self.angle)
        self.pos_y += self.vitesse_speed_up * sin(self.angle)

        self.hitbox.topleft = (self.pos_x, self.pos_y) # on met à jour la position de la hitbox

    def save(self):
        with open("save.txt", "a") as f:
            f.write("\n" + "Virus jaune Indice : "+ str(self.indice) +  
                   " Position X : " + str(self.pos_x) + " Position Y :" + str(self.pos_y) + 
                   " Angle : " + str(self.angle))
            
    # méthode qui permet depuis la save de recréer l'individu   
    def recover_save(self,ind_ligne):
        with open("save.txt", "r") as f:
            contenu = f.readlines()
            ligne = contenu[ind_ligne]
            if ligne[0:11] == "Virus jaune":
                self.pos_x = float((ligne.split(":")[2]).split()[0])
                self.pos_y = float((ligne.split(":")[3]).split()[0])
                self.hitbox=self.image.get_rect(topleft=(self.pos_x,self.pos_y))  
                self.angle = float((ligne.split(":")[4]).split()[0])
            else:
                return
            

    #méthode qui change la vitesse de déplacement de l'individu en fonction de la vitesse de la simulation
    def speed(self, multiplicateur_vitesse):
        self.vitesse_speed_up = self.vitesse * multiplicateur_vitesse