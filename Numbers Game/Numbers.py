##very little logic here since the idea is
##that the instructor will listen to the student's
##pronunciation of the letter of the alphabet
##and manually press a key/button as required
##
##Attempted machine learning solution, but
##wasn't accurate enough!
import pygame
import random
import sys
import time

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (57, 255, 20)
YELLOW = (230,230,0)
RED = (255,0,0)
BLUE = (0,0,255)
BROWN = (97,65,38)

soundwinfile = "audio\\ping.ogg"

finished = False

def new_game():
    clock = pygame.time.Clock()
    previous_time = 0
    time_remaining = 60
    score = 0
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    points = 0
    finished = False
    letter = letter_font.render(alphabet[random.randint(0, 25)], 1, RED)
    letter_rect = letter.get_rect()
    ticks = pygame.time.get_ticks()
    while not finished:
        if pygame.time.get_ticks() - previous_time >= 1000:
            previous_time = pygame.time.get_ticks()
            time_remaining -= 1
            if time_remaining == 0:
                display.fill(WHITE)
                score_text = display_font.render("SCORE: " + str(score), 1, BROWN)
                display.blit(score_text, (display_width / 2, display_height / 2))
                pygame.display.update()
                time.sleep(5)
                finished = True
        time_text = display_font.render(str(time_remaining), 1, BLUE)
        score_text = display_font.render(str(score), 1, RED)
        
        display.fill(WHITE)
        display.blit(time_text, rect_time)
        display.blit(score_text, rect_score)
        letter_rect.center = (display_width / 2, display_height / 2)
        display.blit(letter, letter_rect)
        bartime = pygame.time.get_ticks() - ticks
        if bartime < 3000:
            pygame.draw.rect(display, GREEN, [30, display_height - 80, abs(1 - (bartime / 5000)) * (display_width - 60), 40])
        elif bartime < 4000:
            pygame.draw.rect(display, YELLOW, [30, display_height - 80, abs(1 - (bartime / 5000)) * (display_width - 60), 40])
        else:
            pygame.draw.rect(display, RED, [30, display_height - 80, abs(1 - (bartime / 5000)) * (display_width - 60), 40])
        pygame.draw.rect(display, BLACK, [30, display_height - 80, display_width - 60, 40], 5)
        if bartime >= 5000:
            ticks = pygame.time.get_ticks()
            score -= 1
            letter = letter_font.render(alphabet[random.randint(0, 25)], 1, RED)
            letter_rect = letter.get_rect()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    new_game()
                if event.key == pygame.K_a:
                    score += int((5000 - bartime) / 10)
                    soundwin.play()
                    ticks = pygame.time.get_ticks()
                    letter = letter_font.render(alphabet[random.randint(0, 25)], 1, RED)
                    letter_rect = letter.get_rect()
        clock.tick(30)        
        pygame.display.update()
    pygame.quit()
    sys.exit()


pygame.init()
pygame.mixer.init()

soundwin = pygame.mixer.Sound(soundwinfile)

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_width = display.get_width()
display_height = display.get_height()

display_font = pygame.font.Font(None, 48)
letter_font = pygame.font.Font(None, 800)
rect_score = pygame.Rect((display_width - 120, 50, 120, 50))
rect_time = pygame.Rect((display_width - 120, 0, 50, 50))

display.fill(WHITE)

pygame.display.update()

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                new_game()

pygame.quit()
sys.exit()
