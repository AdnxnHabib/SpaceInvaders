import pygame 
import random


class Player(pygame.sprite.Sprite): # inherit from the sprite class
    def __init__(self, groups):
        super().__init__(groups) # sprite gets added to the group automatically
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.player_direction = pygame.math.Vector2(0, 0)
        self.player_speed = 300
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
    
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.player_speed * dt

        recent_keys = pygame.key.get_just_pressed() # returns the bolean list ONLY for the frame the button was pressed. 
        if recent_keys[pygame.K_SPACE]:
            print("fire laser")

class Star(pygame.sprite.Sprite):
     def __init__(self, groups, surf):
        super().__init__(groups) # sprite gets added to the group automatically
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # returns a Surface object
clock = pygame.time.Clock()
running = True

# Surface  - surfaces are essentially objects that we put on the screen, can be shapes, images, or texts
# display surface vs surface - the display surface is essentially the main screen and there is only one of it, where there can be multiple surfaces

surf = pygame.Surface((300, 20)) # rectangle, the beginning coordinates are at the top left of the rectangle

all_sprites = pygame.sprite.Group()
star_surf =  pygame.image.load('images/star.png').convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)


star_surf = pygame.image.load('images/star.png').convert_alpha()
star_positions = [
    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load('images/laser.png').convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

# TITLE 
pygame.display.set_caption('Space Shooter')

while running:
    dt = clock.tick() / 1000 # convert from ms to s 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #update
    all_sprites.update(dt) # calls an update method on all of the spirtes inside the group 

    # draw the game
    screen.fill('red')    
    all_sprites.draw(screen)
    pygame.display.update() # updaates the display every iteraiton

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
