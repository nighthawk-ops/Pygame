import pygame

class Player():
    def __init__(self, x, y, flip, data, spriteSheet, animation_steps):
        self.size= data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect(x, y, 128, 128)
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attackType = 0
        self.attackCooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.flip = flip
        self.animationList = self.loadImages(spriteSheet, animation_steps)
        #0 = idle, 1 = run, 2 = jump, 3 = attack_1, 4 = attack_2, 5 = getting hit, 6 = dead
        self.action = 0                 # tells us the action so we know which animation to play
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()   # gets the time character was first created
        
    
    def loadImages(self, spriteSheet, animationSteps):
        #extract images from sprite sheets
        animationList = []
        for y, animation in enumerate(animationSteps):
            temp_img_list = []               #list to store each piece of the image that is cut out   
            for x in range(animation):
                temp_img = spriteSheet.subsurface(x * self.size, y * self.size, self.size, self.size)     # cuts out an image of our defined size from the spritesheet 
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self. image_scale)))
            animationList.append(temp_img_list)   # collects all the images of each animation
        return animationList
            
    def movePlayer(self, window, target):
        velocity = 5                    # speed of player
        dx = 0                          # change in x coordinate
        dy = 0                          # change in y coordinate
        self.running = False
        self.attackType = 0
        
        gravity = 2
        keys = pygame.key.get_pressed() # gets keys pressed
        
        # movement only possible if not attacking
        if self.attacking == False:
            #movement
            if keys[pygame.K_a]:            # press a to go left
                dx = -velocity
                self.running = True
                
            if keys[pygame.K_d]:            # press b to go right
                dx += velocity
                self.running = True
                
            
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
            
        # apply cooldown
        if self.attackCooldown > 0:
            self.attackCooldown -= 1
        
           
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
        
    
    
    # updates animation
    def update(self):
        
        #check action
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.updateAction(6)
        elif self.hit == True:
            self.updateAction(5)
        elif self.attacking == True:
            if self.attackType == 1:
                self.updateAction(3)
            elif self.attackType == 2:
                self.updateAction(4)
        elif self.jump == True:
            self.updateAction(2)
        elif self.running == True:
            self.updateAction(1)
        else:
            self.updateAction(0)
            
            
        
        animationCooldown = 120 # milliseconds
        # update animation image
        self.image = self.animationList[self.action][self.frameIndex]
        # check if enough time has passed to switch image
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        #check if animation is finished
        if self.frameIndex >= len(self.animationList[self.action]):
            #check if play is dead
            if self.alive == False:
                self.frameIndex = len(self.animationList[self.action]) - 1
            else:
                self.frameIndex = 0
                #check if attack action is complete
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attackCooldown = 50
                #check for damage
                if self.action == 5:
                    self.hit = False
                    # if player is hit in the middle of an attack their attack stops
                    self.attacking = False
                    self.attackCooldown = 50
    
    
    
    
    
    def attack(self, window, target):
        if self.attackCooldown == 0:
            self.attacking = True # movement will stop because attacking isn't set to false again
            hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            #check for contact
            if hitbox.colliderect(target.rect):           #checks for collision to determine effect
                target.health -= 10
                target.hit = True
            
            pygame.draw.rect(window, (0,255,0), hitbox)   #draws hitbox
      
      
      
    def updateAction(self, newAction):
        if newAction != self.action:
            self.action = newAction
            #reset animation index
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()  
        
    
    def drawPlayer(self, window):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(window, (0,0,0), self.rect)
        window.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    
  