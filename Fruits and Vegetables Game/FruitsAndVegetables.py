#!/usr/bin/python
import pygame, time, math, random, sys
import pygame.font
from pygame.locals import *

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class FruitsAndVegetables(object):
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

        self.my_image_0 = pygame.image.load("images\\apple.png")
        self.my_image_rect_0 = self.my_image_0.get_rect()
        self.my_image_1 = pygame.image.load("images\\apricot.png")
        self.my_image_2 = pygame.image.load("images\\asparagus.png")
        self.my_image_3 = pygame.image.load("images\\avocado.png")
        self.my_image_4 = pygame.image.load("images\\banana.png")
        self.my_image_5 = pygame.image.load("images\\beets.png")
        self.my_image_6 = pygame.image.load("images\\bellpepper.png")
        self.my_image_7 = pygame.image.load("images\\blueberries.png")
        self.my_image_8 = pygame.image.load("images\\broccoli.png")
        self.my_image_9 = pygame.image.load("images\\cabbage.png")
        self.my_image_10 = pygame.image.load("images\\canteloupe.png")
        self.my_image_11 = pygame.image.load("images\\carrots.png")
        self.my_image_12 = pygame.image.load("images\\cauliflour.png")
        self.my_image_13 = pygame.image.load("images\\celery.png")
        self.my_image_14 = pygame.image.load("images\\cherries.png")
        self.my_image_15 = pygame.image.load("images\\chilipeppers.png")
        self.my_image_16 = pygame.image.load("images\\coconut.png")
        self.my_image_17 = pygame.image.load("images\\corn.png")
        self.my_image_18 = pygame.image.load("images\\cucumber.png")
        self.my_image_19 = pygame.image.load("images\\dragonfruit.png")
        self.my_image_20 = pygame.image.load("images\\eggplant.png")
        self.my_image_21 = pygame.image.load("images\\garlic.png")
        self.my_image_22 = pygame.image.load("images\\ginger.png")
        self.my_image_23 = pygame.image.load("images\\grapefruit.png")
        self.my_image_24 = pygame.image.load("images\\grapes.png")
        self.my_image_25 = pygame.image.load("images\\greenbeans.png")
        self.my_image_26 = pygame.image.load("images\\greenonions.png")
        self.my_image_27 = pygame.image.load("images\\guava.png")
        self.my_image_28 = pygame.image.load("images\\kiwi.png")
        self.my_image_29 = pygame.image.load("images\\lettuce.png")
        self.my_image_30 = pygame.image.load("images\\limelemon.png")
        self.my_image_31 = pygame.image.load("images\\lychee.png")
        self.my_image_32 = pygame.image.load("images\\mango.png")
        self.my_image_33 = pygame.image.load("images\\melon.png")
        self.my_image_34 = pygame.image.load("images\\mushroom.png")
        self.my_image_35 = pygame.image.load("images\\olives.png")
        self.my_image_36 = pygame.image.load("images\\onion.png")
        self.my_image_37 = pygame.image.load("images\\orange.png")
        self.my_image_38 = pygame.image.load("images\\papaya.png")
        self.my_image_39 = pygame.image.load("images\\passionfruit.png")
        self.my_image_40 = pygame.image.load("images\\peach.png")
        self.my_image_41 = pygame.image.load("images\\pear.png")
        self.my_image_42 = pygame.image.load("images\\peas.png")
        self.my_image_43 = pygame.image.load("images\\pineapple.png")
        self.my_image_44 = pygame.image.load("images\\plum.png")
        self.my_image_45 = pygame.image.load("images\\pomegranate.png")
        self.my_image_46 = pygame.image.load("images\\potato.png")
        self.my_image_47 = pygame.image.load("images\\pumpkin.png")
        self.my_image_48 = pygame.image.load("images\\radishes.png")
        self.my_image_49 = pygame.image.load("images\\rambutans.png")
        self.my_image_50 = pygame.image.load("images\\raspberries.png")
        self.my_image_51 = pygame.image.load("images\\spinach.png")
        self.my_image_52 = pygame.image.load("images\\starfruit.png")
        self.my_image_53 = pygame.image.load("images\\strawberry.png")
        self.my_image_54 = pygame.image.load("images\\sugarcane.png")
        self.my_image_55 = pygame.image.load("images\\tomatoes.png")
        self.my_image_56 = pygame.image.load("images\\watermelon.png")
        self.my_image_57 = pygame.image.load("images\\yam.png")

        self.my_font = pygame.font.Font(None, 48)# need to make these relative
        self.my_rect = pygame.Rect((273,268,252,64))
        self.my_rect_frag_1 = pygame.Rect((273,20,252,64))
        self.my_rect_frag_2 = pygame.Rect((527,268,252,64))
        self.my_rect_frag_3 = pygame.Rect((273,516,252,64))
        self.my_rect_frag_4 = pygame.Rect((20,268,252,64))

        self.display = pygame.display.set_mode((800, 600))# change to desired resolution -- you'll need to modify rect size.
        pygame.display.set_caption("Fruits and Vegetables Game")
        self.display.fill(FruitsAndVegetables.WHITE)

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
        self.irregular_verbs = [
        [self.my_image_0,[["apple","a"],["banana","q"],["peach","q"],["orange","q"]]],
        [self.my_image_1,[["apricot","a"],["lemon","q"],["starfruit","q"],["potato","q"]]],
        [self.my_image_2,[["asparagus","a"],["avocado","q"],["banana","q"],["beets","q"]]],
        [self.my_image_3,[["avocado","a"],["tomato","q"],["potato","q"],["celery","q"]]],
        [self.my_image_4,[["banana","a"],["beet","q"],["carrot","q"],["guava","q"]]],
        [self.my_image_5,[["beets","a"],["potatoes","q"],["oranges","q"],["starfruit","q"]]],
        [self.my_image_6,[["bell pepper","a"],["tomato","q"],["orange","q"],["watermelon","q"]]],
        [self.my_image_7,[["blueberries","a"],["broccoli","q"],["corn","q"],["peaches","q"]]],
        [self.my_image_8,[["broccoli","a"],["potato","q"],["orange","q"],["starfruit","q"]]],
        [self.my_image_9,[["cabbage","a"],["cauliflower","q"],["garlic","q"],["ginger","q"]]],
        [self.my_image_10,[["canteloupe","a"],["celery","q"],["lychee","q"],["mango","q"]]],
        [self.my_image_11,[["carrots","a"],["potatoes","q"],["tomatoes","q"],["pears","q"]]],
        [self.my_image_12,[["cauliflower","a"],["garlic","q"],["onion","q"],["olive","q"]]],
        [self.my_image_13,[["celery","a"],["pomegranate","q"],["pea","q"],["radish","q"]]],
        [self.my_image_14,[["cherries","a"],["green beans","q"],["oranges","q"],["green onions","q"]]],
        [self.my_image_15,[["chili peppers","a"],["peas","q"],["rambutans","q"],["tomatoes","q"]]],
        [self.my_image_16,[["coconut","a"],["yam","q"],["pineapple","q"],["plum","q"]]],
        [self.my_image_17,[["corn","a"],["potato","q"],["tomato","q"],["lemon","q"]]],
        [self.my_image_18,[["cucumber","a"],["lime","q"],["carrot","q"],["papaya","q"]]],
        [self.my_image_19,[["dragonfruit","a"],["star fruit","q"],["passion fruit","q"],["peach","q"]]],
        [self.my_image_20,[["eggplant","a"],["potato","q"],["coconut","q"],["spinach","q"]]],
        [self.my_image_21,[["garlic","a"],["beet","q"],["banana","q"],["blueberry","q"]]],
        [self.my_image_22,[["ginger","a"],["garlic","q"],["grape","q"],["olive","q"]]],
        [self.my_image_23,[["grapefruit","a"],["grape","q"],["rambutan","q"],["lychee","q"]]],
        [self.my_image_24,[["grapes","a"],["mushrooms","q"],["olives","q"],["papayas","q"]]],
        [self.my_image_25,[["green beans","a"],["peas","q"],["tomatoes","q"],["pineapples","q"]]],
        [self.my_image_26,[["green onions","a"],["watermelons","q"],["melons","q"],["onions","q"]]],
        [self.my_image_27,[["guava","a"],["star fruit","q"],["passion fruit","q"],["radish","q"]]],
        [self.my_image_28,[["kiwi","a"],["pea","q"],["pear","q"],["pumpkin","q"]]],
        [self.my_image_29,[["lettuce","a"],["spinach","q"],["raspberry","q"],["strawberry","q"]]],
        [self.my_image_30,[["lime/lemons","a"],["potatoes","q"],["oranges","q"],["melons","q"]]],
        [self.my_image_31,[["lychee","a"],["rambutan","q"],["mango","q"],["peach","q"]]],
        [self.my_image_32,[["mango","a"],["potato","q"],["tomato","q"],["olive","q"]]],
        [self.my_image_33,[["melon","a"],["canteloupe","q"],["plum","q"],["watermelon","q"]]],
        [self.my_image_34,[["mushroom","a"],["onion","q"],["pumpkin","q"],["pomegranate","q"]]],
        [self.my_image_35,[["olives","a"],["mushrooms","q"],["blueberries","q"],["raspberries","q"]]],
        [self.my_image_36,[["onion","a"],["potato","q"],["onion","q"],["green onion","q"]]],
        [self.my_image_37,[["orange","a"],["lime","q"],["lemon","q"],["pear","q"]]],
        [self.my_image_38,[["papaya","a"],["potato","q"],["orange","q"],["starfruit","q"]]],
        [self.my_image_39,[["passion fruit","a"],["dragonfruit","q"],["orange","q"],["starfruit","q"]]],
        [self.my_image_40,[["peach","a"],["pear","q"],["plum","q"],["apple","q"]]],
        [self.my_image_41,[["pear","a"],["apricot","q"],["orange","q"],["peach","q"]]],
        [self.my_image_42,[["peas","a"],["green beans","q"],["eggplants","q"],["lemons","q"]]],
        [self.my_image_43,[["pineapple","a"],["lime","q"],["orange","q"],["passion fruit","q"]]],
        [self.my_image_44,[["plum","a"],["peach","q"],["apricot","q"],["broccoli","q"]]],
        [self.my_image_45,[["pomegranate","a"],["plum","q"],["starfruit","q"],["sugarcane","q"]]],
        [self.my_image_46,[["potato","a"],["tomato","q"],["yam","q"],["radish","q"]]],
        [self.my_image_47,[["pumpkin","a"],["rambutan","q"],["lychee","q"],["grapefruit","q"]]],
        [self.my_image_48,[["radishes","a"],["blueberries","q"],["peas","q"],["corn","q"]]],
        [self.my_image_49,[["rambutans","a"],["lychees","q"],["raspberries","q"],["blueberries","q"]]],
        [self.my_image_50,[["raspberries","a"],["blueberries","q"],["rambutans","q"],["lychees","q"]]],
        [self.my_image_51,[["spinach","a"],["lettuce","q"],["cabbage","q"],["radish","q"]]],
        [self.my_image_52,[["starfruit","a"],["passion fruit","q"],["dragonfruit","q"],["grapefruit","q"]]],
        [self.my_image_53,[["strawberry","a"],["blueberry","q"],["raspberry","q"],["blackberry","q"]]],
        [self.my_image_54,[["sugarcane","a"],["mango","q"],["lemon","q"],["tomato","q"]]],
        [self.my_image_55,[["tomatoes","a"],["potatoes","q"],["oranges","q"],["pears","q"]]],
        [self.my_image_56,[["watermelon","a"],["melon","q"],["canteloupe","q"],["grapefruit","q"]]],
        [self.my_image_57,[["yam","a"],["potato","q"],["melon","q"],["garlic","q"]]]
        ]

        self.word_list = random.sample(self.irregular_verbs,1)[0]
        self.answer = self.word_list[1][0][0]
        random.shuffle(self.word_list[1])

        self.frag0 = self.word_list[1][0][0]
        self.frag1 = self.word_list[1][1][0]
        self.frag2 = self.word_list[1][2][0]
        self.frag3 = self.word_list[1][3][0]

        self.display.fill(FruitsAndVegetables.WHITE)
        self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
        self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
        self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
        self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)

        self.display.blit(self.word_list[0], ((self.display.get_rect().centerx-self.my_image_rect_0.width/2),(self.display.get_rect().centery-self.my_image_rect_0.height/2)))
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
            self.display.fill(FruitsAndVegetables.WHITE)
            if self.frag0 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag1 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag2 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag3 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 0)
            elif self.frag0 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag1 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag2 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag3 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Wins!', self.my_font, self.my_rect, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.GREEN, FruitsAndVegetables.WHITE, 0)

            self.display.blit(self.rendered_text_word, self.my_rect.topleft)
            self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
            self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
            self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
            self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)
            pygame.display.update()
            self.sound_win.play()
            self.deactivate_keys()

        if fragment != self.answer:# loser
            self.display.fill(FruitsAndVegetables.WHITE)
            if self.frag0 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag1 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag2 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag3 == fragment and player == 1:
                self.rendered_text_word = self.render_textrect('Player 1 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 0)
            elif self.frag0 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag1 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag2 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 0)
            elif self.frag3 == fragment and player == 2:
                self.rendered_text_word = self.render_textrect('Player 2 Loses!', self.my_font, self.my_rect, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 1)#last 0 is to left align
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 2)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, FruitsAndVegetables.BLACK, FruitsAndVegetables.WHITE, 1)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, FruitsAndVegetables.RED, FruitsAndVegetables.WHITE, 0)

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
    new_game = FruitsAndVegetables()
    new_game.run()
