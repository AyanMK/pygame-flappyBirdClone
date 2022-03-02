from email import message
import random
import sys
from turtle import back, width
from pip import main          # use exit to exit the program
import pygame
from pygame.locals import*    # Basick pygame imports

#Global Variables for the game
FPS = 30
screen_width = 1200
screen_hight = 800
screen = pygame.display.set_mode((screen_width,screen_hight))
ground_y = screen_hight*0.8

game_sprites = {}
game_sounds = {}

plane ='gallery/image/plane.png'
background = 'gallery/image/background.png'
building1 = 'gallery/image/building1.png'
building2 = 'gallery/image/building2.png'
plane2 = 'gallery/image/plane2.png'

message = ''

def welcome_screen():
    #Show welcome image on the screen
    plane_x = int(screen_width/5)
    plane_y = int((screen_hight - game_sprites['plane'].get_height())/2)
    
    messagex = int((screen_width - game_sprites['message'].get_width())/2)
    messagey = int(screen_hight*0.13)
     
    base_x = 0
    
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            #If the user press space or up key, start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                screen.blit(game_sprites['background'],(0,0,))
                screen.blit(game_sprites['plane'],(plane_x,plane_y))
                #screen.blit(game_sprites['message'],(messagex,messagey))
                #screen.blit(game_sprites['base'],(basex,ground_y))
                pygame.display.update()
                FPSlock.tick(FPS)
       

#main game function -------------------------------------------->
def main_game():
    score = 0
    plane_x = int(screen_width/5)
    plane_y = int(screen_hight/2)
    base_x = 0
    
    #creating building on the screen
    new_building_1 = lower_object()
    new_plane_2 = upper_object()
    
    #list of plane2 (upper object)
    upperObjects = [
        {'x':int(screen_width+200),'y':new_plane_2['y']},
        {'x':screen_width+200+(screen_width/2),'y':new_plane_2['y']}
    ]
        
    #list of building1 (lower object)
    lowerObjects = [
        {'x':screen_width+200,'y':new_building_1['y']},
        {'x':screen_width+200+(screen_width/2),'y':new_building_1['y']}
    ]
    
    building1_velocity_x = -4
    plane2_velocity_x = -4
    
    plane_velocity_y = -6
    plane_min_velocity_y = -8
    plane_max_velocity_y = 6
    plane_acceleration_y = 1
    
    plane_going_acceleration = -8
    plane_propeller_move = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if plane_y > 0:
                    plane_velocity_y = plane_going_acceleration
                    plane_propeller_move = True
                    #game_sounds[''].play()
                    
        crashTest = isCollide(plane_x,plane_y,upperObjects,lowerObjects)      
        #This function will return true if the plane is crashed
        if crashTest:
            
            return

        #check for score
        plane_mid_position = plane_x + game_sprites['plane'].get_width()/2
        """
        for plane2 in upperObjects:
            plane2_mid_position = plane2['x'] + game_sprites['plane2'].get_width()/2
            
            if plane2_mid_position <= plane_mid_position < plane2_mid_position + 4:
                score+=1
                print(f"Your score is {score}")
                #game_sounds[''].play()      #point sound
        """        
        for building1 in lowerObjects:
            building1_mid_position = building1['x'] + game_sprites['building1'].get_width()/2
            
            if building1_mid_position <= plane_mid_position < building1_mid_position + 4:
                score+=1
                #print(f"Your score is {score}")
                #game_sounds[''].play()      #point sound
            
        if plane_velocity_y < plane_max_velocity_y and not plane_propeller_move:
            plane_velocity_y+=plane_acceleration_y
            
        if plane_propeller_move:
            plane_propeller_move = False
    
        planeHeight = game_sprites['plane'].get_height()
        plane_y = plane_y + min(plane_velocity_y,screen_hight - plane_y - planeHeight)
         
        # move game object to the left
        for upperObject, lowerObject in zip(upperObjects,lowerObjects):
            upperObject['x'] += plane2_velocity_x
            lowerObject['x'] += building1_velocity_x
        
        
        #Add a new object when the  first boject is about to cross the leftmost part of the screen
        if 0 < upperObjects[0]['x']<5:
            upNewObject = upper_object()
            upperObjects.append(upNewObject)
        
        if 0 < lowerObjects[0]['x']<5:
            lowNewObject = lower_object()
            lowerObjects.append(lowNewObject)
        
        
        #if object is out of the screen, remove it
        if upperObjects[0]['x'] < - game_sprites['plane2'].get_width():
            upperObjects.pop(0)
            
        if lowerObjects[0]['x'] < - game_sprites['building1'].get_width():
            lowerObjects.pop(0)
        
        
        # lets blit our sprites now
        screen.blit(game_sprites['background'],(0,0))
        for upperObject, lowerObject in zip(upperObjects,lowerObjects):
            screen.blit(game_sprites['plane2'],(upperObject['x'],upperObject['y']))
            screen.blit(game_sprites['building1'],(lowerObject['x'],lowerObject['y']))
        
        screen.blit(game_sprites['plane'],(plane_x,plane_y))
        
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprites['numbers'][digit].get_width()
        x_offset = (screen_width - width)/2    
        
        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit],(x_offset,screen_hight*0.05))
            x_offset += game_sprites['numbers'][digit].get_width()
        
        pygame.display.update()
        FPSlock.tick(FPS)

def isCollide(plane_x,plane_y,upperObjects,lowerObjects):
    """ 
    if plane_y>screen_hight or plane_y<0:
        return True
    """ 
    """       
    for building1 in lowerObjects:
        if (plane + game_sprites['plane'].get_height() > building1['y']) and abs(plane_x - building1['x'])<game_sprites['building1'].get_width():
            return True
    """
    return False   

def lower_object():
    #generate position of building
    building1_height = game_sprites['building1'].get_height()
    #plane space to move
    offset = screen_hight/3
    lower_object_x = int(screen_width + random.randint(10,20))
    lower_object_y = int(offset+random.randrange(230,int(screen_hight - (screen_hight)/2)))
    building1_position = {'x':lower_object_x,'y':lower_object_y}
    return building1_position
    
def upper_object():
    #generate position 2nd plane
    offset = screen_hight/3
    plane2_height = game_sprites['plane2'].get_height()
    upper_object_x = int(screen_width + random.randrange(0,15))
    upper_object_y = int(plane2_height - (offset+random.randrange(0,int(screen_hight - screen_hight/2)) + offset))
    plane2_position = {'x':upper_object_x,'y':upper_object_y}
    return plane2_position
 

if __name__=="__main__":
    pygame.init()       #initialize all pygame's modules
    FPSlock = pygame.time.Clock()
    pygame.display.set_caption('Plane crush')
    game_sprites['numbers']=(
        pygame.image.load('gallery/image/0.png').convert_alpha(),
        pygame.image.load('gallery/image/1.png').convert_alpha(),
        pygame.image.load('gallery/image/2.png').convert_alpha(),
        pygame.image.load('gallery/image/3.png').convert_alpha(),
        pygame.image.load('gallery/image/4.png').convert_alpha(),
        pygame.image.load('gallery/image/5.png').convert_alpha(),
        pygame.image.load('gallery/image/6.png').convert_alpha(),
        pygame.image.load('gallery/image/7.png').convert_alpha(),
        pygame.image.load('gallery/image/8.png').convert_alpha(),
        pygame.image.load('gallery/image/9.png').convert_alpha()
    )
    
    game_sprites['message']=pygame.image.load('gallery/image/plane.png')
    game_sprites['base']=pygame.image.load('gallery/image/background.png')
    game_sprites['background']=pygame.image.load('gallery/image/background.png')
    
    game_sprites['plane2']=pygame.image.load('gallery/image/plane2.png')
    game_sprites['building1']=pygame.image.load('gallery/image/building1.png')
    game_sprites['building2']=pygame.image.load('gallery/image/building2.png')

    
    """
    #Game sounds
    game_sounds['die']=pygame.mixer.Sound()                 #need to complet
    game_sounds['hit']=pygame.mixer.Sound()
    game_sounds['point']=pygame.mixer.Sound()
    game_sounds['up']=pygame.mixer.Sound()
    """
    game_sprites['background']=pygame.image.load(background).convert()
    game_sprites['plane']=pygame.image.load(plane).convert_alpha()
    
    while True:
        welcome_screen()     #Show welcome screen to the use untill player presses a button
        main_game()          #Main game function
    