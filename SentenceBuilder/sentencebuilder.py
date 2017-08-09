import time
import math
import random
import sqlite3
import pygame
import pygame.font
from pygame.locals import *


class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class SentenceBuilder(object):
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GREEN = (0,128,0)
    YELLOW = (230,230,0)
    RED = (255,0,0)
    BLUE = (0,0,255)
    BROWN = (97,65,38)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        try:
            self.conn = sqlite3.connect('reader.db')
        except:
            print("Database not found!")

        self.c = self.conn.cursor()

        self.sound_win = pygame.mixer.Sound('audio\\ping.ogg')
        self.sound_loss = pygame.mixer.Sound('audio\\buzzer.ogg')         

        self.finished = False

        #self.constructed_sentence = ''


    def render_textrect(self, text_color, background_color, justification=0):
        
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

    def sentence_gen(self):
        sentence_list = sentence.split(' ')
        fragment_list = []
        i = 0
        j = 0
        numberofbuttons = 4#number of buttons on controller

        fragsize_floor = int(math.floor(len(sentence_list)/(numberofbuttons-1)))
        fragsize_remainder = len(sentence_list)%(numberofbuttons-1)

        for i in range(numberofbuttons-1):
            fragment = ""
            for j in range(fragsize_floor):
                fragment = fragment + " " + sentence_list[fragsize_floor*i+j]
            fragment_list.append(fragment)
        #clean up leading space
        i = 0
        for i in range(len(fragment_list)):
            fragment_list[i] = fragment_list[i][1:]

        if fragsize_remainder != 0:
            fragment_list.append(" ".join(sentence_list[len(sentence_list)-fragsize_remainder:]))

        random.shuffle(fragment_list)
        #make sure there are always the correct number of entries.
        if fragsize_remainder == 0:
            fragment_list.append("")

        return fragment_list

    def new_user(self):
        self.constructed_sentence = ''
        self.c.execute('select * from users order by random() limit 1;')
        userdata = self.c.fetchone()
        self.username = str(userdata[1])
        self.c.execute('select * from sentences order by random() limit 1;')
        sentencedata = c.fetchone()
        self.sentence = str(sentencedata[1])
        fragment_list = self.sentence_gen()
        self.frag0 = fragment_list[0]
        self.frag1 = fragment_list[1]
        self.frag2 = fragment_list[2]
        self.frag3 = fragment_list[3]

        display.fill(WHITE)
        #rendered_text = render_textrect(sentenceunderline, self.my_font, self.rect, BLACK, WHITE, 1)
        rendered_text_user = self.render_textrect(BROWN, WHITE, 0)#last 0 is to left align
        rendered_text_frag_1 = self.render_textrect(RED, WHITE, 0)
        rendered_text_frag_2 = self.render_textrect(YELLOW, WHITE, 0)
        rendered_text_frag_3 = self.render_textrect(GREEN, WHITE, 0)
        rendered_text_frag_4 = self.render_textrect(BLUE, WHITE, 0)

        #display.blit(rendered_text, self.rect.topleft)
        display.blit(rendered_text_user, self.rect_user.topleft)
        display.blit(rendered_text_frag_1, self.rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, self.rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, self.rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, self.rect_frag_4.topleft)

        pygame.display.update()

        return

    def refresh_screen(self, fragment):
        if self.constructed_sentence == '':
            self.constructed_sentence = self.constructed_sentence + fragment
        else:
            self.constructed_sentence = self.constructed_sentence + ' ' + fragment

        if fragment == self.frag0:
            self.frag0 = ''
        elif fragment == self.frag1:
            self.frag1 = ''
        elif fragment == self.frag2:
            self.frag2 = ''
        elif fragment == self.frag3:
            self.frag3 = ''

        if self.frag0 == self.frag1 == self.frag2 == self.frag3 == '' and self.sentence == self.constructed_sentence:#winner!
            self.display.fill(WHITE)
            rendered_text = self.render_textrect(sentence, self.my_font, self.rect, GREEN, WHITE, 1)
            rendered_text_user = self.render_textrect(BROWN, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = self.render_textrect(RED, WHITE, 0)
            rendered_text_frag_2 = self.render_textrect(YELLOW, WHITE, 0)
            rendered_text_frag_3 = self.render_textrect(GREEN, WHITE, 0)
            rendered_text_frag_4 = self.render_textrect(BLUE, WHITE, 0)

            display.blit(rendered_text, self.rect.topleft)
            display.blit(rendered_text_user, self.rect_user.topleft)
            display.blit(rendered_text_frag_1, self.rect_frag_1.topleft)
            display.blit(rendered_text_frag_2, self.rect_frag_2.topleft)
            display.blit(rendered_text_frag_3, self.rect_frag_3.topleft)
            display.blit(rendered_text_frag_4, self.rect_frag_4.topleft)

            pygame.display.update()
            self.sound_win.play()

            return

        elif self.frag0 == self.frag1 == self.frag2 == self.frag3 == '' and self.sentence != self.constructed_sentence:#loser
            self.display.fill(WHITE)
            rendered_text = self.render_textrect(RED, WHITE, 1)
            rendered_text_user = self.render_textrect(BROWN, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = self.render_textrect(RED, WHITE, 0)
            rendered_text_frag_2 = self.render_textrect(YELLOW, WHITE, 0)
            rendered_text_frag_3 = self.render_textrect(GREEN, WHITE, 0)
            rendered_text_frag_4 = self.render_textrect(BLUE, WHITE, 0)

            display.blit(rendered_text, self.rect.topleft)
            display.blit(rendered_text_user, self.rect_user.topleft)
            display.blit(rendered_text_frag_1, self.rect_frag_1.topleft)
            display.blit(rendered_text_frag_2, self.rect_frag_2.topleft)
            display.blit(rendered_text_frag_3, self.rect_frag_3.topleft)
            display.blit(rendered_text_frag_4, self.rect_frag_4.topleft)

            pygame.display.update()
            self.sound_loss.play()

            return

        display.fill(WHITE)
        rendered_text = self.render_textrect(BLACK, WHITE, 1)
        rendered_text_user = self.render_textrect(BROWN, WHITE, 0)#last 0 is to left align
        rendered_text_frag_1 = self.render_textrect(RED, WHITE, 0)
        rendered_text_frag_2 = self.render_textrect(YELLOW, WHITE, 0)
        rendered_text_frag_3 = self.render_textrect(GREEN, WHITE, 0)
        rendered_text_frag_4 = self.render_textrect(BLUE, WHITE, 0)

        display.blit(rendered_text, self.rect.topleft)
        display.blit(rendered_text_user, self.rect_user.topleft)
        display.blit(rendered_text_frag_1, self.rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, self.rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, self.rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, self.rect_frag_4.topleft)

        pygame.display.update()

        return

    def run(self):
        self.display = pygame.display.set_mode((1024, 768))

        self.my_font = pygame.font.Font(None, 64)
        self.rect = pygame.Rect((20, 200, 984, 388))
        self.rect_user = pygame.Rect((20, 20, 984, 80))
        self.rect_frag_1 = pygame.Rect((20, 488, 984, 65))
        self.rect_frag_2 = pygame.Rect((20, 553, 984, 65))
        self.rect_frag_3 = pygame.Rect((20, 618, 984, 65))
        self.rect_frag_4 = pygame.Rect((20, 683, 984, 65))

        self.display.fill(SentenceBuilder.WHITE)

        pygame.display.update()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.new_user()
                    if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
                        if self.frag0 != '':
                            self.refresh_screen(self.frag0)
                        else:
                            pass
                    if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
                        if self.frag1 != '':
                            self.refresh_screen(self.frag1)
                        else:
                            pass
                    if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
                        if self.frag2 != '':
                            self.refresh_screen(self.frag2)
                        else:
                            pass
                    if event.key in (pygame.K_d,pygame.K_h,pygame.K_l,pygame.K_p,pygame.K_t,pygame.K_x):
                        if self.frag3 != '':
                            self.refresh_screen(self.frag3)
                        else:
                            pass
                    
            pygame.display.update()
            
        self.conn.close()
