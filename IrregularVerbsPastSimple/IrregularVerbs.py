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
    ["be",[["was/were","a"],["been","q"],["being","q"],["is","q"]]],
    ["bear",[["bore","a"],["born","q"],["bears","q"],["bearing","q"]]],
    ["beat",[["beat","a"],["beaten","q"],["beating","q"],["beats","q"]]],
    ["begin",[["began","a"],["begun","q"],["beginning","q"],["begins","q"]]],
    ["bite",[["bit","a"],["bitten","q"],["biting","q"],["bite","q"]]],
    ["blow",[["blew","a"],["blown","q"],["blows","q"],["blowing","q"]]],
    ["broadcast",[["broadcast","a"],["broadcasting","q"],["broadcasts","q"],["broadcaster","q"]]],
    ["break",[["broke","a"],["broken","q"],["breaked","q"],["breaking","q"]]],
    ["bring",[["brought","a"],["bringing","q"],["brings","q"],["brung","q"]]],
    ["build",[["built","a"],["building","q"],["builded","q"],["builds","q"]]],
    ["buy",[["bought","a"],["buying","q"],["buys","q"],["buy","q"]]],
    ["can",[["could","a"],["cans","q"],["canning","q"],["can","q"]]],
    ["catch",[["caught","a"],["catched","q"],["catches","q"],["catching","q"]]],
    ["choose",[["chose","a"],["choose","q"],["choosed","q"],["choosing","q"]]],
    ["come",[["came","a"],["coming","q"],["comed","q"],["comes","q"]]],
    ["cost",[["cost","a"],["costs","q"],["costed","q"],["costing","q"]]],
    ["cut",[["cut","a"],["cutted","q"],["cutter","q"],["cutting","q"]]],
    ["do",[["did","a"],["doing","q"],["doed","q"],["does","q"]]],
    ["draw",[["drew","a"],["drawn","q"],["draw","q"],["drawing","q"]]],
    ["drink",[["drank","a"],["drinked","q"],["drink","q"],["drunk","q"]]],
    ["drive",[["drove","a"],["drives","q"],["driven","q"],["driving","q"]]],
    ["eat",[["ate","a"],["eaten","q"],["eats","q"],["eating","q"]]],
    ["fall",[["fell","a"],["fallen","q"],["falls","q"],["fall","q"]]],
    ["feed",[["fed","a"],["feeding","q"],["feeds","q"],["felt","q"]]],
    ["feel",[["felt","a"],["feeling","q"],["feels","q"],["feel","q"]]],
    ["fight",[["fought","a"],["fighting","q"],["fights","q"],["fight","q"]]],
    ["find",[["found","a"],["finding","q"],["find","q"],["finds","q"]]],
    ["fly",[["flew","a"],["flown","q"],["flies","q"],["fly","q"]]],
    ["forget",[["forgot","a"],["forget","q"],["forgotten","q"],["forgets","q"]]],
    ["freeze",[["froze","a"],["frozen","q"],["freeze","q"],["freezes","q"]]],
    ["get",[["got","a"],["gotten","q"],["get","q"],["gets","q"]]],
    ["give",[["gave","a"],["given","q"],["give","q"],["gives","q"]]],
    ["go",[["went","a"],["gone","q"],["goes","q"],["going","q"]]],
    ["grow",[["grew","a"],["grown","q"],["grows","q"],["grow","q"]]],
    ["hang",[["hung","a"],["hangs","q"],["hanging","q"],["hanger","q"]]],
    ["have",[["had","a"],["have","q"],["has","q"],["halved","q"]]],
    ["hear",[["heard","a"],["hears","q"],["hearing","q"],["hear","q"]]],
    ["hide",[["hid","a"],["hidden","q"],["hide","q"],["hides","q"]]],
    ["hit",[["hit","a"],["hits","q"],["hitting","q"],["hitted","q"]]],
    ["hold",[["held","a"],["hold","q"],["holds","q"],["holding","q"]]],
    ["hurt",[["hurt","a"],["hurting","q"],["hurts","q"],["hurted","q"]]],
    ["keep",[["kept","a"],["keeps","q"],["keep","q"],["keeping","q"]]],
    ["know",[["knew","a"],["known","q"],["knows","q"],["knowing","q"]]],
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
    ["ride",[["rode","a"],["ridden","q"],["riding","q"],["ride","q"]]],
    ["ring",[["rang","a"],["rung","q"],["ring","q"],["ringer","q"]]],
    ["rise",[["rose","a"],["risen","q"],["rise","q"],["rises","q"]]],
    ["run",[["ran","a"],["run","q"],["running","q"],["runs","q"]]],
    ["say",[["said","a"],["says","q"],["say","q"],["saying","q"]]],
    ["see",[["saw","a"],["seen","q"],["see","q"],["sees","q"]]],
    ["sell",[["sold","a"],["sell","q"],["sells","q"],["selling","q"]]],
    ["send",[["sent","a"],["sends","q"],["sending","q"],["send","q"]]],
    ["set",[["set","a"],["setting","q"],["sets","q"],["setted","q"]]],
    ["shoot",[["shot","a"],["shooting","q"],["shoot","q"],["shooted","q"]]],
    ["shut",[["shut","a"],["shutting","q"],["shuts","q"],["shutted","q"]]],
    ["sing",[["sang","a"],["sung","q"],["sings","q"],["singing","q"]]],
    ["sit",[["sat","a"],["sits","q"],["sitting","q"],["sitted","q"]]],
    ["sleep",[["slept","a"],["sleeping","q"],["sleep","q"],["sleeps","q"]]],
    ["speak",[["spoke","a"],["spoken","q"],["speaks","q"],["speaking","q"]]],
    ["spend",[["spent","a"],["spend","q"],["spending","q"],["spends","q"]]],
    ["stand",[["stood","a"],["stands","q"],["stand","q"],["standing","q"]]],
    ["steal",[["stole","a"],["stolen","q"],["steal","q"],["steals","q"]]],
    ["stick",[["stuck","a"],["sticked","q"],["sticking","q"],["stick","q"]]],
    ["swim",[["swam","a"],["swum","q"],["swim","q"],["swimming","q"]]],
    ["take",[["took","a"],["taken","q"],["takes","q"],["take","q"]]],
    ["teach",[["taught","a"],["teached","q"],["teach","q"],["teaches","q"]]],
    ["tell",[["told","a"],["tells","q"],["telling","q"],["telled","q"]]],
    ["think",[["thought","a"],["thinks","q"],["think","q"],["thinked","q"]]],
    ["throw",[["threw","a"],["thrown","q"],["throw","q"],["throws","q"]]],
    ["wake",[["woke","a"],["woken","q"],["wake","q"],["waked","q"]]],
    ["wear",[["wore","a"],["worn","q"],["wear","q"],["wears","q"]]],
    ["win",[["won","a"],["wins","q"],["win","q"],["winning","q"]]],
    ["write",[["wrote","a"],["written","q"],["write","q"],["writes","q"]]]
    ]

    wordlist = random.sample(irregular_verbs,1)[0]
    answer = wordlist[1][0][0]
    random.shuffle(wordlist[1])

    frag0 = wordlist[1][0][0]
    frag1 = wordlist[1][1][0]
    frag2 = wordlist[1][2][0]
    frag3 = wordlist[1][3][0]

    display.fill(WHITE)
    rendered_text_word = render_textrect(wordlist[0], my_font, my_rect, PURPLE, WHITE, 1)
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 1)#center align
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 2)#right align
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 1)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)

    display.blit(rendered_text_word, my_rect.topleft)
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
    
