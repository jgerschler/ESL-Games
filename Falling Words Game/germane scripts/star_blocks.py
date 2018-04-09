import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Star(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        self.image = pygame.image.load('star.png')
        self.rect = self.image.get_rect()

    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)

    def update(self):
        self.rect.y += 2
        if self.rect.y > screen_height:
            self.reset_pos()


class Crosshair(Star):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('crosshair.png')
        self.rect = self.image.get_rect()
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_width()
pygame.mouse.set_visible(0)

laser_sound = pygame.mixer.Sound('laser.ogg')
explosion_sound = pygame.mixer.Sound('explosion.ogg')
explosion_image = pygame.image.load('explosion.png')

star_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(10):
    star = Star()

    star.rect.x = random.randrange(screen_width)
    star.rect.y = random.randrange(screen_height)

    star_list.add(star)
    all_sprites_list.add(star)

crosshair = Crosshair()
all_sprites_list.add(crosshair)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            star_hit_list = pygame.sprite.spritecollide(crosshair, star_list, False)
            if len(star_hit_list) > 0:
                explosion_sound.play()
                screen.blit(explosion_image, (crosshair.rect.x - 60, crosshair.rect.y - 60))
                pygame.display.update()
                pygame.time.delay(300)
                for star in star_hit_list:
                    score += 1
                    print(score)
                    star.reset_pos()
            else:
                laser_sound.play()

    screen.fill(BLACK)
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    clock.tick(20)
    pygame.display.update()

pygame.quit()
