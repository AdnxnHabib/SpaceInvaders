import pygame 
import random

pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # returns a Surface object
clock = pygame.time.Clock()
running = True

# Surface  - surfaces are essentially objects that we put on the screen, can be shapes, images, or texts
# display surface vs surface - the display surface is essentially the main screen and there is only one of it, where there can be multiple surfaces

surf = pygame.Surface((300, 20)) # rectangle, the beginning coordinates are at the top left of the rectangle

# Images

# Convert - for performance
# If image has no transparent pixels, use .convert
# otherwise, use .convert_alpha

player_surf = pygame.image.load('images/player.png').convert_alpha()
player_rect = player_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_x = 100
player_direction = pygame.math.Vector2(1, 1)
player_speed = 1000


star_surf = pygame.image.load('images/star.png').convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

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
    
    screen.fill('red')
    for pos in star_positions:
        screen.blit(star_surf, pos) 
    
    screen.blit(meteor_surf, meteor_rect)
    screen.blit(laser_surf, laser_rect)
    if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
        player_direction.y *= -1
    if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        player_direction.x *= -1
    player_rect.center += player_direction * player_speed * dt
    
    screen.blit(player_surf, player_rect)  # identifies the coordinates at which the top-left of the rectangle should spawn
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
