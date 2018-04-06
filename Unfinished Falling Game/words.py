import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)

class Word(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.words = ['eat','talk','watch','walk',
                'work','sleep','sing','red',
                'orange','yellow','green','blue',
                'purple']
        self.font = pygame.font.Font(None, random.randint(16, 96))
        self.word = random.choice(self.words)
        self.image = self.font.render(self.word, 1, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        self.rect = self.image.get_rect()
        self.time = None

    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)

    def update(self):
        self.rect.y += 6
        if self.rect.y > screen_height:
            self.reset_pos()


class Crosshair(Word):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images\\crosshair.png')
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

laser_sound = pygame.mixer.Sound('audio\\laser.ogg')
explosion_sound = pygame.mixer.Sound('audio\\explosion.ogg')
explosion_image = pygame.image.load('images\\explosion.png')

font = pygame.font.Font(None, 128)

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

word_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(20):
    word = Word()

    word.rect.x = random.randrange(screen_width)
    word.rect.y = random.randrange(screen_height)

    word_list.add(word)
    all_sprites_list.add(word)

crosshair = Crosshair()
all_sprites_list.add(crosshair)

done = False

clock = pygame.time.Clock()
score = 0
previous_time = 0
time_remaining = 60

adjectives = ['red','orange','yellow','green','blue','purple']
verbs = ['eat','talk','watch','walk','work','sleep','sing']

while not done:
    if pygame.time.get_ticks() - previous_time >= 1000:
        previous_time = pygame.time.get_ticks()
        time_remaining -= 1
        if time_remaining < 0:
            done = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            word_hit_list = pygame.sprite.spritecollide(crosshair, word_list, False)
            if len(word_hit_list) > 0:
                explosion_sound.play()
                screen.blit(explosion_image, (crosshair.rect.x - 60, crosshair.rect.y - 60))
                pygame.display.update()
                for word in word_hit_list:
                    all_sprites_list.remove(word)
                    word_list.remove(word)
                    if word.word in verbs:
                        print("you killed a verb!")
                        score += 1
                    else:
                        print("argh! you killed an adjective")
                        score += 2
            else:
                laser_sound.play()

    screen.fill(BLACK)
    time_text = font.render(str(time_remaining), 1, (148, 0, 201))
    score_text = font.render(str(score), 1, (255, 0, 0))
    screen.blit(time_text, (0, 100))
    screen.blit(score_text, (0, 0))
                
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
