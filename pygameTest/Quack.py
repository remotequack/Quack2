import pygame
from enum import Enum

class dim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

dimentions = dim(1024, 720)
fps = 30
tireParSecondes = 8
peutTirer = True
delaiSpawn = 500
score = 0

AFFICHAGE_TIMER_EVENT = pygame.USEREVENT + 0
COLLISION_EVENT = pygame.USEREVENT + 1
DELAY_TIRE_EVENT = pygame.USEREVENT + 2
SPAWN_TIMER_EVENT = pygame.USEREVENT + 3

class NafaireTypes(Enum):
    DEFAULT = 0
    JOUEUR = 1
    ENNEMI = 2
    BALLE = 3

class Nafaire:
    def __init__(self, position=(0,0), animation=None, vie=0, dmg=1, vitesseX=0.1, vitesseY=0.1, rect=None, type=NafaireTypes.DEFAULT):
        self.x , self.y = position
        self.anciennePos = position
        self.animation = animation
        self.vie = vie
        self.dmg = dmg   
        self.vitesseX = vitesseX
        self.vitesseY = vitesseY
        self.type = type
        
        if(animation == None): return
        
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))

    """
    .deplacement(x, y): déplace l'objet

    :param x: taux de déplacement sur l'axe x
    :param y: taux de déplacement sur l'axe y
    """
    def deplacement(self, x, y):
        self.anciennePos = (self.x, self.y)
        self.x += x * self.vitesseX
        self.y += y * self.vitesseY
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))
        
        self.detectCollisions()

    def detectCollisions(self):

        if(self.x < 0 or self.x > dimentions.x or self.y < 0 or self.y > dimentions.y): 
            pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=None))        

        if(self.type == NafaireTypes.JOUEUR):
            
            for enemi in enemies:
                if self.rect.colliderect(enemi.rect): 
                    pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=enemi))

        elif(self.type == NafaireTypes.ENNEMI and self.rect.colliderect(Joueur.rect)): 
            pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=Joueur))

        elif(self.type == NafaireTypes.BALLE):
            
            for enemi in enemies:
                
                if self.rect.colliderect(enemi.rect): 
                    pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=enemi))
                    break

class Zimage:
    def _init_(self,image,scale=(0,0),centre=(0,0)):
        self.image= pygame.image.load(str(image)).convert_alpha()
        self.scale= pygame.transform.smoothscale(self.image, scale)
        self.rect= self.scale.get_rect(center=centre)
    
    def affiche(self):
       Fenêtre.blit(self.scale , self.surface )
###
# Affichage() dessine ce qui doit etre affiché grace a pygame. Il es utiliser à la fin du mainloop pour raffraichir la scène  
# 
###
def Affichage():

    Fenêtre.blit(arrièrePlan.animation[0], (0,0))
    
    Fenêtre.blit(Joueur.animation[0], Joueur.rect) #dessine le personnage à l'écran

    for enemi in enemies:
        Fenêtre.blit(enemi.animation[0], enemi.rect)

    for b in balleList:
        Fenêtre.blit(b.animation[0], b.rect)
    
    img = score_im.render('{}'.format(str(score)), True , (255,255,255))
    rect_score_img = score_img.get_rect()
    Fenêtre.blit(score_img, (0,0))
    Fenêtre.blit(img, rect_score_img.center)

    pygame.display.update()
 
"""
tire() crée des balles pour qu'elles soient déplacées ensuite
"""
def tire():
    global peutTirer
    peutTirer = False
    balle = Nafaire([Joueur.rect.centerx, Joueur.rect.top], balleImg, type=NafaireTypes.BALLE, vitesseY=8)
    balleList.append(balle)

    pygame.time.set_timer(DELAY_TIRE_EVENT, int(1000/tireParSecondes), True)

#rajout ennemi
dimx = []
dimy = 10
for i in range(34):
    dimx.append((int(i)*30))

change_dimx = 0

def spawn_enemies():
        
    global change_dimx
        
    enemies.append(Nafaire(( dimx[change_dimx] , dimy ), ennemiImg, type=NafaireTypes.ENNEMI))
            
    change_dimx += 1
    if change_dimx >= 34:
        change_dimx = 0
        #print("1 sec est passée")
#rajout

"""
main(): C'est le point d'entré du programme. Il gère les évenements, les entrées utilisateurs et les déplacements

:returns: 0 si tout c'est bien passé
"""
def main():

    leJeuTourne = True

    global peutTirer
    global score
    global Fenêtre
    global Joueur
    global arrièrePlan
    global bonus
    global enemies
    global balleList
    global balleImg
    global ennemiImg
    global score_img
    global score_im
    global img
    

    #DEBUT DU PROGRAMME
    pygame.init()   #initialisation de pygame
    pygame.display.set_caption("JEU BIEN")  #titre du jeu
    Fenêtre = pygame.display.set_mode((dimentions.x, dimentions.y)) # crée la fenêtre et enregiste sa variable

    arrièrePlan = Nafaire([0,0], [pygame.image.load("background0.png")])
    arrièrePlan.animation[0] = pygame.transform.smoothscale(arrièrePlan.animation[0], (dimentions.x, dimentions.y))

    JoueurImg  = [pygame.transform.smoothscale(pygame.image.load("joueur.png"),(125,108))]
    Joueur = Nafaire([dimentions.x / 2, dimentions.y / 2], JoueurImg, type=NafaireTypes.JOUEUR, vitesseX=5, vitesseY=5)
    

    enemies = list()
    enemies.append(Nafaire([dimentions.x / 2, 5 ], [pygame.image.load("heart.png")], type=NafaireTypes.ENNEMI, vitesseX=4, vitesseY=4))   #cree un ennemi

    balleImg = [pygame.image.load("balleJoueur.png")]
    ennemiImg = [pygame.image.load("quacklenvers.png")]
    balleList = list()
    bonus = Nafaire(dmg=0, vitesseX=0)

    #rajout score
    score_img = pygame.image.load("score_espace.jpg").convert() #c'est le cadre du score
    score_img = pygame.transform.smoothscale(score_img,(100,45))
    score_im = pygame.font.SysFont(None , 30)
    img = score_im.render('{}'.format(str(score)), True , (255,255,255))
    #rajout score

    #crée des evenement à intervalles réguliers
    pygame.time.set_timer(AFFICHAGE_TIMER_EVENT, int(1000/fps))    #crée un évenement tout les 'x' fois par secondes coresspondant au nombre de rafraichissement de la scène que l'on souhaite
    pygame.time.set_timer(SPAWN_TIMER_EVENT, delaiSpawn)    #crée un evenement pour l'apparition des ennemis tout les 'x' ms

    pygame.key.set_repeat(int(1000/fps))#permet d'avoir des evenements pour les touches qui restent appuyées, avec un délai pour éviter de bloquer le programme


    LEFT_CLICK = 1
    keysDown = None

    while leJeuTourne:

        ###gestion des evenements:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:# Change la valeur à False pour terminer le while
                leJeuTourne = False

            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keysDown = pygame.key.get_pressed()

            elif event.type == pygame.MOUSEBUTTONUP: #tire quand on clique avec la souris
                if (event.button == LEFT_CLICK and peutTirer == True): 
                    tire()            

            elif event.type == DELAY_TIRE_EVENT:
                peutTirer = True

            elif event.type == COLLISION_EVENT:

                if(event.collision == None):#collision avec la 'bordure du cadre'
                
                    if(event.source.type == NafaireTypes.JOUEUR or event.source.type == NafaireTypes.ENNEMI):
                        ###corrige la position du joueur ou de l'ennemi pour qu'il ne sorte pas du cadre
                        if event.source.x < 0 : event.source.x = 0
                        if event.source.x > dimentions.x : event.source.x = dimentions.x
                        if event.source.y < 0 : event.source.y = 0
                        if event.source.y > dimentions.y : event.source.y = dimentions.y

                    elif(event.source.type == NafaireTypes.BALLE):
                        ###détruit les balles hors champs
                        if event.source in balleList:
                            balleList.remove(event.source)                

                elif(event.source.type == NafaireTypes.BALLE and event.collision.type == NafaireTypes.ENNEMI):#collision balle ennemi
                    if event.collision in enemies:
                        enemies.remove(event.collision)
                    if event.source in balleList:
                        balleList.remove(event.source)
                    score += 1
                
                elif(event.source.type == NafaireTypes.ENNEMI and event.collision.type == NafaireTypes.JOUEUR) or (event.source.type == NafaireTypes.JOUEUR and event.collision.type == NafaireTypes.ENNEMI):#collision joueur ennemi
                    event.source.x, event.source.y = event.source.anciennePos
                    event.source.rect = event.source.animation[0].get_rect(center=(event.source.x, event.source.y))

            elif event.type == SPAWN_TIMER_EVENT:
                spawn_enemies()

            elif event.type == AFFICHAGE_TIMER_EVENT:
            
                #gestion des déplacement à l'évenement d'affichage pour eviter de bloquer l'affichage ou la file d'évenements avec des déplacements constants
                if(keysDown != None):

                    tmpDeplacementJoueur = dim(0, 0)
       
                    if keysDown[pygame.K_z]:             
                        tmpDeplacementJoueur.y -= 1
                    if keysDown[pygame.K_s]:
                        tmpDeplacementJoueur.y += 1
                    if keysDown[pygame.K_q]:
                        tmpDeplacementJoueur.x -= 1
                    if keysDown[pygame.K_d]:                
                        tmpDeplacementJoueur.x += 1  
                    if (keysDown[pygame.K_SPACE] and peutTirer == True):
                        tire()           
                
                    if(tmpDeplacementJoueur.x != 0 or tmpDeplacementJoueur.y != 0):
                        Joueur.deplacement(tmpDeplacementJoueur.x, tmpDeplacementJoueur.y)

                    keysDown = None

                if(len(enemies) != 0): 
                    for ennemi in enemies:
                        ennemi.deplacement(0, 1)

                for b in balleList:
                    b.deplacement(0, -1)

                Affichage()
    return 0


if __name__ == "__main__":
    main()