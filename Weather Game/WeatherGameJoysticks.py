import pygame, time, sqlite3, math, random
import pygame.font
from pygame.locals import *

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class WeatherGame(object):
    def __init__(self):
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.GREEN = (0,128,0)
        self.YELLOW = (255,229,51)
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.BROWN = (97,65,38)
        self.PURPLE = (128,0,128)    
    
        pygame.init()
        pygame.mixer.init()

        self.SoundWinFile = 'ping.ogg'
        self.SoundLossFile = 'buzzer.ogg'
        self.SoundWin = pygame.mixer.Sound(self.SoundWinFile)
        self.SoundLoss = pygame.mixer.Sound(self.SoundLossFile)

        self.MySound0 = pygame.mixer.Sound('audio\\itscloudy.ogg')
        self.MySound1 = pygame.mixer.Sound('audio\\itscold.ogg')
        self.MySound2 = pygame.mixer.Sound('audio\\itshot.ogg')
        self.MySound3 = pygame.mixer.Sound('audio\\itsfoggy.ogg')
        self.MySound4 = pygame.mixer.Sound('audio\\itsraining.ogg')
        self.MySound5 = pygame.mixer.Sound('audio\\itssunny.ogg')
        self.MySound6 = pygame.mixer.Sound('audio\\itsstormy.ogg')
        self.MySound7 = pygame.mixer.Sound('audio\\itswindy.ogg')
        self.MySound8 = pygame.mixer.Sound('audio\\itssnowing.ogg')

        self.MyImage0 = pygame.image.load('images\cloudy.png')
        self.MyImageRect0 = self.MyImage0.get_rect()
        self.MyImage1 = pygame.image.load('images\\cold.png')
        self.MyImage2 = pygame.image.load('images\\hot.png')
        self.MyImage3 = pygame.image.load('images\\foggy.png')
        self.MyImage4 = pygame.image.load('images\\raining.png')
        self.MyImage5 = pygame.image.load('images\\sunny.png')
        self.MyImage6 = pygame.image.load('images\\stormy.png')
        self.MyImage7 = pygame.image.load('images\\windy.png')
        self.MyImage8 = pygame.image.load('images\\snowing.png')
        self.MyImageVol = pygame.image.load('images\\sound.png')

        self.my_font = pygame.font.Font(None, 48)# need to make these relative
        self.my_rect = pygame.Rect((273,268,252,64))
        self.my_rect_frag_1 = pygame.Rect((273,20,252,64))
        self.my_rect_frag_2 = pygame.Rect((527,268,252,64))
        self.my_rect_frag_3 = pygame.Rect((273,516,252,64))
        self.my_rect_frag_4 = pygame.Rect((20,268,252,64))

        self.display = pygame.display.set_mode((800, 600))# change to desired resolution -- you'll need to modify rect size.
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
                        raise TextRectException, 'The word ' + word + ' is too long to fit in the provided rect.'
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
                raise TextRectException, 'After word wrap, the text string was too tall to fit in the provided rect.'
            if line != '':
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException, 'Invalid justification argument: ' + str(justification)
            accumulated_height += font.size(line)[1]

        return surface

    def new_user(self):

        self.IrregularVerbs = [
        [self.MyImage0,[["It's cloudy.","a"],["It's cold.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.MyImage1,[["It's cold.","a"],["It's hot.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.MyImage2,[["It's hot.","a"],["It's foggy.","q"],["It's raining.","q"],["It's sunny.","q"]]],
        [self.MyImage3,[["It's foggy.","a"],["It's sunny.","q"],["It's stormy.","q"],["It's raining.","q"]]],
        [self.MyImage4,[["It's raining.","a"],["It's stormy.","q"],["It's sunny.","q"],["It's windy.","q"]]],
        [self.MyImage5,[["It's sunny.","a"],["It's stormy.","q"],["It's windy.","q"],["It's snowing.","q"]]],
        [self.MyImage6,[["It's stormy.","a"],["It's windy.","q"],["It's snowing.","q"],["It's cloudy.","q"]]],
        [self.MyImage7,[["It's windy.","a"],["It's foggy.","q"],["It's sunny.","q"],["It's raining.","q"]]],
        [self.MyImage8,[["It's snowing.","a"],["It's windy.","q"],["It's foggy.","q"],["It's sunny.","q"]]],
        [self.MySound0,[["It's cloudy.","a"],["It's cold.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.MySound1,[["It's cold.","a"],["It's hot.","q"],["It's foggy.","q"],["It's raining.","q"]]],
        [self.MySound2,[["It's hot.","a"],["It's foggy.","q"],["It's raining.","q"],["It's sunny.","q"]]],
        [self.MySound3,[["It's foggy.","a"],["It's sunny.","q"],["It's stormy.","q"],["It's raining.","q"]]],
        [self.MySound4,[["It's raining.","a"],["It's stormy.","q"],["It's sunny.","q"],["It's windy.","q"]]],
        [self.MySound5,[["It's sunny.","a"],["It's stormy.","q"],["It's windy.","q"],["It's snowing.","q"]]],
        [self.MySound6,[["It's stormy.","a"],["It's windy.","q"],["It's snowing.","q"],["It's cloudy.","q"]]],
        [self.MySound7,[["It's windy.","a"],["It's foggy.","q"],["It's sunny.","q"],["It's raining.","q"]]],
        [self.MySound8,[["It's snowing.","a"],["It's windy.","q"],["It's foggy.","q"],["It's sunny.","q"]]],
        ]

        self.WordList = random.sample(self.IrregularVerbs,1)[0]
        self.answer = self.WordList[1][0][0]
        random.shuffle(self.WordList[1])

        self.frag0 = self.WordList[1][0][0]
        self.frag1 = self.WordList[1][1][0]
        self.frag2 = self.WordList[1][2][0]
        self.frag3 = self.WordList[1][3][0]

        self.display.fill(self.WHITE)
        self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, self.BLACK, self.WHITE, 1)
        self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, self.BLACK, self.WHITE, 2)
        self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, self.BLACK, self.WHITE, 1)
        self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, self.BLACK, self.WHITE, 0)

        if self.WordList[0] in (self.MyImage0,self.MyImage1,self.MyImage2,self.MyImage3,self.MyImage4,self.MyImage5,self.MyImage6,self.MyImage7,self.MyImage8):
            self.display.blit(self.WordList[0], ((self.display.get_rect().centerx-self.MyImageRect0.width/2),(self.display.get_rect().centery-self.MyImageRect0.height/2)))
        else:
            self.display.blit(self.MyImageVol, ((self.display.get_rect().centerx-self.MyImageRect0.width/2),(self.display.get_rect().centery-self.MyImageRect0.height/2)))
            self.WordList[0].play()
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
        if fragment == self.answer:#winner!
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
            self.SoundWin.play()
            self.deactivate_keys()

        if fragment != self.answer:#loser
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
            self.SoundLoss.play()
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
    NewGame = WeatherGame()
    NewGame.run()
