#!/usr/bin/env python
import pygame
import time
import math
import random
import pygame.font
import sys
from pygame.locals import *

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class IrregularVerbs(object):
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
        
        self.my_font = pygame.font.Font(None, 48)
        self.my_rect = pygame.Rect((273,268,252,64))
        self.my_rect_frag_1 = pygame.Rect((273,20,252,64))
        self.my_rect_frag_2 = pygame.Rect((527,268,252,64))
        self.my_rect_frag_3 = pygame.Rect((273,516,252,64))
        self.my_rect_frag_4 = pygame.Rect((20,268,252,64))

        self.display = pygame.display.set_mode((800, 600))# change to desired resolution -- you'll need to modify rect size.
        pygame.display.set_caption("Irregular Verbs Game")
        self.display.fill(IrregularVerbs.WHITE)

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
                raise TextRectException('After word wrap, the text string was too tall to fit in the provided rect.')
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


    def new_user(self):
        irregular_verbs = [
                ["be",[["was/were","q"],["been","a"],["being","q"],["is","q"]]],
                ["beat",[["beat","q"],["beaten","a"],["beating","q"],["beats","q"]]],
                ["begin",[["began","q"],["begun","a"],["beginning","q"],["begins","q"]]],
                ["bite",[["bit","q"],["bitten","a"],["biting","q"],["bite","q"]]],
                ["blow",[["blew","q"],["blown","a"],["blows","q"],["blowing","q"]]],
                ["broadcast",[["broadcast","a"],["broadcasting","q"],["broadcasts","q"],["broadcaster","q"]]],
                ["break",[["broke","q"],["broken","a"],["breaked","q"],["breaking","q"]]],
                ["bring",[["brought","a"],["bringing","q"],["brings","q"],["bring","q"]]],
                ["build",[["built","a"],["building","q"],["builded","q"],["builds","q"]]],
                ["buy",[["bought","a"],["buying","q"],["buys","q"],["buy","q"]]],
                ["catch",[["caught","a"],["catched","q"],["catches","q"],["catching","q"]]],
                ["choose",[["chose","q"],["choose","q"],["chosen","a"],["choosing","q"]]],
                ["come",[["came","q"],["coming","q"],["come","a"],["comes","q"]]],
                ["cost",[["cost","a"],["costs","q"],["costed","q"],["costing","q"]]],
                ["cut",[["cut","a"],["cutted","q"],["cutter","q"],["cutting","q"]]],
                ["do",[["did","q"],["doing","q"],["done","a"],["does","q"]]],
                ["draw",[["drew","q"],["drawn","a"],["draw","q"],["drawing","q"]]],
                ["drink",[["drank","q"],["drinked","q"],["drink","q"],["drunk","a"]]],
                ["drive",[["drove","q"],["drives","q"],["driven","a"],["driving","q"]]],
                ["eat",[["ate","q"],["eaten","a"],["eats","q"],["eating","q"]]],
                ["fall",[["fell","q"],["fallen","a"],["falls","q"],["fall","q"]]],
                ["feed",[["fed","a"],["feeding","q"],["feeds","q"],["felt","q"]]],
                ["feel",[["felt","a"],["feeling","q"],["feels","q"],["feel","q"]]],
                ["fight",[["fought","a"],["fighting","q"],["fights","q"],["fight","q"]]],
                ["find",[["found","a"],["finding","q"],["find","q"],["finds","q"]]],
                ["fly",[["flew","q"],["flown","a"],["flies","q"],["fly","q"]]],
                ["forget",[["forgot","q"],["forget","q"],["forgotten","a"],["forgets","q"]]],
                ["freeze",[["froze","q"],["frozen","a"],["freeze","q"],["freezes","q"]]],
                ["get",[["got","q"],["gotten","a"],["get","q"],["gets","q"]]],
                ["give",[["gave","q"],["given","a"],["give","q"],["gives","q"]]],
                ["go",[["went","q"],["gone","a"],["goes","q"],["going","q"]]],
                ["grow",[["grew","q"],["grown","a"],["grows","q"],["grow","q"]]],
                ["hang",[["hung","a"],["hangs","q"],["hanging","q"],["hanger","q"]]],
                ["have",[["had","a"],["have","q"],["has","q"],["halved","q"]]],
                ["hear",[["heard","a"],["hears","q"],["hearing","q"],["hear","q"]]],
                ["hide",[["hid","q"],["hidden","a"],["hide","q"],["hides","q"]]],
                ["hit",[["hit","a"],["hits","q"],["hitting","q"],["hitted","q"]]],
                ["hold",[["held","a"],["hold","q"],["holds","q"],["holding","q"]]],
                ["hurt",[["hurt","a"],["hurting","q"],["hurts","q"],["hurted","q"]]],
                ["keep",[["kept","a"],["keeps","q"],["keep","q"],["keeping","q"]]],
                ["know",[["knew","q"],["known","a"],["knows","q"],["knowing","q"]]],
                ["lead",[["led","a"],["leads","q"],["leading","q"],["lead","q"]]],
                ["leave",[["left","a"],["leaves","q"],["leave","q"],["leaving","q"]]],
                ["lend",[["lent","a"],["lending","q"],["lend","q"],["lends","q"]]],
                ["let",[["let","a"],["lets","q"],["letting","q"],["letted","q"]]],
                ["lose",[["lost","a"],["lose","q"],["loses","q"],["losing","q"]]],
                ["make",[["made","a"],["make","q"],["maked","q"],["making","q"]]],
                ["mean",[["meant","a"],["means","q"],["mean","q"],["meaning","q"]]],
                ["meet",[["met","a"],["meeting","q"],["meet","q"],["meets","q"]]],
                ["pay",[["paid","a"],["paying","q"],["pay","q"],["pays","q"]]],
                ["put",[["put","a"],["puts","q"],["putting","q"],["putted","q"]]],
                ["read",[["read","a"],["reading","q"],["reads","q"],["reader","q"]]],
                ["ride",[["rode","q"],["ridden","a"],["riding","q"],["ride","q"]]],
                ["ring",[["rang","q"],["rung","a"],["ring","q"],["ringer","q"]]],
                ["rise",[["rose","q"],["risen","a"],["rise","q"],["rises","q"]]],
                ["run",[["ran","q"],["run","a"],["running","q"],["runs","q"]]],
                ["say",[["said","a"],["says","q"],["say","q"],["saying","q"]]],
                ["see",[["saw","q"],["seen","a"],["see","q"],["sees","q"]]],
                ["sell",[["sold","a"],["sell","q"],["sells","q"],["selling","q"]]],
                ["send",[["sent","a"],["sends","q"],["sending","q"],["send","q"]]],
                ["set",[["set","a"],["setting","q"],["sets","q"],["setted","q"]]],
                ["shoot",[["shot","a"],["shooting","q"],["shoot","q"],["shooted","q"]]],
                ["shut",[["shut","a"],["shutting","q"],["shuts","q"],["shutted","q"]]],
                ["sing",[["sang","q"],["sung","a"],["sings","q"],["singing","q"]]],
                ["sit",[["sat","a"],["sits","q"],["sitting","q"],["sitted","q"]]],
                ["sleep",[["slept","a"],["sleeping","q"],["sleep","q"],["sleeps","q"]]],
                ["speak",[["spoke","q"],["spoken","a"],["speaks","q"],["speaking","q"]]],
                ["spend",[["spent","a"],["spend","q"],["spending","q"],["spends","q"]]],
                ["stand",[["stood","a"],["stands","q"],["stand","q"],["standing","q"]]],
                ["steal",[["stole","q"],["stolen","a"],["steal","q"],["steals","q"]]],
                ["stick",[["stuck","a"],["sticked","q"],["sticking","q"],["stick","q"]]],
                ["swim",[["swam","q"],["swum","a"],["swim","q"],["swimming","q"]]],
                ["take",[["took","q"],["taken","a"],["takes","q"],["take","q"]]],
                ["teach",[["taught","a"],["teached","q"],["teach","q"],["teaches","q"]]],
                ["tell",[["told","a"],["tells","q"],["telling","q"],["telled","q"]]],
                ["think",[["thought","a"],["thinks","q"],["think","q"],["thinked","q"]]],
                ["throw",[["threw","q"],["thrown","a"],["throw","q"],["throws","q"]]],
                ["wake",[["woke","q"],["woken","a"],["wake","q"],["waked","q"]]],
                ["wear",[["wore","q"],["worn","q"],["wear","q"],["wears","q"]]],
                ["win",[["won","a"],["wins","q"],["win","q"],["winning","q"]]],
                ["write",[["wrote","q"],["written","a"],["write","q"],["writes","q"]]]
                ]

        wordlist = random.sample(irregular_verbs, 1)[0]
        for entry in wordlist[1]:
            if entry[1] == "a":
                self.answer = entry[0]
        random.shuffle(wordlist[1])

        self.frag0 = wordlist[1][0][0]
        self.frag1 = wordlist[1][1][0]
        self.frag2 = wordlist[1][2][0]
        self.frag3 = wordlist[1][3][0]

        self.display.fill(IrregularVerbs.WHITE)
        self.rendered_text_word = self.render_textrect(wordlist[0], self.my_font, self.my_rect, IrregularVerbs.PURPLE, IrregularVerbs.WHITE, 1)
        self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
        self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
        self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
        self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)

        self.display.blit(self.rendered_text_word, self.my_rect.topleft)
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
            self.display.fill(IrregularVerbs.WHITE)
            if self.frag0 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag1 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag2 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag3 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 0)
            elif self.frag0 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag1 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag2 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag3 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Wins!", self.my_font, self.my_rect, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.GREEN, IrregularVerbs.WHITE, 0)

            self.display.blit(self.rendered_text_word, self.my_rect.topleft)
            self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
            self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
            self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
            self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)
            pygame.display.update()
            self.sound_win.play()
            self.deactivate_keys()

        if fragment != self.answer:#loser
            self.display.fill(IrregularVerbs.WHITE)
            if self.frag0 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag1 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.RED, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag2 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag3 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect("Player 1 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.RED, IrregularVerbs.WHITE, 0)
            elif self.frag0 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag1 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.RED, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag2 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 0)
            elif self.frag3 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect("Player 2 Loses!", self.my_font, self.my_rect, IrregularVerbs.RED, IrregularVerbs.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, IrregularVerbs.BLACK, IrregularVerbs.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, IrregularVerbs.RED, IrregularVerbs.WHITE, 0)

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
                    finished = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.finished = True
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
        pygame.quit()
        sys.exit()
    
if __name__ == '__main__':
    new_game = IrregularVerbs()
    new_game.run()
