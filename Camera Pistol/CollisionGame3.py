#!/usr/bin/env python
from pygame.locals import *
import imutils
import cv2
import pygame
import random
import sys
import math



class PistolGame(object):
    FONT_SIZE = 32# font size for words
    SCORE_SIZE = 32# font size for score
    
    GAME_TIME = 60# number of seconds to complete the game

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,162,232)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mouse.set_visible(0)

        self.sound_right = pygame.mixer.Sound('audio\\right.ogg')
        self.sound_wrong = pygame.mixer.Sound('audio\\wrong.ogg')
        self.sound_miss = pygame.mixer.Sound('audio\\ricochet.ogg')
        self.image_shot = pygame.image.load('images\\bang.png')

##        self.object_lower = (89, 230, 230)# HSV color range for object to be tracked
##        self.object_upper = (108, 255, 255)
        self.object_lower = (94, 126, 129)# HSV color range for object to be tracked
        self.object_upper = (131, 255, 255)

        self.Words = []

        self.finished = False
        self.score = 0

        self.game_display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pistolero Test Game')
        self.display_width, self.display_height = pygame.display.get_surface().get_size()

        self.left_border = (self.display_height/self.display_width) * 0.02 * self.display_width
        self.right_border = (self.display_width -
                        (self.display_height/self.display_width) * 0.02 * self.display_width)
        self.top_border = 0.02 * self.display_height
        self.bottom_border = 0.98 * self.display_height
        self.center_width = self.display_width/2
        self.center_height = self.display_height/2
        self.circle_radius = 40
        self.tracking_rect = pygame.Rect(self.center_width-self.circle_radius, self.center_height-self.circle_radius, 2*self.circle_radius, 2*self.circle_radius)

        for x in range(10):
            self.Words.append(self.Word())
        
        self.game_display.fill(PistolGame.WHITE)
        pygame.display.update()

    class Word:
        def __init__(self):
            self.font = pygame.font.Font(None, 48)
            self.words_dict = {'father':'padre','mother':'madre','brother':'hermano','sister':'hermana',
            'husband':'esposo'}
            self.word = random.choice(list(self.words_dict.keys()))
            self.rendered_word = self.font.render(self.word, 1, (255,100,0))
            self.rect = self.rendered_word.get_rect()
            self.x = random.randint(100,800)
            self.y = random.randint(100,600)
            self.speedx = 10*(random.random()+0.01)
            self.speedy = 10*(random.random()+0.01)
            self.shrink_level = 1

        def shrink(self):
            if self.shrink_level == 1:
                self.font = pygame.font.Font(None, 32)
                self.rendered_word = self.font.render(self.word, 1, (255,255,000))
                self.shrink_level = 2
                self.speedx+=10
                self.speedy+=10
            elif self.shrink_level == 2:
                self.font = pygame.font.Font(None, 24)
                self.rendered_word = self.font.render(self.word, 1, (255,0,0))
                self.shrink_level = 3
            else:
                del(pg.Words[pg.Words.index(self)])
                #pg.Words.remove(Word)

    def WordCollide(self,C1,C2):
        C1Speed = math.sqrt((C1.speedx**2)+(C1.speedy**2))
        XDiff = -(C1.x-C2.x)
        YDiff = -(C1.y-C2.y)
        if XDiff > 0:
            if YDiff > 0:
                Angle = math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -C1Speed*math.cos(math.radians(Angle))
                YSpeed = -C1Speed*math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -C1Speed*math.cos(math.radians(Angle))
                YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif XDiff < 0:
            if YDiff > 0:
                Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -C1Speed*math.cos(math.radians(Angle))
                YSpeed = -C1Speed*math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -C1Speed*math.cos(math.radians(Angle))
                YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif XDiff == 0:
            if YDiff > 0:
                Angle = -90
            else:
                Angle = 90
            XSpeed = C1Speed*math.cos(math.radians(Angle))
            YSpeed = C1Speed*math.sin(math.radians(Angle))
        elif YDiff == 0:
            if XDiff < 0:
                Angle = 0
            else:
                Angle = 180
            XSpeed = C1Speed*math.cos(math.radians(Angle))
            YSpeed = C1Speed*math.sin(math.radians(Angle))
        C1.speedx = XSpeed
        C1.speedy = YSpeed
        
    def Move(self):
        for Word in self.Words:
            Word.x += Word.speedx
            Word.y += Word.speedy
            
    def CollisionDetect(self):
        for Word in self.Words:
            if ((Word.x < self.left_border + Word.rect.width / 2) or
                (Word.x > self.right_border - Word.rect.width / 2)):
                Word.speedx *= -1            
            if (Word.y < self.top_border + Word.rect.height / 2 or
                Word.y > self.bottom_border - Word.rect.height / 2):
                Word.speedy *= -1
            if Word.rect.colliderect(self.tracking_rect):
                if abs(self.tracking_rect.top - Word.rect.bottom) < 10 and Word.speedy > 0:
                    Word.speedy *= -1
                if abs(self.tracking_rect.bottom - Word.rect.top) < 10 and Word.speedy < 0:
                    Word.speedy *= -1
                if abs(self.tracking_rect.right - Word.rect.left) < 10 and Word.speedx < 0:
                    Word.speedx *= -1
                if abs(self.tracking_rect.left - Word.rect.right) < 10 and Word.speedx > 0:
                    Word.speedx *= -1
        
        for Word in self.Words:
            for Word2 in self.Words:
                if Word != Word2:
                    if ((Word.rect.x + Word.rect.width >= Word2.rect.x) and
                        (Word.rect.x <= Word2.rect.x + Word2.rect.w) and
                        (Word.rect.y + Word.rect.height >= Word2.rect.y) and
                        (Word.rect.y <= Word2.rect.y + Word2.rect.height)):
                        pg.WordCollide(Word,Word2)
        
    def end_game(self):
        self.game_display.fill(PistolGame.WHITE)
        self.message_display("GAME OVER", (self.display_width/2, self.display_height/2), 1, 0)
        self.message_display("SCORE: {0}".format(str(self.score)), (self.display_width/2, self.display_height/3), 1, 0)
        pygame.display.update()
        pygame.time.delay(3000)
        self.finished = True
        self.camera.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()

    def run(self):
        self.camera = cv2.VideoCapture(0)# change 1 to 0 if you only have one camera
        
        self.score = 0
        int_x, int_y = 0, 0
        start_ticks = pygame.time.get_ticks()
        
        while not self.finished:
            seconds = (pygame.time.get_ticks() - start_ticks)/1000
            if PistolGame.GAME_TIME - seconds == 0:
                self.end_game()
            
            (grabbed, frame) = self.camera.read()

            frame = imutils.resize(frame, width=self.display_width)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, self.object_lower, self.object_upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                int_x, int_y = self.display_width - int(x), self.display_height - int(y)
                # if radius > 10:# left here for troubleshooting purposes
                    # cv2.circle(frame, (int_x, int_y), int(radius), (0, 255, 255), 2)
            # cv2.imshow("Frame", frame)
            
            self.game_display.fill(PistolGame.WHITE)

            pygame.draw.circle(self.game_display, PistolGame.BLUE, (int(self.display_width/2), int(self.display_height/2)), self.circle_radius)# change tracking circle radius as necessary
            pg.Move()
            pg.CollisionDetect()
            for Word in self.Words:
                Word.rect.center = (Word.x, Word.y)
                self.game_display.blit(Word.rendered_word, Word.rect)
            #if rect0.collidepoint(int_x, int_y) or rect1.collidepoint(int_x, int_y) or rect2.collidepoint(int_x, int_y) or rect3.collidepoint(int_x, int_y):
            pygame.draw.circle(self.game_display, PistolGame.RED,(int_x, int_y), 10)
            #else:
            #    pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    for Word in self.Words:
                        if Word.rect.collidepoint(int_x, int_y):
                            if Word.words_dict[Word.word] == 'padre':
                                self.sound_right.play()
                                self.Words.remove(Word)
                            else:
                                self.sound_wrong.play()
                                Word.shrink()
                                #self.Words.remove(Word)
                            
##                    # update to use dictionary here?
##                    if (rect0.collidepoint(int_x, int_y) and self.professions_list[0] == self.selected_profession):
##                        self.sound_shot.play()
##                        self.score+=1
##                        #self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
##                        pygame.display.update()
##                        pygame.time.delay(300)
##                    else:
##                        self.sound_miss.play()

                    #self.new_round()

            pygame.display.update()

        self.camera.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()

        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
