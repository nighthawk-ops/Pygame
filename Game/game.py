import pygame
from character import Player        # get player code to be used in game loop

# initializes game
pygame.init()

# window variables
windowWidth = 800
windowHeight = 640 
window = pygame.display.set_mode((windowWidth,windowHeight))
title = pygame.display.set_caption("Battle-Bytes")
clock = pygame.time.Clock()
icon = pygame.image.load("assests/images/icon/muay-thai.png")   # variabe that holds the icon image.
pygame.display.set_icon(icon) # loads the icon onto the window.

#background image (images should be loaded outside main loop)
bgImage = pygame.image.load("assests/images/background/dojo.png").convert_alpha()
def draw_bg():
    scaledBg = pygame.transform.scale(bgImage, (windowWidth, windowHeight)) # scales bg to screen size
    window.blit(scaledBg, (0,0))

# load player images
playerOne_img = pygame.image.load("assests/images/character/demo/action.png").convert_alpha()
playerTwo_img = pygame.image.load("assests/images/character/demo/man.png").convert_alpha()

#Colors
RED = (255, 0, 0)   
DARKRED = (132, 22, 23)
WHITE = (255,255,255)


# Players health bar
def healthBar(health, x, y):
    ratio = health/100
    pygame.draw.rect(window, WHITE, (x-1, y-1, 252, 27))
    pygame.draw.rect(window, DARKRED, (x, y, 250, 25))
    pygame.draw.rect(window, RED, (x, y, 250*ratio, 25)) 

# player instances
playerOne = Player(80, 468)
playerTwo = Player(580, 468)

#Game loop
run = True
while run:
    
    clock.tick(60)                      # setting FPS
    
    window.fill((14,219,240))           # screen background
    draw_bg()                           # draws background image
    
    #move players
    playerOne.movePlayer(window,playerTwo) 
    
    #draw player stats
    healthBar(playerOne.health, 20, 20)
    healthBar(playerTwo.health, 520, 20)
    
    #draw fighters
    playerOne.drawPlayer(window)
    playerTwo.drawPlayer(window)
    
    
    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # quit event when x in top corner pressed.
            run = False
    
    
    pygame.display.update()             # updates screen inorder to see changes.


pygame.quit()                           # quit pygame.