#!/usr/bin/env python
import pygame, time, sqlite3, math, random, sys
import pygame.font
from pygame.locals import *

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class WeatherGame(object):
    WHITE = (255,255,255)# some colors are not currently used, but left for future modification
    BLACK = (0,0,0)
    GREEN = (0,128,0)
    YELLOW = (255,229,51)
    RED = (255,0,0)
    BLUE = (0,0,255)
    BROWN = (97,65,38)
    PURPLE = (128,0,128)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.sound_win = pygame.mixer.Sound('audio\\ping.ogg')
        self.sound_loss = pygame.mixer.Sound('audio\\buzzer.ogg')

        self.my_sound_0 = pygame.mixer.Sound('audio\\itscloudy.ogg')
        self.my_sound_1 = pygame.mixer.Sound('audio\\itscold.ogg')
        self.my_sound_2 = pygame.mixer.Sound('audio\\itshot.ogg')
        self.my_sound_3 = pygame.mixer.Sound('audio\\itsfoggy.ogg')
        self.my_sound_4 = pygame.mixer.Sound('audio\\itsraining.ogg')
        self.my_sound_5 = pygame.mixer.Sound('audio\\itssunny.ogg')
        self.my_sound_6 = pygame.mixer.Sound('audio\\itsstormy.ogg')
        self.my_sound_7 = pygame.mixer.Sound('audio\\itswindy.ogg')
        self.my_sound_8 = pygame.mixer.Sound('audio\\itssnowing.ogg')

        self.my_image_0 = pygame.image.load('images\cloudy.png')
        self.my_image_rect_0 = self.my_image_0.get_rect()
        self.my_image_1 = pygame.image.load('images\\cold.png')
        self.my_image_2 = pygame.image.load('images\\hot.png')
        self.my_image_3 = pygame.image.load('images\\foggy.png')
        self.my_image_4 = pygame.image.load('images\\raining.png')
        self.my_image_5 = pygame.image.load('images\\sunny.png')
        self.my_image_6 = pygame.image.load('images\\stormy.png')
        self.my_image_7 = pygame.image.load('images\\windy.png')
        self.my_image_8 = pygame.image.load('images\\snowing.png')
        self.my_image_vol = pygame.image.load('images\\sound.png')

        self.my_font = pygame.font.Font(None, 48)# need to make these relative
        self.my_rect = pygame.Rect((273,268,252,64))
        self.my_rect_frag_1 = pygame.Rect((273,20,252,64))
        self.my_rect_frag_2 = pygame.Rect((527,268,252,64))
        self.my_rect_frag_3 = pygame.Rect((273,516,252,64))
        self.my_rect_frag_4 = pygame.Rect((20,268,252,64))

        self.display = pygame.display.set_mode((800, 600))# change to desired resolution -- you'll need to modify rect size.
        pygame.display.set_caption("Weather Game")
        self.display.fill(self.WHITE)

        pygame.display.update()

        self.finished = False
    
    def render_textrect(self, string, font, rect, text_color, background_color, justification=0):
        
        final_lines = []

        requested_lines = string.splitlines()

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise TextRectException('The word ' + word + ' is too long to fit in the provided rect.')
                accumulated_line = ''
                for word in words:
                    test_line = accumulated_line + word + ' '   
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line 
                    else: 
                        final_lines.append(accumulated_line) 
                        accumulated_line = word + ' ' 
                final_lines.append(accumulated_line)
            else: 
                final_lines.append(requested_line) 

        surface = pygame.Surface(rect.size) 
        surface.fill(background_color) 

        accumulated_height = 0 
        for line in final_lines: 
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise TextRectException('After word wrap, the text string was too tall to fit in the provided rect.')
            if line != '':
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException('Invalid justification argument: ' + str(justification))
            accumulated_height += font.size(line)[1]

        return surface

    def new_user(self):

        self.irregular_verbs = [
        [self.my_image_0,[["It's cloudy.","a"],["It's cold.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.my_image_1,[["It's cold.","a"],["It's hot.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.my_image_2,[["It's hot.","a"],["It's foggy.","q"],["It's raining.","q"],["It's sunny.","q"]]],
        [self.my_image_3,[["It's foggy.","a"],["It's sunny.","q"],["It's stormy.","q"],["It's raining.","q"]]],
        [self.my_image_4,[["It's raining.","a"],["It's stormy.","q"],["It's sunny.","q"],["It's windy.","q"]]],
        [self.my_image_5,[["It's sunny.","a"],["It's stormy.","q"],["It's windy.","q"],["It's snowing.","q"]]],
        [self.my_image_6,[["It's stormy.","a"],["It's windy.","q"],["It's snowing.","q"],["It's cloudy.","q"]]],
        [self.my_image_7,[["It's windy.","a"],["It's foggy.","q"],["It's sunny.","q"],["It's raining.","q"]]],
        [self.my_image_8,[["It's snowing.","a"],["It's windy.","q"],["It's foggy.","q"],["It's sunny.","q"]]],
        [self.my_sound_0,[["It's cloudy.","a"],["It's cold.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.my_sound_1,[["It's cold.","a"],["It's hot.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.my_sound_2,[["It's hot.","a"],["It's foggy.","q"],["It's raining.","q"],["It's sunny.","q"]]],
        [self.my_sound_3,[["It's foggy.","a"],["It's sunny.","q"],["It's stormy.","q"],["It's raining.","q"]]],
        [self.my_sound_4,[["It's raining.","a"],["It's stormy.","q"],["It's sunny.","q"],["It's windy.","q"]]],
        [self.my_sound_5,[["It's sunny.","a"],["It's stormy.","q"],["It's windy.","q"],["It's snowing.","q"]]],
        [self.my_sound_6,[["It's stormy.","a"],["It's windy.","q"],["It's snowing.","q"],["It's cloudy.","q"]]],
        [self.my_sound_7,[["It's windy.","a"],["It's foggy.","q"],["It's sunny.","q"],["It's raining.","q"]]],
        [self.my_sound_8,[["It's snowing.","a"],["It's windy.","q"],["It's foggy.","q"],["It's sunny.","q"]]],
        ]

        self.word_list = random.sample(self.irregular_verbs,1)[0]
        self.answer = self.word_list[1][0][0]
        random.shuffle(self.word_list[1])

        self.frag0 = self.word_list[1][0][0]
        self.frag1 = self.word_list[1][1][0]
        self.frag2 = self.word_list[1][2][0]
        self.frag3 = self.word_list[1][3][0]

        self.display.fill(self.WHITE)
        self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
        self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
        self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
        self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)

        if self.word_list[0] in (self.my_image_0,self.my_image_1,self.my_image_2,self.my_image_3,self.my_image_4,self.my_image_5,self.my_image_6,self.my_image_7,self.my_image_8):
            self.display.blit(self.word_list[0], ((self.display.get_rect().centerx-self.my_image_rect_0.width/2),(self.display.get_rect().centery-self.my_image_rect_0.height/2)))
        else:
            self.display.blit(self.my_image_vol, ((self.display.get_rect().centerx-self.my_image_rect_0.width/2),(self.display.get_rect().centery-self.my_image_rect_0.height/2)))
            self.word_list[0].play()
        self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
        self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
        self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
        self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)

        pygame.display.update()

        return

    def deactivate_keys(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    return

    def refresh_screen(self, fragment, player):
        if fragment == self.answer:# winner!
            self.display.fill(self.WHITE)
            if self.frag0 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.GREEN, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag1 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.GREEN, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag2 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.GREEN, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag3 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.GREEN, self.WHITE, 0)
            elif self.frag0 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.GREEN, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag1 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.GREEN, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag2 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.GREEN, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag3 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, self.GREEN, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.GREEN, self.WHITE, 0)

            self.display.blit(self.rendered_text_word, self.my_rect.topleft)
            self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
            self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
            self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
            self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)
            pygame.display.update()
            self.sound_win.play()
            self.deactivate_keys()

        if fragment != self.answer:# loser
            self.display.fill(self.WHITE)
            if self.frag0 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.RED, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag1 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.RED, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag2 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.RED, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag3 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.RED, self.WHITE, 0)
            elif self.frag0 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.RED, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag1 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.RED, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag2 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.RED, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)
            elif self.frag3 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, self.RED, self.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.RED, self.WHITE, 0)

            self.display.blit(self.rendered_text_word, self.my_rect.topleft)
            self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
            self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
            self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
            self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)
            pygame.display.update()
            self.sound_loss.play()
            self.deactivate_keys()


    def run(self):
        while not self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.new_user()
                    if event.key == pygame.K_a:
                        self.refresh_screen(self.frag0, player=1)
                    elif event.key == pygame.K_e:
                        self.refresh_screen(self.frag0, player=2)
                    elif event.key == pygame.K_b:
                        self.refresh_screen(self.frag1, player=1)
                    elif event.key == pygame.K_f:
                        self.refresh_screen(self.frag1, player=2)
                    elif event.key == pygame.K_c:
                        self.refresh_screen(self.frag2, player=1)
                    elif event.key == pygame.K_g:
                        self.refresh_screen(self.frag2, player=2)
                    elif event.key == pygame.K_d:
                        self.refresh_screen(self.frag3, player=1)
                    elif event.key == pygame.K_h:
                        self.refresh_screen(self.frag3, player=2)
                    else:
                        pass
                   
            pygame.display.update()
        
if __name__ == '__main__':
    new_game = WeatherGame()
    new_game.run()
