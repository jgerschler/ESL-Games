import pygame, time, sqlite3, math, random
import pygame.font
from pygame.locals import *

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)
YELLOW = (255,229,51)
RED = (255,0,0)
BLUE = (0,0,255)
BROWN = (97,65,38)
PURPLE = (128,0,128)

soundwinfile = "audio\\ping.ogg"
soundlossfile = "audio\\buzzer.ogg"

finished = False

constructedsentence = ""



def render_textrect(string, font, rect, text_color, background_color, justification=0):
    
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

def special_render_textrect(string, font, rect, text_color, special_color, background_color, justification=0):#this could be removed but we'll leave it for now for future modification?

    global sentencePOSword
    
    final_lines = []

    requested_lines = string.splitlines()

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')#if sentence is too big for rectangle, then split up using spaces into words.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."#if the word is still too big for the rect, then raise an exception.
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "   
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line #make a test line, check if it fits in the rectangle then save and add another word if it fits.
                else: 
                    final_lines.append(accumulated_line) #otherwise just add the fragment to the final lines list
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
            if sentencePOSword in line:
                #make surfaces
                tempsurface = font.render(line[0:line.index(sentencePOSword)], 1, text_color)
                tempsurface1 = font.render(sentencePOSword, 1, special_color)
                tempsurface2 = font.render(line[line.index(sentencePOSword)+len(sentencePOSword):-1], 1, text_color)
                surface.blit(tempsurface, (0, accumulated_height))
                surface.blit(tempsurface1, (tempsurface.get_width(), accumulated_height))
                surface.blit(tempsurface2, (tempsurface.get_width()+tempsurface1.get_width(), accumulated_height))
                        
            else:
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
    global username
    global sentence
    global plainsentence
    global POSlist
    global sentencePOSword
    global sentencePOSwordIND

    POSlist = ["noun","verb","adjective","adverb","conjunction","preposition","proper noun","interjection","possessive pronoun","pronoun"]

    sentencelist = [["The English rock band Pink Floyd released the album Dark Side of the Moon in 1973.",[["band","noun"],["album","noun"],["released","verb"],["Dark","adjective"]]],
                    ["In 1969, NASA astronauts on the Apollo 10 space mission heard what sounded like outer-space music.",[["outer-space","noun"],["sounded","verb"],["on","pre"],["mission","noun"]]],
                    ["Nearly 50 years later, those mysterious noises on Apollo 10 have become a trending topic on social media.",[["topic","noun"],["noises","noun"],["mysterious","adjective"],["trending","adjective"]]],
                    ["In May of 1969, the Apollo 10 crew approached the far side of the moon.",[["crew","noun"],["May","proper noun"],["approached","verb"],["far","adjective"]]],
                    ["The three astronauts, Thomas Stafford, John Young, and Eugene Cernan, would have no contact with the Earth.",[["astronauts","noun"],["Eugene Cernan","proper noun"],["John Young","proper noun"],["three","adjective"]]],
                    ["But just as they approached the far side of the moon, the crew heard strange music.",[["moon","noun"],["strange","adjective"],["music","noun"],["they","pronoun"]]],
                    ["That was the conversation between astronauts Eugene Cernan and John Young after hearing the strange sounds.",[["conversation","noun"],["hearing","verb"],["after","con"],["and","con"]]],
                    ["The story of the unusual space noises will appear on a television series called NASA's Unexplained Files.",[["television","noun"],["unusual","adjective"],["story","noun"],["appear","verb"]]],
                    ["A preview of the episode appeared on YouTube earlier this week.",[["week","noun"],["appeared","verb"],["YouTube","proper noun"],["on","preposition"]]],
                    ["Some news reports and social media posts wrongly said that the Apollo 10 audio files were recently made public.",[["files","noun"],["and","conjunction"],["said","verb"],["recently","adverb"]]],
                    ["There has been praise and condemnation for Hollywood star Sean Penn this week.",[["praise","noun"],["Sean Penn","proper noun"],["and","conjunction"],["been","verb"]]],
                    ["Sean Penn has had controversial moments throughout his public life.",[["life","noun"],["has","verb"],["his","possessive pronoun"],["throughout","preposition"]]],
                    ["This week, the public learned that Penn met with the leader of a brutal Mexican crime group.",[["group","noun"],["learned","verb"],["brutal","adjective"],["with","preposition"]]],
                    ["The actor interviewed Joaquin Guzman in October 2015.",[["actor","noun"],["interviewed","verb"],["October","proper noun"],["Joaquin Guzman","proper noun"]]],
                    ["Guzman had escaped from a Mexican federal prison in July.",[["prison","noun"],["federal","adjective"],["in","preposition"],["escaped","verb"]]],
                    ["It was his second escape.",[["escape","noun"],["second","adjective"],["It","pronoun"],["his","possessive pronoun"]]],
                    ["He was on the lam from 2001 to 2014 after the first prison break.",[["prison","noun"],["He","pronoun"],["first","adjective"],["prison break","noun"]]],
                    ["He was serving a 20-year sentence for murder and drug trafficking.",[["murder","noun"],["20-year","adjective"],["drug","adjective"],["serving","verb"]]],
                    ["Rolling Stone magazine published Penn's interview online January 11.",[["magazine","noun"],["published","verb"],["January","proper noun"],["interview","noun"]]],
                    ["Mexican federal police recaptured El Chapo a day earlier.",[["day","noun"],["recaptured","verb"],["federal","adjective"],["day","noun"]]],
                    ["In his article, Penn explained why he wanted to meet the crime leader.",[["article","noun"],["his","possessive pronoun"],["explained","verb"],["wanted","verb"]]],
                    ["Penn is a longtime political activist.",[["activist","noun"],["Penn","proper noun"],["longtime","adjective"],["political","activist"]]],
                    ["He has involved himself in international affairs at high levels.",[["levels","noun"],["international","adjective"],["high","adjective"],["involved","verb"]]],
                    ["In 2007, he met and befriended Hugo Chavez, who was then the socialist president of Venezuela.",[["president","noun"],["Venezuela","proper noun"],["befriended","verb"],["socialist","adjective"]]],
                    ["The US government was not a fan of Chavez, who allied himself with Cuban leaders Fidel and Raul Castro.",[["fan","noun"],["Cuban","adjective"],["allied","verb"],["with","preposition"]]],
                    ["Penn also has met with Raul Castro.",[["Raul Castro","proper noun"],["met","verb"],["Penn","proper noun"],["has","verb"]]],
                    ["He got involved in the Falklands dispute between Britain and Argentina.",[["dispute","noun"],["in","preposition"],["involved","verb"],["Argentina","proper noun"]]],
                    ["The actor met with Argentinian President Cristina Fernandez de Kirchner in 2012, after Britain made military moves toward Argentina.",[["actor","noun"],["Argentinian","proper noun"],["after","preposition"],["toward","preposition"]]],
                    ["Penn sided with Argentina in that dispute.",[["dispute","noun"],["sided","verb"],["Argentina","proper noun"],["Penn","proper noun"]]],
                    ["Penn has written about his experiences for the news media before.",[["experiences","noun"],["his","possessive pronoun"],["about","preposition"],["news","adjective"]]],
                    ["He visited Iraq in 2004, and Iran the following year.",[["year","noun"],["visited","verb"],["Iran","proper noun"],["He","pronoun"]]],
                    ["He wrote about those experiences for the San Francisco Chronicle.",[["experiences","noun"],["about","preposition"],["San Francisco Chronicle","proper noun"],["for","preposition"]]],
                    ["Penn had been to Iraq earlier to protest international military strikes against the country.",[["strikes","noun"],["Iraq","proper noun"],["to","preposition"],["against","preposition"]]],
                    ["The star also helped in times of natural disaster.",[["star","noun"],["disaster","noun"],["in","preposition"],["natural","adjective"]]],
                    ["He started a foundation to help victims of the earthquake in Haiti.",[["earthquake","noun"],["started","verb"],["help","verb"],["Haiti","proper noun"]]],
                    ["He also went to New Orleans shortly after Hurricane Katrina and reportedly rescued some survivors.",[["survivors","noun"],["after","preposition"],["New Orleans","proper noun"],["rescued","verb"]]],
                    ["Wow! In 2012, Sean Penn went to Bolivia to visit a US businessman jailed there.",[["businessman","noun"],["Wow!","interjection"],["Bolivia","proper noun"],["visit","verb"]]],
                    ["Jacob Ostreicher had been jailed for months and never charged with a crime.",[["months","noun"],["jailed","verb"],["Jacob Ostreicher","proper noun"],["with","preposition"]]]]

    c.execute('select * from users order by random() limit 1;')
    userdata = c.fetchone()
    username = str(userdata[1])
    #c.execute('select * from sentences order by random() limit 1;')
    #sentencedata = c.fetchone()
    #sentence = str(sentencedata[1])
    sentence = sentencelist[random.randint(0,len(sentencelist)-1)]
    plainsentence = sentence[0]
    sentencePOS = sentence[1][random.randint(0,len(sentencelist[1])-1)]
    sentencePOSword = sentencePOS[0]
    sentencePOSwordIND = sentencePOS[1]
    answerlist = random.sample(POSlist,3)
    while sentencePOS[1] in answerlist:
        answerlist = random.sample(POSlist,3)
    answerlist.append(sentencePOS[1])
    random.shuffle(answerlist)
    
    frag0 = answerlist[0]
    frag1 = answerlist[1]
    frag2 = answerlist[2]
    frag3 = answerlist[3]

    display.fill(WHITE)
    rendered_text = special_render_textrect(plainsentence, my_font, my_rect, BLACK, PURPLE, WHITE, 1)#need to figure out how to bold or color the word we want
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

def RefreshScreen(fragment):
    global frag0
    global frag1
    global frag2
    global frag3
    global username
    global sentence
    global plainsentence
    global POSlist
    global sentencePOSword
    global sentencePOSwordIND

    if fragment == sentencePOSwordIND:#winner!
        display.fill(WHITE)
        rendered_text = special_render_textrect(plainsentence, my_font, my_rect, BLACK, PURPLE, WHITE, 1)#need to figure out how to bold or color the word we want
        rendered_text_user = render_textrect(username, my_font, my_rect_user, BROWN, WHITE, 0)#last 0 is to left align
        if frag0 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, GREEN, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, GREEN, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, GREEN, WHITE, 0)
        else:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)     

        display.blit(rendered_text, my_rect.topleft)
        display.blit(rendered_text_user, my_rect_user.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

        pygame.display.update()
        soundwin.play()

        return

    if fragment != sentencePOSwordIND:#loser
        display.fill(WHITE)
        rendered_text = special_render_textrect(plainsentence, my_font, my_rect, BLACK, PURPLE, WHITE, 1)#need to figure out how to bold or color the word we want
        rendered_text_user = render_textrect(username, my_font, my_rect_user, BROWN, WHITE, 0)#last 0 is to left align
        if frag0 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag1 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, RED, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag2 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, RED, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)
        elif frag3 == fragment:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, RED, WHITE, 0)
        else:
            rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, BLACK, WHITE, 0)
            rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, BLACK, WHITE, 0)
            rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, BLACK, WHITE, 0)
            rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLACK, WHITE, 0)     

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
    rendered_text = special_render_textrect(plainsentence, my_font, my_rect, BLACK, PURPLE, WHITE, 1)
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

display = pygame.display.set_mode((800, 600))

my_font = pygame.font.Font(None, 48)
my_rect = pygame.Rect((20, 100, 760, 240))
my_rect_user = pygame.Rect((20, 20, 760, 80))
my_rect_frag_1 = pygame.Rect((20, 340, 760, 65))
my_rect_frag_2 = pygame.Rect((20, 405, 760, 65))
my_rect_frag_3 = pygame.Rect((20, 470, 760, 65))
my_rect_frag_4 = pygame.Rect((20, 535, 760, 65))

display.fill(WHITE)

pygame.display.update()

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                NewUser()
            if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
                if frag0 != "":
                    RefreshScreen(frag0)
                else:
                    pass
            if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
                if frag1 != "":
                    RefreshScreen(frag1)
                else:
                    pass
            if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
                if frag2 != "":
                    RefreshScreen(frag2)
                else:
                    pass
            if event.key in (pygame.K_d,pygame.K_h,pygame.K_l,pygame.K_p,pygame.K_t,pygame.K_x):
                if frag3 != "":
                    RefreshScreen(frag3)
                else:
                    pass
            
    pygame.display.update()

##conn.close()
