import pygame

class Player():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 128, 128)
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attackType = 0
        self.health = 100
        self.flip = False
        
    
    def movePlayer(self, window, target):
        velocity = 5                    # speed of player
        dx = 0                          # change in x coordinate
        dy = 0                          # change in y coordinate
        
        gravity = 2
        keys = pygame.key.get_pressed() # gets keys pressed
        
        # movement only possible if not attacking
        if self.attacking == False:
            #movement
            if keys[pygame.K_a]:            # press a to go left
                dx = -velocity
            if keys[pygame.K_d]:            # press b to go right
                dx += velocity
            
            #jumping
            if keys[pygame.K_w] and self.jump == False: # Press w to jump
                self.vel_y = -30
                self.jump = True
                
            # attacking
            if keys[pygame.K_r] or keys[pygame.K_t]:  # press T or R to attack
                self.attack(window, target)
                if keys[pygame.K_r]:                  
                    self.attackType = 1               # attack type 1 if r is pressed
                if keys[pygame.K_t]:
                    self.attackType = 2               # attack type 1 if r is pressed
            
            
        #update position
        self.vel_y += gravity           # applies gravity to bring character back down  
        dy += self.vel_y                # updates y
        
        self.rect.x += dx               # horizontal position
        self.rect.y += dy               # vertical position
        
        # ensure players face each other
        if target.rect.centerx > self.rect.centerx: # check if opponent is to the right
            self.flip = False
        else:
            self.flip = True 
        
         # Boarder check: resets position if crossed.
        if self.rect.x <= 0:            # left boarder
             self.rect.x = 0            # reset coordinate
        elif self.rect.x>= 672:         # right boarder
            self.rect.x = 672           # reset coordinate
        
        if self.rect.y >= 468:          # ensures character doesn't fall through floor
            self.vel_y = 0
            self.rect.y = 468
            self.jump = False
        
        
    
    def attack(self, window, target):
        self.attacking = True # movement will stop because attacking isn't set to false again
        hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        #check for contact
        if hitbox.colliderect(target.rect):           #checks for collision to determine effect
            target.health -= 10
        
        pygame.draw.rect(window, (0,255,0), hitbox)   #draws hitbox
        
        
    
    def drawPlayer(self, window):
        pygame.draw.rect(window, (0,0,0), self.rect)

    
  