import pygame
import random
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)

letters = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
score = 0
letter_str_list = []
previous_time = 0
time_remaining = 60
num_of_letters = 15

class Letter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, random.randint(64, 128))
        self.letter = random.choice(letters)
        self.image = self.font.render(self.letter, 1, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        self.rect = self.image.get_rect()
        self.speed = random.randint(3, 8)

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

class Crosshair(Letter):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images\\crosshair.png')
        self.rect = self.image.get_rect()
        
    def update(self):
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
    sys.exit()

pygame.init()
pygame.mixer.init()
pygame.joystick.init()
joystick_player_0 = pygame.joystick.Joystick(0)
joystick_player_0.init()
joystick_player_1 = pygame.joystick.Joystick(1)
joystick_player_1.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
pygame.mouse.set_visible(0)

crosshair_x_y = [round(screen_width / 2, 0), round(screen_height / 2, 0)]

laser_sound = pygame.mixer.Sound('audio\\laser.ogg')
wrong_sound = pygame.mixer.Sound('audio\\wrong.ogg')
explosion_image = pygame.image.load('images\\explosion.png')

letter_a = pygame.mixer.Sound('audio\\A.ogg')
letter_b = pygame.mixer.Sound('audio\\B.ogg')
letter_c = pygame.mixer.Sound('audio\\C.ogg')
letter_d = pygame.mixer.Sound('audio\\D.ogg')
letter_e = pygame.mixer.Sound('audio\\E.ogg')
letter_f = pygame.mixer.Sound('audio\\F.ogg')
letter_g = pygame.mixer.Sound('audio\\G.ogg')
letter_h = pygame.mixer.Sound('audio\\H.ogg')
letter_i = pygame.mixer.Sound('audio\\I.ogg')
letter_j = pygame.mixer.Sound('audio\\J.ogg')
letter_k = pygame.mixer.Sound('audio\\K.ogg')
letter_l = pygame.mixer.Sound('audio\\L.ogg')
letter_m = pygame.mixer.Sound('audio\\M.ogg')
letter_n = pygame.mixer.Sound('audio\\N.ogg')
letter_o = pygame.mixer.Sound('audio\\O.ogg')
letter_p = pygame.mixer.Sound('audio\\P.ogg')
letter_q = pygame.mixer.Sound('audio\\Q.ogg')
letter_r = pygame.mixer.Sound('audio\\R.ogg')
letter_s = pygame.mixer.Sound('audio\\S.ogg')
letter_t = pygame.mixer.Sound('audio\\T.ogg')
letter_u = pygame.mixer.Sound('audio\\U.ogg')
letter_v = pygame.mixer.Sound('audio\\V.ogg')
letter_w = pygame.mixer.Sound('audio\\W.ogg')
letter_x = pygame.mixer.Sound('audio\\X.ogg')
letter_y = pygame.mixer.Sound('audio\\Y.ogg')
letter_z = pygame.mixer.Sound('audio\\Z.ogg')

letter_dict = {"A":letter_a, "B":letter_b, "C":letter_c, "D":letter_d, "E":letter_e,
               "F":letter_f, "G":letter_g, "H":letter_h, "I":letter_i, "J":letter_j,
               "K":letter_k, "L":letter_l, "M":letter_m, "N":letter_n, "O":letter_o,
               "P":letter_p, "Q":letter_q, "R":letter_r, "S":letter_s, "T":letter_t,
               "U":letter_u, "V":letter_v, "W":letter_w, "X":letter_x, "Y":letter_y,
               "Z":letter_z}

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

letter_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(30):
    letter = Letter()

    letter.rect.x = random.randrange(screen_width)
    letter.rect.y = random.randrange(screen_height)

    letter_str_list.append(letter.letter)
    
    letter_list.add(letter)
    all_sprites_list.add(letter)

sel_letters = random.sample(letter_str_list, num_of_letters)
current_letter = sel_letters.pop()

crosshair = Crosshair()
all_sprites_list.add(crosshair)

done = False

clock = pygame.time.Clock()

while not done:
    if pygame.time.get_ticks() - previous_time >= 1000:
        previous_time = pygame.time.get_ticks()
        time_remaining -= 1
        letter_dict[current_letter].play()
        if time_remaining == 0:
            done = True
    # player one
    if (abs(joystick_player_0.get_axis(0)) > 0.1 or abs(joystick_player_0.get_axis(1)) > 0.1):
        lx_axis = round(30 * joystick_player_0.get_axis(0), 0)
        ly_axis = round(30 * joystick_player_0.get_axis(1), 0)
        crosshair_x_y[0] += lx_axis
        crosshair_x_y[1] += ly_axis
    if (abs(joystick_player_0.get_axis(3)) > 0.1 or abs(joystick_player_0.get_axis(4)) > 0.1):
        rx_axis = round(30 * joystick_player_0.get_axis(4), 0)
        ry_axis = round(30 * joystick_player_0.get_axis(3), 0)
        crosshair_x_y[0] += rx_axis
        crosshair_x_y[1] += ry_axis
    if abs(joystick_player_0.get_axis(2)) > 0.1:
        letter_hit_list = pygame.sprite.spritecollide(crosshair, letter_list, False)
        if len(letter_hit_list) > 0:
            screen.blit(explosion_image, (crosshair.rect.x - 60, crosshair.rect.y - 60))
            pygame.display.update()
            for letter in letter_hit_list:
                all_sprites_list.remove(letter)
                letter_list.remove(letter)
                if letter.letter == current_letter:
                    laser_sound.play()
                    if len(sel_letters) > 0:
                        current_letter = sel_letters.pop()
                    else:
                        done = True
                    score += 1
                else:
                    wrong_sound.play()
                    if len(sel_letters) > 0:
                        current_letter = sel_letters.pop()
                    else:
                        done = True
                    score -= 1
    # player two
    if (abs(joystick_player_1.get_axis(0)) > 0.1 or abs(joystick_player_1.get_axis(1)) > 0.1):
        lx_axis = round(30 * joystick_player_0.get_axis(0), 0)
        ly_axis = round(30 * joystick_player_0.get_axis(1), 0)
        crosshair_x_y[0] += lx_axis
        crosshair_x_y[1] += ly_axis
    if (abs(joystick_player_1.get_axis(3)) > 0.1 or abs(joystick_player_1.get_axis(4)) > 0.1):
        rx_axis = round(30 * joystick_player_0.get_axis(4), 0)
        ry_axis = round(30 * joystick_player_0.get_axis(3), 0)
        crosshair_x_y[0] += rx_axis
        crosshair_x_y[1] += ry_axis
    if abs(joystick_player_1.get_axis(2)) > 0.1:
        letter_hit_list = pygame.sprite.spritecollide(crosshair, letter_list, False)
        if len(letter_hit_list) > 0:
            screen.blit(explosion_image, (crosshair.rect.x - 60, crosshair.rect.y - 60))
            pygame.display.update()
            for letter in letter_hit_list:
                all_sprites_list.remove(letter)
                letter_list.remove(letter)
                if letter.letter == current_letter:
                    laser_sound.play()
                    if len(sel_letters) > 0:
                        current_letter = sel_letters.pop()
                    else:
                        done = True
                    score += 1
                else:
                    wrong_sound.play()
                    if len(sel_letters) > 0:
                        current_letter = sel_letters.pop()
                    else:
                        done = True
                    score -= 1
                    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

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
