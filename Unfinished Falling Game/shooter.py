import pygame
import random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('crosshair.png', -1)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def shoot(self, target):
        hitbox = self.rect.inflate(-5, -5)
        return hitbox.colliderect(target.rect)


screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w
pygame.display.set_caption('Shooter')
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

star_field_slow = []

for slow_stars in range(5):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_slow.append([star_loc_x, star_loc_y])

WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
                                 
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

    pygame.display.update()

    clock.tick(30)

pygame.quit()
