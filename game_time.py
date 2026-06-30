# Fichier s'occupant la gestion du temps lors de la simulation
from time import sleep



#classe Horloge qui gère le temps
class Horloge:
    def __init__(self):
        self.sec = 0
        self.min = 0
        self.hours = 0
        self.en_cours = True


    # fonction qui incrémente le temps
    def temps_jeu(self, lock, state):
        while self.en_cours == True:
            sleep(1)
            with lock:
                self.sec+= state["speed"]
                
                if self.sec//60 > 0:
                    self.sec = self.sec - 60
                    self.min +=1
                    if self.min == 60:
                        self.min = 0
                        self.hours += 1
                            
    
    # fonction qui renvoie le temps en string pour l'afficher
    def time_str(self):
        if self.sec < 10:
            str_sec = "0" + str(self.sec)
        else:
            str_sec = str(self.sec)

        if self.min < 10:
            str_min = "0" + str(self.min)
        else:
            str_min = str(self.min)

        if self.hours != 0:
            string = str(self.hours) + ":" + str_min + ":" + str_sec
        else:
            string = str_min + ":" + str_sec

        return string



    # fonction qui renvoie le temps en secondes actuel pour la génération en cours
    def get_actual_time(self):
        return self.hours * 3600 + self.min * 60 + self.sec


    # fonction qui reset le temps
    def reset_time(self):
        self.sec = 0
        self.min = 0
        self.hours = 0

    #fonction qui restaure le temps depuis une save
    def recover_time(self, time_sec):
        self.hours = time_sec//3600
        self.min = (time_sec - self.hours*3600)//60
        self.sec = time_sec - self.hours*3600 - self.min*60

                


