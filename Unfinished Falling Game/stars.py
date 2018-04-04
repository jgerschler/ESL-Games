import pygame
import random

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w
pygame.display.set_caption('Window Caption')
clock = pygame.time.Clock()

#create the locations of the stars for when we animate the background
star_field_slow = []
##star_field_medium = []
##star_field_fast = []

for slow_stars in range(5):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_slow.append([star_loc_x, star_loc_y])
    
##for medium_stars in range(3):
##    star_loc_x = random.randrange(0, width)
##    star_loc_y = random.randrange(0, height)
##    star_field_medium.append([star_loc_x, star_loc_y])
##
##for fast_stars in range(1):
##    star_loc_x = random.randrange(0, width)
##    star_loc_y = random.randrange(0, height)
##    star_field_fast.append([star_loc_x, star_loc_y])

#define some commonly used colours
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
                                 
#create the window
pygame.init()

finished = True

while finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Goodbye!")
            finished = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Goodbye!")
            finished = False

    screen.fill(BLACK)

    for star in star_field_slow:
        star[1] += 1
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, DARKGREY, star, 10)

##    for star in star_field_medium:
##        star[1] += 4
##        if star[1] > height:
##            star[0] = random.randrange(0, width)
##            star[1] = random.randrange(-20, -5)
##        pygame.draw.circle(screen, LIGHTGREY, star, 10)
##
##    for star in star_field_fast:
##        star[1] += 8
##        if star[1] > height:
##            star[0] = random.randrange(0, width)
##            star[1] = random.randrange(-20, -5)
##        pygame.draw.circle(screen, WHITE, star, 10)

    #redraw everything we've asked pygame to draw
    pygame.display.update()

    #set frames per second
    clock.tick(30)

#quit gracefully
pygame.quit()
