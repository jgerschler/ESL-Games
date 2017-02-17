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
    BLUE = (0,162,232)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.sound_shot = pygame.mixer.Sound('audio\\shot.ogg')
        self.image_shot = pygame.image.load('images\\bang.png')

        self.object_lower = (89, 230, 230)# HSV color range for object to be tracked
        self.object_upper = (108, 255, 255)

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

    def message_display_topleft(self, text, tuple_topleft):# subdivide these into topleft, topright...etc
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', 32))
        text_rect.topleft = tuple_topleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
       
    def message_display_bottomleft(self, text, tuple_bottomleft):# subdivide these into topleft, topright...etc
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', 32))
        text_rect.bottomleft = tuple_bottomleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_topright(self, text, tuple_topright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', 32))
        text_rect.topright = tuple_topright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_bottomright(self, text, tuple_bottomright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', 32))
        text_rect.bottomright = tuple_bottomright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def new_round(self):
        self.word_list = random.sample(self.verbs, 3)# update this with dictionary for more flexibility
        self.word_list.append(random.sample(self.adjectives, 1)[0])
        random.shuffle(self.word_list)

    def run(self):
        camera = cv2.VideoCapture(0)
        
        self.word_list = random.sample(self.verbs, 3)# update this with dictionary for more flexibility
        self.word_list.append(random.sample(self.adjectives, 1)[0])
        random.shuffle(self.word_list)

        int_x, int_y = 0, 0
        
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
                rect0 = self.message_display_topleft(self.word_list[0], (50, 50))
                rect1 = self.message_display_bottomleft(self.word_list[1], (50, PistolGame.DISPLAY_HEIGHT - 50))
                rect2 = self.message_display_topright(self.word_list[2], (PistolGame.DISPLAY_WIDTH - 50, 50))
                rect3 = self.message_display_bottomright(self.word_list[3], (PistolGame.DISPLAY_WIDTH - 50, PistolGame.DISPLAY_HEIGHT - 50))
                pygame.draw.circle(self.game_display, PistolGame.BLUE, (PistolGame.DISPLAY_WIDTH/2, PistolGame.DISPLAY_HEIGHT/2), 60)
                if rect0.collidepoint(int_x, int_y) or rect1.collidepoint(int_x, int_y) or rect2.collidepoint(int_x, int_y) or rect3.collidepoint(int_x, int_y):
                    pygame.draw.circle(self.game_display, PistolGame.RED,(int_x, int_y), 10)
                else:
                    pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), 10)
                
            except:
                pass# temporary! add error handling!

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.MOUSEBUTTONUP:# event.type == pygame.KEYUP, event.key == pygame.K_a
                    #update to use dictionary here
                    if ((rect0.collidepoint(int_x, int_y) and self.word_list[0] in self.adjectives) or (rect1.collidepoint(int_x, int_y) and self.word_list[1] in self.adjectives) or
                        (rect2.collidepoint(int_x, int_y) and self.word_list[2] in self.adjectives) or (rect3.collidepoint(int_x, int_y) and self.word_list[3] in self.adjectives)):
                        #winner -- show shot, add point and switch to next set
                        self.sound_shot.play()
                        self.game_display.blit(self.image_shot, (280, 210))#update scoring
                        pygame.display.update()
                        pygame.time.delay(300)
                        print("winner!")
                    elif rect0.collidepoint(int_x, int_y) or rect1.collidepoint(int_x, int_y) or rect2.collidepoint(int_x, int_y) or rect3.collidepoint(int_x, int_y):
                        #loser -- show shot, subtract point and switch to next set
                        self.sound_shot.play()
                        self.game_display.blit(self.image_shot, (280, 210))#update scoring
                        pygame.display.update()
                        pygame.time.delay(300)
                        print("loser")
                    else:
                        self.sound_shot.play()
                        
                        
                        
                    # self.game_display.blit(self.image_shot, (280, 210))#update scoring
                    # pygame.display.update()
                    # pygame.time.delay(300)
                    self.new_round()


            pygame.display.update()

        camera.release()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
