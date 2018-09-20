import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)


global words
global score
letters = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
score = 0
previous_time = 0
time_remaining = 60 

class Word(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, random.randint(32, 96))
        self.letter = random.choice(letters)
        self.image = self.font.render(self.letter, 1, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        self.rect = self.image.get_rect()
        self.speed = random.randint(1, 8)

    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)

    def update(self):
        if score > 0:
            self.rect.y += (self.speed * score / 5) + 1
        else:
            self.rect.y += 1
        if self.rect.y > screen_height:
            self.reset_pos()


class Crosshair(Word):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images\\crosshair.png')
        self.rect = self.image.get_rect()
        
    def update(self):
##        pos = pygame.mouse.get_pos()
        self.rect.x = crosshair_x_y[0]
        self.rect.y = crosshair_x_y[1]

def game_over():
    screen.fill(BLACK)
    score_text = font.render("SCORE: " + str(score), 1, (255, 0, 0))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (screen_width / 2, screen_height / 2)
    screen.blit(score_text, score_text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()

    

pygame.init()
pygame.mixer.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
pygame.mouse.set_visible(0)

crosshair_x_y = [round(screen_width / 2, 0), round(screen_height / 2, 0)]

laser_sound = pygame.mixer.Sound('audio\\laser.ogg')
explosion_sound = pygame.mixer.Sound('audio\\explosion.ogg')
scream_sound = pygame.mixer.Sound('audio\\scream.ogg')
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

for i in range(50):
    word = Word()

    word.rect.x = random.randrange(screen_width)
    word.rect.y = random.randrange(screen_height)

    word_list.add(word)
    all_sprites_list.add(word)

crosshair = Crosshair()

all_sprites_list.add(crosshair)

done = False

clock = pygame.time.Clock()




while not done:
    if pygame.time.get_ticks() - previous_time >= 1000:
        previous_time = pygame.time.get_ticks()
        time_remaining -= 1
        if time_remaining == 0:
            done = True
    if (abs(joystick.get_axis(0)) > 0.1 or abs(joystick.get_axis(1)) > 0.1):
        lx_axis = round(30 * joystick.get_axis(0), 0)
        ly_axis = round(30 * joystick.get_axis(1), 0)
        crosshair_x_y[0] += lx_axis
        crosshair_x_y[1] += ly_axis
    if (abs(joystick.get_axis(3)) > 0.1 or abs(joystick.get_axis(4)) > 0.1):
        rx_axis = round(30 * joystick.get_axis(4), 0)
        ry_axis = round(30 * joystick.get_axis(3), 0)
        crosshair_x_y[0] += rx_axis
        crosshair_x_y[1] += ry_axis
    if abs(joystick.get_axis(2)) > 0.1:
        word_hit_list = pygame.sprite.spritecollide(crosshair, word_list, False)
        if len(word_hit_list) > 0:
            screen.blit(explosion_image, (crosshair.rect.x - 60, crosshair.rect.y - 60))
            pygame.display.update()
            for word in word_hit_list:
                all_sprites_list.remove(word)
                word_list.remove(word)
                if word.word in past_participles:
                    explosion_sound.play()
                    score += 1
                else:
                    scream_sound.play()
                    score -= 1
        else:
            laser_sound.play()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
##        if event.type == pygame.MOUSEBUTTONDOWN:

    screen.fill(BLACK)
    time_text = font.render(str(time_remaining), 1, (148, 0, 201))
    score_text = font.render(str(score), 1, (255, 0, 0))
    score_text_rect = score_text.get_rect()
    score_text_rect.topright = (screen_width, 0)
    screen.blit(time_text, (0, 0))
    screen.blit(score_text, score_text_rect)
                
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

game_over()
