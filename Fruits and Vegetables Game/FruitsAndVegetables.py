import pygame, time, sqlite3, math, random
import pygame.font
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)
YELLOW = (255,229,51)
RED = (255,0,0)
BLUE = (0,0,255)
BROWN = (97,65,38)
PURPLE = (128,0,128)

soundwinfile = "ping.ogg"
soundlossfile = "buzzer.ogg"

myimage0 = pygame.image.load("apple.png")
imagerect0 = myimage0.get_rect()
myimage1 = pygame.image.load("apricot.png")
myimage2 = pygame.image.load("asparagus.png")
myimage3 = pygame.image.load("avocado.png")
myimage4 = pygame.image.load("banana.png")
myimage5 = pygame.image.load("beets.png")
myimage6 = pygame.image.load("bellpepper.png")
myimage7 = pygame.image.load("blueberries.png")
myimage8 = pygame.image.load("broccoli.png")
myimage9 = pygame.image.load("cabbage.png")
myimage10 = pygame.image.load("canteloupe.png")
myimage11 = pygame.image.load("carrots.png")
myimage12 = pygame.image.load("cauliflour.png")
myimage13 = pygame.image.load("celery.png")
myimage14 = pygame.image.load("cherries.png")
myimage15 = pygame.image.load("chilipeppers.png")
myimage16 = pygame.image.load("coconut.png")
myimage17 = pygame.image.load("corn.png")
myimage18 = pygame.image.load("cucumber.png")
myimage19 = pygame.image.load("dragonfruit.png")
myimage20 = pygame.image.load("eggplant.png")
myimage21 = pygame.image.load("garlic.png")
myimage22 = pygame.image.load("ginger.png")
myimage23 = pygame.image.load("grapefruit.png")
myimage24 = pygame.image.load("grapes.png")
myimage25 = pygame.image.load("greenbeans.png")
myimage26 = pygame.image.load("greenonions.png")
myimage27 = pygame.image.load("guava.png")
myimage28 = pygame.image.load("kiwi.png")
myimage29 = pygame.image.load("lettuce.png")
myimage30 = pygame.image.load("limelemon.png")
myimage31 = pygame.image.load("lychee.png")
myimage32 = pygame.image.load("mango.png")
myimage33 = pygame.image.load("melon.png")
myimage34 = pygame.image.load("mushroom.png")
myimage35 = pygame.image.load("olives.png")
myimage36 = pygame.image.load("onion.png")
myimage37 = pygame.image.load("orange.png")
myimage38 = pygame.image.load("papaya.png")
myimage39 = pygame.image.load("passionfruit.png")
myimage40 = pygame.image.load("peach.png")
myimage41 = pygame.image.load("pear.png")
myimage42 = pygame.image.load("peas.png")
myimage43 = pygame.image.load("pineapple.png")
myimage44 = pygame.image.load("plum.png")
myimage45 = pygame.image.load("pomegranate.png")
myimage46 = pygame.image.load("potato.png")
myimage47 = pygame.image.load("pumpkin.png")
myimage48 = pygame.image.load("radishes.png")
myimage49 = pygame.image.load("rambutans.png")
myimage50 = pygame.image.load("raspberries.png")
myimage51 = pygame.image.load("spinach.png")
myimage52 = pygame.image.load("starfruit.png")
myimage53 = pygame.image.load("strawberry.png")
myimage54 = pygame.image.load("sugarcane.png")
myimage55 = pygame.image.load("tomatoes.png")
myimage56 = pygame.image.load("watermelon.png")
myimage57 = pygame.image.load("yam.png")


finished = False

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):#leave this verbose in case we want to use this for other purposes
    
    final_lines = []

    requested_lines = string.splitlines()

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
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
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

def NewUser():
    global frag0
    global frag1
    global frag2
    global frag3
    global wordlist
    global answer

    irregular_verbs = [
    [myimage0,[["apple","a"],["banana","q"],["peach","q"],["orange","q"]]],
    [myimage1,[["apricot","a"],["lemon","q"],["starfruit","q"],["potato","q"]]],
    [myimage2,[["asparagus","a"],["avocado","q"],["banana","q"],["beets","q"]]],
    [myimage3,[["avocado","a"],["tomato","q"],["potato","q"],["celery","q"]]],
    [myimage4,[["banana","a"],["beet","q"],["carrot","q"],["guava","q"]]],
    [myimage5,[["beets","a"],["potatoes","q"],["oranges","q"],["starfruit","q"]]],
    [myimage6,[["bell pepper","a"],["tomato","q"],["orange","q"],["watermelon","q"]]],
    [myimage7,[["blueberries","a"],["broccoli","q"],["corn","q"],["peaches","q"]]],
    [myimage8,[["broccoli","a"],["potato","q"],["orange","q"],["starfruit","q"]]],
    [myimage9,[["cabbage","a"],["cauliflower","q"],["garlic","q"],["ginger","q"]]],
    [myimage10,[["canteloupe","a"],["celery","q"],["lychee","q"],["mango","q"]]],
    [myimage11,[["carrots","a"],["potatoes","q"],["tomatoes","q"],["pears","q"]]],
    [myimage12,[["cauliflower","a"],["garlic","q"],["onion","q"],["olive","q"]]],
    [myimage13,[["celery","a"],["pomegranate","q"],["pea","q"],["radish","q"]]],
    [myimage14,[["cherries","a"],["green beans","q"],["oranges","q"],["green onions","q"]]],
    [myimage15,[["chili peppers","a"],["peas","q"],["rambutans","q"],["tomatoes","q"]]],
    [myimage16,[["coconut","a"],["yam","q"],["pineapple","q"],["plum","q"]]],
    [myimage17,[["corn","a"],["potato","q"],["tomato","q"],["lemon","q"]]],
    [myimage18,[["cucumber","a"],["lime","q"],["carrot","q"],["papaya","q"]]],
    [myimage19,[["dragonfruit","a"],["star fruit","q"],["passion fruit","q"],["peach","q"]]],
    [myimage20,[["eggplant","a"],["potato","q"],["coconut","q"],["spinach","q"]]],
    [myimage21,[["garlic","a"],["beet","q"],["banana","q"],["blueberry","q"]]],
    [myimage22,[["ginger","a"],["garlic","q"],["grape","q"],["olive","q"]]],
    [myimage23,[["grapefruit","a"],["grape","q"],["rambutan","q"],["lychee","q"]]],
    [myimage24,[["grapes","a"],["mushrooms","q"],["olives","q"],["papayas","q"]]],
    [myimage25,[["green beans","a"],["peas","q"],["tomatoes","q"],["pineapples","q"]]],
    [myimage26,[["green onions","a"],["watermelons","q"],["melons","q"],["onions","q"]]],
    [myimage27,[["guava","a"],["star fruit","q"],["passion fruit","q"],["radish","q"]]],
    [myimage28,[["kiwi","a"],["pea","q"],["pear","q"],["pumpkin","q"]]],
    [myimage29,[["lettuce","a"],["spinach","q"],["raspberry","q"],["strawberry","q"]]],
    [myimage30,[["lime/lemons","a"],["potatoes","q"],["oranges","q"],["melons","q"]]],
    [myimage31,[["lychee","a"],["rambutan","q"],["mango","q"],["peach","q"]]],
    [myimage32,[["mango","a"],["potato","q"],["tomato","q"],["olive","q"]]],
    [myimage33,[["melon","a"],["canteloupe","q"],["plum","q"],["watermelon","q"]]],
    [myimage34,[["mushroom","a"],["onion","q"],["pumpkin","q"],["pomegranate","q"]]],
    [myimage35,[["olives","a"],["mushrooms","q"],["blueberries","q"],["raspberries","q"]]],
    [myimage36,[["onion","a"],["potato","q"],["onion","q"],["green onion","q"]]],
    [myimage37,[["orange","a"],["lime","q"],["lemon","q"],["pear","q"]]],
    [myimage38,[["papaya","a"],["potato","q"],["orange","q"],["starfruit","q"]]],
    [myimage39,[["passion fruit","a"],["dragonfruit","q"],["orange","q"],["starfruit","q"]]],
    [myimage40,[["peach","a"],["pear","q"],["plum","q"],["apple","q"]]],
    [myimage41,[["pear","a"],["apricot","q"],["orange","q"],["peach","q"]]],
    [myimage42,[["peas","a"],["green beans","q"],["eggplants","q"],["lemons","q"]]],
    [myimage43,[["pineapple","a"],["lime","q"],["orange","q"],["passion fruit","q"]]],
    [myimage44,[["plum","a"],["peach","q"],["apricot","q"],["broccoli","q"]]],
    [myimage45,[["pomegranate","a"],["plum","q"],["starfruit","q"],["sugarcane","q"]]],
    [myimage46,[["potato","a"],["tomato","q"],["yam","q"],["radish","q"]]],
    [myimage47,[["pumpkin","a"],["rambutan","q"],["lychee","q"],["grapefruit","q"]]],
    [myimage48,[["radishes","a"],["blueberries","q"],["peas","q"],["corn","q"]]],
    [myimage49,[["rambutans","a"],["lychees","q"],["raspberries","q"],["blueberries","q"]]],
    [myimage50,[["raspberries","a"],["blueberries","q"],["rambutans","q"],["lychees","q"]]],
    [myimage51,[["spinach","a"],["lettuce","q"],["cabbage","q"],["radish","q"]]],
    [myimage52,[["starfruit","a"],["passion fruit","q"],["dragonfruit","q"],["grapefruit","q"]]],
    [myimage53,[["strawberry","a"],["blueberry","q"],["raspberry","q"],["blackberry","q"]]],
    [myimage54,[["sugarcane","a"],["mango","q"],["lemon","q"],["tomato","q"]]],
    [myimage55,[["tomatoes","a"],["potatoes","q"],["oranges","q"],["pears","q"]]],
    [myimage56,[["watermelon","a"],["melon","q"],["canteloupe","q"],["grapefruit","q"]]],
    [myimage57,[["yam","a"],["potato","q"],["melon","q"],["garlic","q"]]]
    ]

    wordlist = random.sample(irregular_verbs,1)[0]
    answer = wordlist[1][0][0]
    random.shuffle(wordlist[1])

    frag0 = wordlist[1][0][0]
    frag1 = wordlist[1][1][0]
    frag2 = wordlist[1][2][0]
    frag3 = wordlist[1][3][0]

    display.fill(WHITE)
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)#center align
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)#right align
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)

    display.blit(wordlist[0], ((display.get_rect().centerx-imagerect0.width/2),(display.get_rect().centery-imagerect0.height/2)))
    display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
    display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
    display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
    display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

    pygame.display.update()

    return

def DeactivateKeys():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return

def RefreshScreen(fragment, player):
    global frag0
    global frag1
    global frag2
    global frag3
    global wordlist
    global answer
    
    if fragment == answer:#winner!
        display.fill(WHITE)
        if frag0 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, GREEN, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, GREEN, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, GREEN, WHITE, 0)
        elif frag0 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, GREEN, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, GREEN, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, GREEN, WHITE, 0)

        display.blit(rendered_text_word, my_rect.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)
        pygame.display.update()
        soundwin.play()
        DeactivateKeys()

    if fragment != answer:#loser
        display.fill(WHITE)
        if frag0 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, RED, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, RED, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, RED, WHITE, 0)
        elif frag0 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, RED, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, RED, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, RED, WHITE, 0)

        display.blit(rendered_text_word, my_rect.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)
        pygame.display.update()
        soundloss.play()
        DeactivateKeys()

pygame.init()

pygame.mixer.init()

soundwin = pygame.mixer.Sound(soundwinfile)
soundloss = pygame.mixer.Sound(soundlossfile)

display = pygame.display.set_mode((800, 600))

my_font = pygame.font.Font(None, 48)#need to make these relative
my_rect = pygame.Rect((273,268,252,64))
my_rect_frag_1 = pygame.Rect((273,20,252,64))
my_rect_frag_2 = pygame.Rect((527,268,252,64))
my_rect_frag_3 = pygame.Rect((273,516,252,64))
my_rect_frag_4 = pygame.Rect((20,268,252,64))

display.fill(WHITE)

pygame.display.update()

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                NewUser()
            if event.key == pygame.K_a:
                RefreshScreen(frag0, player=1)
            elif event.key == pygame.K_e:
                RefreshScreen(frag0, player=2)
            elif event.key == pygame.K_b:
                RefreshScreen(frag1, player=1)
            elif event.key == pygame.K_f:
                RefreshScreen(frag1, player=2)
            elif event.key == pygame.K_c:
                RefreshScreen(frag2, player=1)
            elif event.key == pygame.K_g:
                RefreshScreen(frag2, player=2)
            elif event.key == pygame.K_d:
                RefreshScreen(frag3, player=1)
            elif event.key == pygame.K_h:
                RefreshScreen(frag3, player=2)
            else:
                pass
           
    pygame.display.update()
    
