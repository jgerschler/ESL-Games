import time
import sqlite3
import math
import random
import pygame
import pygame.font
from pygame.locals import *

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

constructed_sentence = ''

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    
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

def sentence_gen(sentence):
    sentencelist = sentence.split(' ')
    fragmentlist = []
    i = 0
    j = 0
    numberofbuttons = 4#number of buttons on controller

    fragsizefloor = int(math.floor(len(sentencelist)/(numberofbuttons-1)))
    fragsizeremainder = len(sentencelist)%(numberofbuttons-1)

    for i in range(numberofbuttons-1):
        fragment = ""
        for j in range(fragsizefloor):
            fragment = fragment + " " + sentencelist[fragsizefloor*i+j]
        fragmentlist.append(fragment)
    #clean up leading space
    i = 0
    for i in range(len(fragmentlist)):
        fragmentlist[i] = fragmentlist[i][1:]

    if fragsizeremainder != 0:
        fragmentlist.append(" ".join(sentencelist[len(sentencelist)-fragsizeremainder:]))

    random.shuffle(fragmentlist)
    #make sure there are always the correct number of entries.
    if fragsizeremainder == 0:
        fragmentlist.append("")

    return fragmentlist

def new_user():
    constructed_sentence = ""
    c.execute('select * from users order by random() limit 1;')
    userdata = c.fetchone()
    username = str(userdata[1])
    c.execute('select * from sentences order by random() limit 1;')
    sentencedata = c.fetchone()
    sentence = str(sentencedata[1])
    fragmentlist = sentence_gen(sentence)
    frag0 = fragmentlist[0]
    frag1 = fragmentlist[1]
    frag2 = fragmentlist[2]
    frag3 = fragmentlist[3]

    display.fill(WHITE)
    #rendered_text = render_textrect(sentenceunderline, my_font, my_rect, BLACK, WHITE, 1)
    rendered_text_user = render_textrect(username, my_font, my_rect_user, BROWN, WHITE, 0)#last 0 is to left align
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

    #display.blit(rendered_text, my_rect.topleft)
    display.blit(rendered_text_user, my_rect_user.topleft)
    display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
    display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
    display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
    display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

    pygame.display.update()

    return frag0, frag1, frag2, frag3, username, sentence, constructed_sentence

def refresh_screen(fragment):
    global sentence
    global constructed_sentence
    global frag0
    global frag1
    global frag2
    global frag3
    global username

    if constructed_sentence == "":
        constructed_sentence = constructed_sentence + fragment
    else:
        constructed_sentence = constructed_sentence + " " + fragment

    if fragment == frag0:
        frag0 = ""
    elif fragment == frag1:
        frag1 = ""
    elif fragment == frag2:
        frag2 = ""
    elif fragment == frag3:
        frag3 = ""

    if frag0 == frag1 == frag2 == frag3 == "" and sentence == constructed_sentence:#winner!
        display.fill(WHITE)
        rendered_text = render_textrect(sentence, my_font, my_rect, GREEN, WHITE, 1)
        rendered_text_user = render_textrect(username, my_font, my_rect_user, BROWN, WHITE, 0)#last 0 is to left align
        rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
        rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
        rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
        rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

        display.blit(rendered_text, my_rect.topleft)
        display.blit(rendered_text_user, my_rect_user.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

        pygame.display.update()
        soundwin.play()

        return

    elif frag0 == frag1 == frag2 == frag3 == "" and sentence != constructed_sentence:#loser
        display.fill(WHITE)
        rendered_text = render_textrect(constructed_sentence, my_font, my_rect, RED, WHITE, 1)
        rendered_text_user = render_textrect(username, my_font, my_rect_user, BROWN, WHITE, 0)#last 0 is to left align
        rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
        rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
        rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
        rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

        display.blit(rendered_text, my_rect.topleft)
        display.blit(rendered_text_user, my_rect_user.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

        pygame.display.update()
        soundloss.play()

        return

    display.fill(WHITE)
    rendered_text = render_textrect(constructed_sentence, my_font, my_rect, BLACK, WHITE, 1)
    rendered_text_user = render_textrect(username, my_font, my_rect_user, BROWN, WHITE, 0)#last 0 is to left align
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

    display.blit(rendered_text, my_rect.topleft)
    display.blit(rendered_text_user, my_rect_user.topleft)
    display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
    display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
    display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
    display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

    pygame.display.update()

    return

#connect to database
try:
    conn = sqlite3.connect('reader.db')
except:
    print("Database not found!")

c = conn.cursor()

pygame.init()
pygame.mixer.init()

soundwin = pygame.mixer.Sound(soundwinfile)
soundloss = pygame.mixer.Sound(soundlossfile)

display = pygame.display.set_mode((1024, 768))

my_font = pygame.font.Font(None, 48)
my_rect = pygame.Rect((20, 200, 984, 388))
my_rect_user = pygame.Rect((20, 20, 984, 80))
my_rect_frag_1 = pygame.Rect((20, 488, 984, 65))
my_rect_frag_2 = pygame.Rect((20, 553, 984, 65))
my_rect_frag_3 = pygame.Rect((20, 618, 984, 65))
my_rect_frag_4 = pygame.Rect((20, 683, 984, 65))

display.fill(WHITE)

pygame.display.update()

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                frag0, frag1, frag2, frag3, username, sentence, constructed_sentence = new_user()
            if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
                if frag0 != "":
                    refresh_screen(frag0)
                else:
                    pass
            if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
                if frag1 != "":
                    refresh_screen(frag1)
                else:
                    pass
            if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
                if frag2 != "":
                    refresh_screen(frag2)
                else:
                    pass
            if event.key in (pygame.K_d,pygame.K_h,pygame.K_l,pygame.K_p,pygame.K_t,pygame.K_x):
                if frag3 != "":
                    refresh_screen(frag3)
                else:
                    pass
            
    pygame.display.update()

conn.close()
