from collections import deque
from pygame.locals import *
import numpy as np
import argparse, imutils, cv2, pygame, time, random

class PistolGame(object):
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.sound_shot = pygame.mixer.Sound('audio\\shot.ogg')
        self.image_shot = pygame.image.load('images\\bang.png')

        self.object_lower = (0, 112, 208)# HSV color range for object to be tracked
        self.object_upper = (19, 255, 255)

        self.verbs = ['eat','walk','talk','run','speak','read','be','watch','see','hear','listen','allow','permit']
        self.adjectives = ['red','green','blue','furry','hairy','happy']

        self.finished = False

        self.game_display = pygame.display.set_mode((PistolGame.DISPLAY_WIDTH, PistolGame.DISPLAY_HEIGHT))
        pygame.display.set_caption('Pistolero Game')
        self.game_display.fill(PistolGame.WHITE)
        pygame.display.update()

    def text_objects(self, text, font):
        text_surface = font.render(text, True, PistolGame.BLACK)
        return text_surface, text_surface.get_rect()

    def message_display_left(self, text, tuple_topleft):# subdivide these into topleft, topright...etc
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', 32))
        text_rect.topleft = tuple_topleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_right(self, text, tuple_topright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', 32))
        text_rect.topright = tuple_topright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def new_round(self):
        self.word_list = random.sample(self.verbs, 3)
        self.word_list.append(random.sample(self.adjectives, 1)[0])
        random.shuffle(self.word_list)

    def run(self):
        camera = cv2.VideoCapture(0)
        
        self.word_list = random.sample(self.verbs, 3)
        self.word_list.append(random.sample(self.adjectives, 1)[0])
        random.shuffle(self.word_list)
        
        while not self.finished:
            (grabbed, frame) = camera.read()

            frame = imutils.resize(frame, width=800)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, self.object_lower, self.object_upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                int_x, int_y = int(x), int(y)
                if radius > 10:
                    cv2.circle(frame, (int_x, int_y), int(radius), (0, 255, 255), 2)
            cv2.imshow("Frame", frame)
            
            try:
                self.game_display.fill(PistolGame.WHITE)
                rect1 = self.message_display_left(self.word_list[0], (50, 50))
                rect2 = self.message_display_left(self.word_list[1], (50, PistolGame.DISPLAY_HEIGHT - 50))
                rect3 = self.message_display_right(self.word_list[2], (PistolGame.DISPLAY_WIDTH - 50, 50))
                rect4 = self.message_display_right(self.word_list[3], (PistolGame.DISPLAY_WIDTH - 50, PistolGame.DISPLAY_HEIGHT - 50))
                if rect1.collidepoint(int_x, int_y):
                    pygame.draw.circle(self.game_display, PistolGame.RED,(int_x, int_y), 10)
                else:
                    pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), 10)
                
            except:
                pass# temporary! add error handling!

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.MOUSEBUTTONUP:# event.type == pygame.KEYUP, event.key == pygame.K_a
                    #if int_x int_y
                    self.sound_shot.play()# check to see if you are inside rect, and if it is the correct rect!
                    self.game_display.blit(self.image_shot, (280, 210))#update scoring
                    pygame.display.update()
                    time.sleep(0.5)# change to use pygame
                    self.new_round()


            pygame.display.update()

        camera.release()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
