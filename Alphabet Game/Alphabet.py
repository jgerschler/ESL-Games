import pygame
import random

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)
YELLOW = (230,230,0)
RED = (255,0,0)
BLUE = (0,0,255)
BROWN = (97,65,38)

soundwinfile = "audio\\ping.ogg"
soundlossfile = "audio\\buzzer.ogg"

finished = False

points = 0
game_time = 60
previous_time = 0
time_remaining = 60
score = 0
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'




def new_game(alphabet, score):
    # fix these colors
    time_text = display_font.render(str(time_remaining), 1, (148, 0, 201))
    score_text = display_font.render(str(score), 1, (255, 0, 0))
    letter = display_font.render(alphabet[random.randint(0, 25)], 1, (255, 0, 0))
    display.fill(WHITE)
    display.blit(time_text, rect_time)
    display.blit(score_text, rect_score)
    display.blit(letter, rect_letter)

    pygame.display.update()

    return


def new_letter(alphabet, score):
    # fix these colors
    time_text = display_font.render(str(time_remaining), 1, (148, 0, 201))
    score_text = display_font.render(str(score), 1, (255, 0, 0))
    letter = display_font.render(alphabet[random.randint(0, 25)], 1, (255, 0, 0))
    display.fill(WHITE)
    display.blit(time_text, rect_time)
    display.blit(score_text, rect_score)
    display.blit(letter, rect_letter)

    pygame.display.update()

    return


pygame.init()
pygame.mixer.init()

soundwin = pygame.mixer.Sound(soundwinfile)
soundloss = pygame.mixer.Sound(soundlossfile)

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_width = display.get_width()
display_height = display.get_height()

display_font = pygame.font.Font(None, 48)
rect_letter = pygame.Rect((20, 50, display_width - 20, 388))
rect_score = pygame.Rect((display_width - 50, 50, 50, 50))
rect_time = pygame.Rect((display_width - 50, 0, 50, 50))

display.fill(WHITE)

pygame.display.update()

clock = pygame.time.Clock()

while not finished:
    if pygame.time.get_ticks() - previous_time >= 1000:
        previous_time = pygame.time.get_ticks()
        time_remaining -= 1
        if time_remaining == 0:
            display.fill(WHITE)
            score_text = display_font.render("SCORE: " + str(score), 1, (148, 0, 201))
            display.blit(score_text, (display_width / 2, display_height / 2))
            pygame.display.update()
            time.sleep(5)
            finished = True
    time_text = display_font.render(str(time_remaining), 1, (148, 0, 201))
    score_text = display_font.render(str(score), 1, (255, 0, 0))
    display.fill(WHITE, rect_time)
    display.fill(WHITE, rect_score)
    display.blit(time_text, rect_time)
    display.blit(score_text, rect_score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                new_game(alphabet, score)
            if event.key == pygame.K_a:
                score += 1
                new_letter()


    clock.tick(30)        
    pygame.display.update()

pygame.quit()
