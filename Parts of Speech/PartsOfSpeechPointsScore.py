#!/usr/bin/env python
import pygame
import time
import math
import sqlite3
import random
import pygame.font
from pygame.locals import *
import sys

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message
        
class PartsOfSpeech(object):
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

        self.score = 0
        self.start_time = 60
        
        try:
            self.conn = sqlite3.connect('student.db')# connect to database
        except:
            print("Database not found!")

        self.c = self.conn.cursor()

        self.sound_win = pygame.mixer.Sound('audio\\ping.ogg')
        self.sound_loss = pygame.mixer.Sound('audio\\buzzer.ogg')        

        self.my_font = pygame.font.Font(None, 48)
        self.my_rect = pygame.Rect((20, 100, 760, 240))
        self.my_rect_user = pygame.Rect((20, 20, 760, 80))
        self.my_rect_frag_1 = pygame.Rect((20, 340, 760, 65))
        self.my_rect_frag_2 = pygame.Rect((20, 405, 760, 65))
        self.my_rect_frag_3 = pygame.Rect((20, 470, 760, 65))
        self.my_rect_frag_4 = pygame.Rect((20, 535, 760, 65))

        self.display = pygame.display.set_mode((800, 600))# change to desired resolution -- you'll need to modify rect size.
        pygame.display.set_caption("Parts of Speech Game")
        self.display.fill(PartsOfSpeech.WHITE)

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
                raise TextRectException("After word wrap, the text string was too tall to fit in the provided rect.")
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

    def special_render_textrect(self, string, font, rect, text_color, special_color, background_color, justification=0):

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
                raise TextRectException("After word wrap, the text string was too tall to fit in the provided rect.")
            if line != "":
                if self.sentence_pos_word in line:
                    tempsurface = font.render(line[0:line.index(self.sentence_pos_word)], 1, text_color)
                    tempsurface1 = font.render(self.sentence_pos_word, 1, special_color)
                    tempsurface2 = font.render(line[line.index(self.sentence_pos_word)+len(self.sentence_pos_word):-1], 1, text_color)
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
                        raise TextRectException("Invalid justification argument: " + str(justification))
            accumulated_height += font.size(line)[1]

        return surface

    def new_user(self):
        self.pos_list = ["noun","verb","adjective","adverb","conjunction","preposition","proper noun","interjection","possessive pronoun","pronoun","article","possessive noun"]

        sentence_list = [["The English rock band Pink Floyd released the album Dark Side of the Moon in 1973.",[["band","noun"],["album","noun"],["released","verb"],["Dark","adjective"]]],
                        ["In 1969, NASA astronauts on the Apollo 10 space mission heard what sounded like outer-space music.",[["outer-space","adjective"],["sounded","verb"],["on","pre"],["mission","noun"]]],
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
                        ["He was on the lam from 2001 to 2014 after the first prison break.",[["break","noun"],["He","pronoun"],["first","adjective"],["prison","adjective"]]],
                        ["He was serving a 20-year sentence for murder and drug trafficking.",[["murder","noun"],["20-year","adjective"],["drug","adjective"],["serving","verb"]]],
                        ["Rolling Stone magazine published Penn's interview online January 11.",[["magazine","noun"],["published","verb"],["January","proper noun"],["interview","noun"]]],
                        ["Mexican federal police recaptured El Chapo a day earlier.",[["day","noun"],["recaptured","verb"],["federal","adjective"],["day","noun"]]],
                        ["In his article, Penn explained why he wanted to meet the crime leader.",[["article","noun"],["his","possessive pronoun"],["explained","verb"],["wanted","verb"]]],
                        ["Penn is a longtime political activist.",[["activist","noun"],["Penn","proper noun"],["longtime","adjective"],["political","activist"]]],
                        ["He has involved himself in international affairs at high levels.",[["levels","noun"],["international","adjective"],["high","adjective"],["involved","verb"]]],
                        ["In 2007, he met and befriended Hugo Chavez, who was then the socialist president of Venezuela.",[["president","noun"],["Venezuela","proper noun"],["befriended","verb"],["socialist","adjective"]]],
                        ["The US government was not a fan of Chavez, who allied himself with Cuban leaders Fidel and Raul Castro.",[["fan","noun"],["Cuban","adjective"],["allied","verb"],["with","preposition"]]],
                        ["Penn also has met with Raul Castro.",[["Raul Castro","proper noun"],["met","verb"],["Penn","proper noun"],["has","verb"]]],
                        ["He got involved in the Falklands dispute between Britain and Argentina.",[["dispute","noun"],["the","article"],["involved","verb"],["Argentina","proper noun"]]],
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
                        ["A Russian spacecraft traveling to the International Space Station Thursday had to make an emergency landing when a rocket engine failed to fire.",[["Russian","adjective"],["emergency","adjective"],["Thursday","proper noun"],["make","verb"]]],
                        ["About two minutes after launching, the three-stage Soyuz booster rocket suffered an unspecified failure of its second stage.",[["failure","noun"],["three-stage","adjective"],["two","adjective"],["rocket","noun"]]],
                        ["The Russian space program has suffered several failures in recent years.",[["years","noun"],["suffered","verb"],["program","noun"],["several","adjective"]]],
                        ["The cosmonauts safely escaped in that accident as well.",[["cosmonauts","noun"],["safely","adverb"],["accident","noun"],["the","article"]]],
                        ["Relations between the U.S. and Russia have been very tense in recent years.",[["Relations","noun"],["very","adverb"],["Russia","proper noun"],["tense","adjective"]]],
                        ["However, the two sides have continued their cooperation in space.",[["space","noun"],["two","adjective"],["sides","noun"],["continued","verb"]]],
                        ["Weather officials believe the storm will pass over North and South Carolina before heading out to the Atlantic Ocean in coming days.",[["before","preposition"],["the","article"],["South Carolina","proper noun"],["heading","verb"]]],
                        ["Wood and metal from destroyed buildings covered streets and moved through flooded neighborhoods.",[["neighborhoods","noun"],["flooded","adjective"],["metal","noun"],["covered","verb"]]],
                        ["Rick Scott is the governor of Florida.",[["governor","noun"],["the","article"],["Rick Scott","proper noun"],["is","verb"]]],
                        ["Ouch! I just broke my leg.",[["Ouch!","interjection"],["broke","verb"],["my","possessive adjective"],["I","pronoun"]]],
                        ["Holy Moly! I love mole.",[["mole","noun"],["Holy Moly!","interjection"],["I","pronoun"],["love","verb"]]],
                        ["Don't touch Ivan's green pochocuiles.",[["pochocuiles","noun"],["Ivan's","possessive noun"],["green","adjective"],["touch","verb"]]],
                        ["Concha and Briseida quickly run to El Chontal.",[["quickly","adverb"],["and","conjunction"],["El Chontal","proper noun"],["run","verb"]]],
                        ["Diego hungrily swallows the gross taco.",[["taco","noun"],["the","article"],["gross","adjective"],["hungrily","adverb"]]],
                        ["Florizet loudly said 'Oh my God!'.",[["said","verb"],["Oh my God!","interjection"],["Florizet","proper noun"],["loudly","adverb"]]],
                        ["Jennifer hurriedly danced with La Chenta at the Video Bar.",[["hurriedly","adverb"],["the","article"],["Jennifer","proper noun"],["danced","verb"]]],
                        ["Silvia likes to read romantic anime.",[["romantic","adjective"],["anime","noun"],["Silvia","proper noun"],["read","verb"]]],
                        ["Yoaly and Jesus secretly pretend not to see the teacher.",[["not","adverb"],["secretly","adverb"],["and","conjunction"],["pretend","verb"]]],
                        ["More than 98 million of the world's adolescent girls do not go to school.",[["world's","possessive noun"],["adolescent","adjective"],["not","adverb"],["go","verb"]]],
                        ["Jacob Ostreicher had been jailed for months and never charged with a crime.",[["months","noun"],["jailed","verb"],["Jacob Ostreicher","proper noun"],["with","preposition"]]]]

        self.c.execute('select * from users order by random() limit 1;')
        userdata = self.c.fetchone()
        self.username = str(userdata[1])
        self.sentence = sentence_list[random.randint(0,len(sentence_list)-1)]
        self.plain_sentence = self.sentence[0]
        sentence_pos = self.sentence[1][random.randint(0,len(sentence_list[1])-1)]
        self.sentence_pos_word = sentence_pos[0]
        self.sentence_pos_wordIND = sentence_pos[1]
        answerlist = random.sample(self.pos_list,3)
        while sentence_pos[1] in answerlist:
            answerlist = random.sample(self.pos_list,3)
        answerlist.append(sentence_pos[1])
        random.shuffle(answerlist)
        
        self.frag0 = answerlist[0]
        self.frag1 = answerlist[1]
        self.frag2 = answerlist[2]
        self.frag3 = answerlist[3]

        self.display.fill(PartsOfSpeech.WHITE)
        self.rendered_text = self.special_render_textrect(self.plain_sentence, self.my_font, self.my_rect, PartsOfSpeech.BLACK, PartsOfSpeech.PURPLE, PartsOfSpeech.WHITE, 1)
        self.rendered_text_user = self.render_textrect("SCORE: {0}, TIME: {1}".format(self.score, round(self.start_time - self.seconds, 0)), self.my_font, self.my_rect_user, PartsOfSpeech.BROWN, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.RED, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.YELLOW, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.GREEN, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLUE, PartsOfSpeech.WHITE, 0)

        self.display.blit(self.rendered_text, self.my_rect.topleft)
        self.display.blit(self.rendered_text_user, self.my_rect_user.topleft)
        self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
        self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
        self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
        self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)

        pygame.display.update()

        return

    def refresh_screen(self, fragment):
        if fragment == self.sentence_pos_wordIND:#winner!
            self.score += 1
            self.display.fill(PartsOfSpeech.WHITE)
            rendered_text = self.special_render_textrect(self.plain_sentence, self.my_font, self.my_rect, PartsOfSpeech.BLACK, PartsOfSpeech.PURPLE, PartsOfSpeech.WHITE, 1)#need to figure out how to bold or color the word we want
            rendered_text_user = self.render_textrect("SCORE: {0}, TIME: {1}".format(self.score, round(self.start_time - self.seconds, 0)), self.my_font, self.my_rect_user, PartsOfSpeech.BROWN, PartsOfSpeech.WHITE, 0)#last 0 is to left align
            if self.frag0 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.GREEN, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
            elif self.frag1 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.GREEN, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
            elif self.frag2 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.GREEN, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
            elif self.frag3 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.GREEN, PartsOfSpeech.WHITE, 0)
            else:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)     

            self.display.blit(self.rendered_text, self.my_rect.topleft)
            self.display.blit(self.rendered_text_user, self.my_rect_user.topleft)
            self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
            self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
            self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
            self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)

            pygame.display.update()
            self.sound_win.play()

            return

        if fragment != self.sentence_pos_wordIND:#loser
            self.score -= 1
            self.display.fill(PartsOfSpeech.WHITE)
            self.rendered_text = self.special_render_textrect(self.plain_sentence, self.my_font, self.my_rect, PartsOfSpeech.BLACK, PartsOfSpeech.PURPLE, PartsOfSpeech.WHITE, 1)
            self.rendered_text_user = self.render_textrect("SCORE: {0}, TIME: {1}".format(self.score, round(self.start_time - self.seconds, 0)), self.my_font, self.my_rect_user, PartsOfSpeech.BROWN, PartsOfSpeech.WHITE, 0)
            if self.frag0 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.RED, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
            elif self.frag1 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.RED, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
            elif self.frag2 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.RED, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
            elif self.frag3 == fragment:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.RED, PartsOfSpeech.WHITE, 0)
            else:
                self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)
                self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLACK, PartsOfSpeech.WHITE, 0)     

            self.display.blit(self.rendered_text, self.my_rect.topleft)
            self.display.blit(self.rendered_text_user, self.my_rect_user.topleft)
            self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
            self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
            self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
            self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)

            pygame.display.update()
            self.sound_loss.play()

            return

        self.display.fill(PartsOfSpeech.WHITE)
        self.rendered_text = self.special_render_textrect(self.plain_sentence, self.my_font, self.my_rect, PartsOfSpeech.BLACK, PartsOfSpeech.PURPLE, PartsOfSpeech.WHITE, 1)
        self.rendered_text_user = self.render_textrect("SCORE: {0}, TIME: {1}".format(self.score, round(self.start_time - self.seconds, 0)), self.my_font, self.my_rect_user, PartsOfSpeech.BROWN, PartsOfSpeech.WHITE, 0)#last 0 is to left align
        self.rendered_text_frag_1 = self.render_textrect(self.frag0, self.my_font, self.my_rect_frag_1, PartsOfSpeech.RED, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_2 = self.render_textrect(self.frag1, self.my_font, self.my_rect_frag_2, PartsOfSpeech.YELLOW, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_3 = self.render_textrect(self.frag2, self.my_font, self.my_rect_frag_3, PartsOfSpeech.GREEN, PartsOfSpeech.WHITE, 0)
        self.rendered_text_frag_4 = self.render_textrect(self.frag3, self.my_font, self.my_rect_frag_4, PartsOfSpeech.BLUE, PartsOfSpeech.WHITE, 0)

        self.display.blit(self.rendered_text, self.my_rect.topleft)
        self.display.blit(self.rendered_text_user, self.my_rect_user.topleft)
        self.display.blit(self.rendered_text_frag_1, self.my_rect_frag_1.topleft)
        self.display.blit(self.rendered_text_frag_2, self.my_rect_frag_2.topleft)
        self.display.blit(self.rendered_text_frag_3, self.my_rect_frag_3.topleft)
        self.display.blit(self.rendered_text_frag_4, self.my_rect_frag_4.topleft)

        pygame.display.update()

        return

    def run(self):
        self.start_ticks = pygame.time.get_ticks()# not needed
        while not self.finished:
            self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
            if 60 - self.seconds <= 0:
                print(self.score)
                self.finished = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.conn.close()
                    self.finished = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.new_user()
                    if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
                        if self.frag0 != "":
                            self.refresh_screen(self.frag0)
                        else:
                            pass
                    if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
                        if self.frag1 != "":
                            self.refresh_screen(self.frag1)
                        else:
                            pass
                    if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
                        if self.frag2 != "":
                            self.refresh_screen(self.frag2)
                        else:
                            pass
                    if event.key in (pygame.K_d,pygame.K_h,pygame.K_l,pygame.K_p,pygame.K_t,pygame.K_x):
                        if self.frag3 != "":
                            self.refresh_screen(self.frag3)
                        else:
                            pass
                    
            pygame.display.update()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    new_game = PartsOfSpeech()
    new_game.run()
