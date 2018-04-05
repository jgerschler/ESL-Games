import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)

class Star(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.words = ['eat','talk','watch','walk',
                'work','sleep','sing','red',
                'orange','yellow','green','blue',
                'purple']
        self.font = pygame.font.Font(None, 32)
        self.word = random.choice(self.words)
        self.image = self.font.render(self.word, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.time = None
        self.dead = False

    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)

    def update(self):
        if self.dead:
            self.rect.x, self.rect.y = -100, -100
        else:
            self.rect.y += 6
            if self.rect.y > screen_height:
                self.reset_pos()
##        if self.time is not None:
##            if pygame.time.get_ticks() - self.time >= 1000:
##                print(self.word)


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

star_field_slow = []
star_field_medium = []

for slow_stars in range(60):
    star_loc_x = random.randrange(0, screen_width)
    star_loc_y = random.randrange(0, screen_height)
    star_field_slow.append([star_loc_x, star_loc_y])
    
for medium_stars in range(60):
    star_loc_x = random.randrange(0, screen_width)
    star_loc_y = random.randrange(0, screen_height)
    star_field_medium.append([star_loc_x, star_loc_y])

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
adjectives = ['red','orange','yellow','green','blue','purple']
verbs = ['eat','talk','watch','walk','work','sleep','sing']

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
                star.time = pygame.time.get_ticks()
                for star in star_hit_list:
                    all_sprites_list.remove(star)
                    star_list.remove(star)
                    if star.word in verbs:
                        score += 1
                    else:
                        print("argh! you killed an adjective")
                    print(score)
##                    star.reset_pos()
            else:
                laser_sound.play()

    screen.fill(BLACK)
                
    for bg_star in star_field_slow:
        bg_star[1] += 1
        if bg_star[1] > screen_height:
            bg_star[0] = random.randrange(0, screen_width)
            bg_star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, DARKGREY, bg_star, 3)

    for bg_star in star_field_medium:
        bg_star[1] += 4
        if bg_star[1] > screen_height:
            bg_star[0] = random.randrange(0, screen_width)
            bg_star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, LIGHTGREY, bg_star, 3)

    
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    clock.tick(30)
    pygame.display.update()

pygame.quit()
