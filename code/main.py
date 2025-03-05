import pygame 
import random



class Player(pygame.sprite.Sprite): # inherit from the sprite class
    def __init__(self, groups):
        super().__init__(groups) # sprite gets added to the group automatically
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.player_direction = pygame.math.Vector2(0, 0)
        self.player_speed = 300

        # cooldown 

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400 # 2 seconds
    
    def laser_timer(self):
        if not self.can_shoot: 
            current_time = pygame.time.get_ticks() # the amount of time passed since pygame.init
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
    
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.player_speed * dt

        recent_keys = pygame.key.get_just_pressed() # returns the bolean list ONLY for the frame the button was pressed. 
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()   


class Star(pygame.sprite.Sprite):
     def __init__(self, groups, surf):
        super().__init__(groups) # sprite gets added to the group automatically
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
        self.laser_direction = pygame.math.Vector2(0, -1)
        self.laser_speed = 300
       
    def update(self, dt):
        self.rect.center += self.laser_direction * self.laser_speed * dt
        if self.rect.bottom < 0: 
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.meteor_direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.meteor_speed = random.randint(400, 500)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
       
    def update(self, dt):
        self.rect.center += self.meteor_direction * self.meteor_speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime: 
            self.kill()

def collision():
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprites:
        print(collision_sprites[0])
        running = False
    
    for laser in laser_sprites: 
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites: 
            laser.kill()

# General Setup
pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # returns a Surface object
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
running = True
 
# Imports
# Surface  - surfaces are essentially objects that we put on the screen, can be shapes, images, or texts
# display surface vs surface - the display surface is essentially the main screen and there is only one of it, where there can be multiple surfaces
star_surf =  pygame.image.load('images/star.png').convert_alpha()
laser_surf =  pygame.image.load('images/laser.png').convert_alpha()
meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)

# custom events -> meteor event 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)



while running:
    dt = clock.tick() / 1000 # convert from ms to s 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == meteor_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), meteor_surf, (x,y))
    
    #update  
    all_sprites.update(dt) # calls an update method on all of the spirtes inside the group  
    collision()
        
   
    # draw the game
    screen.fill('red')    
    all_sprites.draw(screen)
    pygame.display.update() # updaates the display every iteraiton

    # test collision 


pygame.quit()


'''
If in your game loop you have:

x = 100
while running: 
screen.fill('red') # display surface
x += 0.1
screen.blit(surf, (x, 200))

This will create an animation. However, if I remove the screen.fill(red), the effect is that I am essentially creating a new rectangle on top of my old rectangle.



'''

'''
Delta Time
 - the time it takes for the computer to render the current frame 
 e.g 60 frames / second -> 0.017 seconds to render 1 frame 


'''


'''
Why we normalize

 new_position = player_rect.center + (1 * 300 * dt, 1 * 300 * dt) if player_speed is (1,1)
 effectievly, we are moving diagonally at a higher speed than 300 pixels. (424 pixels whihc is the hypoteneuse), so we normalize

 So if we normalize the vector (1, 1) -> that trasnforms it to (0.71, 0.71)
 Movement = (0.71 * 300 * dt, 0.71 & 300 * dt)
 Magnitude = sqrt((212 *dt)^2 + (212 * dt)^2) = 300, which is our desired speed

'''

''' 
Interval Timer  
- a timer that triggers every x seconds 
- first create an envent and then set a timer with that evetn 
- cpature the event in the event loop 

Custom Timer 
- capture the time since the start of the game
- get a starting point and measure the time passed since that point 
'''