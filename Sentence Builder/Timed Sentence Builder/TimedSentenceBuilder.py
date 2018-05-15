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
sentence_list = ["This is the best sentence.", "This is the worst sentence."]


class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color=WHITE, justification=0):
    
    final_lines = []

    requested_lines = string.splitlines()

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "   
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface

def new_game():
    time_remaining = 60
    constructed_sentence = ''
    sentence = random.choice(sentence_list)
    sentence_surface = render_textrect(sentence, font, sentence_rect, RED)
    
    

pygame.init()
pygame.mixer.init()

soundwin = pygame.mixer.Sound(soundwinfile)
soundloss = pygame.mixer.Sound(soundlossfile)

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_width = display.get_width()
display_height = display.get_height()

font = pygame.font.Font(None, 48)
sentence_rect = pygame.Rect(20, 20, display_width - 40, display_height / 2)

display.fill(WHITE)

pygame.display.update()

clock = pygame.time.Clock()

while not finished:
    if pygame.time.get_ticks() - previous_time >= 1000:
        previous_time = pygame.time.get_ticks()
        time_remaining -= 1
        if time_remaining == 0:
            finished = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                finished == True
            if event.key == pygame.K_SPACE:
                new_game()
            if event.key == pygame.K_a:
                if frag0 != "":
                    refresh_screen(frag0)
                else:
                    pass
            if event.key == pygame.K_b:
                if frag1 != "":
                    refresh_screen(frag1)
                else:
                    pass
            if event.key == pygame.K_c:
                if frag2 != "":
                    refresh_screen(frag2)
                else:
                    pass
            if event.key == pygame.K_d:
                if frag3 != "":
                    refresh_screen(frag3)
                else:
                    pass
    clock.tick(30)        
    pygame.display.update()

pygame.quit()
