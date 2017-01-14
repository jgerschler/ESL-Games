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

myimage0 = pygame.image.load("cloudy.png")
imagerect0 = myimage0.get_rect()
myimage1 = pygame.image.load("cold.png")
myimage2 = pygame.image.load("hot.png")
myimage3 = pygame.image.load("foggy.png")
myimage4 = pygame.image.load("raining.png")
myimage5 = pygame.image.load("sunny.png")
myimage6 = pygame.image.load("stormy.png")
myimage7 = pygame.image.load("windy.png")
myimage8 = pygame.image.load("snowing.png")
myimagevol = pygame.image.load("sound.png")

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
    [myimage0,[["It's cloudy.","a"],["It's cold.","q"],["It's foggy.","q"],["It's raining.","q"]]],
    [myimage1,[["It's cold.","a"],["It's hot.","q"],["It's foggy.","q"],["It's raining.","q"]]],
    [myimage2,[["It's hot.","a"],["It's foggy.","q"],["It's raining.","q"],["It's sunny.","q"]]],
    [myimage3,[["It's foggy.","a"],["It's sunny.","q"],["It's stormy.","q"],["It's raining.","q"]]],
    [myimage4,[["It's raining.","a"],["It's stormy.","q"],["It's sunny.","q"],["It's windy.","q"]]],
    [myimage5,[["It's sunny.","a"],["It's stormy.","q"],["It's windy.","q"],["It's snowing.","q"]]],
    [myimage6,[["It's stormy.","a"],["It's windy.","q"],["It's snowing.","q"],["It's cloudy.","q"]]],
    [myimage7,[["It's windy.","a"],["It's foggy.","q"],["It's sunny.","q"],["It's raining.","q"]]],
    [myimage8,[["It's snowing.","a"],["It's windy.","q"],["It's foggy.","q"],["It's sunny.","q"]]],
    [mysound0,[["It's cloudy.","a"],["It's cold.","q"],["It's foggy.","q"],["It's raining.","q"]]],
    [mysound1,[["It's cold.","a"],["It's hot.","q"],["It's foggy.","q"],["It's raining.","q"]]],
    [mysound2,[["It's hot.","a"],["It's foggy.","q"],["It's raining.","q"],["It's sunny.","q"]]],
    [mysound3,[["It's foggy.","a"],["It's sunny.","q"],["It's stormy.","q"],["It's raining.","q"]]],
    [mysound4,[["It's raining.","a"],["It's stormy.","q"],["It's sunny.","q"],["It's windy.","q"]]],
    [mysound5,[["It's sunny.","a"],["It's stormy.","q"],["It's windy.","q"],["It's snowing.","q"]]],
    [mysound6,[["It's stormy.","a"],["It's windy.","q"],["It's snowing.","q"],["It's cloudy.","q"]]],
    [mysound7,[["It's windy.","a"],["It's foggy.","q"],["It's sunny.","q"],["It's raining.","q"]]],
    [mysound8,[["It's snowing.","a"],["It's windy.","q"],["It's foggy.","q"],["It's sunny.","q"]]],
    ]

    wordlist = random.sample(irregular_verbs,1)[0]
    answer = wordlist[1][0][0]
    random.shuffle(wordlist[1])

    frag0 = wordlist[1][0][0]
    frag1 = wordlist[1][1][0]
    frag2 = wordlist[1][2][0]
    frag3 = wordlist[1][3][0]

    display.fill(WHITE)
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)#center align
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)#right align
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

    if wordlist[0] in (myimage0,myimage1,myimage2,myimage3,myimage4,myimage5,myimage6,myimage7,myimage8):
        display.blit(wordlist[0], (20,(display.get_rect().centery-imagerect0.height/2)))
    else:
        display.blit(myimagevol, (20,(display.get_rect().centery-imagerect0.height/2)))
        wordlist[0].play()
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
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, GREEN, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, GREEN, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, GREEN, WHITE, 0)
        elif frag0 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 1)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, GREEN, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, GREEN, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Wins!", my_font, my_rect, GREEN, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
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
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, RED, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, RED, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 1:
            rendered_text_word = render_textrect("Player 1 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, RED, WHITE, 0)
        elif frag0 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, RED, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, RED, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment and player == 2:
            rendered_text_word = render_textrect("Player 2 Loses!", my_font, my_rect, RED, WHITE, 0)#last 0 is to left align
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
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

mysound0 = pygame.mixer.Sound('itscloudy.ogg')
mysound1 = pygame.mixer.Sound('itscold.ogg')
mysound2 = pygame.mixer.Sound('itshot.ogg')
mysound3 = pygame.mixer.Sound('itsfoggy.ogg')
mysound4 = pygame.mixer.Sound('itsraining.ogg')
mysound5 = pygame.mixer.Sound('itssunny.ogg')
mysound6 = pygame.mixer.Sound('itsstormy.ogg')
mysound7 = pygame.mixer.Sound('itswindy.ogg')
mysound8 = pygame.mixer.Sound('itssnowing.ogg')

display = pygame.display.set_mode((800, 600))

my_font = pygame.font.Font(None, 48)#need to make these relative
my_rect = pygame.Rect((20,268,252,64))
my_rect_frag_1 = pygame.Rect((400,20,252,64))
my_rect_frag_2 = pygame.Rect((400,196,252,64))
my_rect_frag_3 = pygame.Rect((400,340,252,64))
my_rect_frag_4 = pygame.Rect((400,516,252,64))

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
    
