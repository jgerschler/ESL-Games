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

    def message_display_left(self, text, tuple_topleft):
        large_text = pygame.font.Font('arial.ttf',18)
        text_surf, text_rect = self.text_objects(text, large_text)
        text_rect.topleft = tuple_topleft
        self.game_display.blit(text_surf, text_rect)
        
    def message_display_right(self, text, tuple_topright):
        large_text = pygame.font.Font('arial.ttf',18)
        text_surf, text_rect = self.text_objects(text, large_text)
        text_rect.topright = tuple_topright
        self.game_display.blit(text_surf, text_rect)
        
    def new_round(self):
        word_list = random.sample(self.verbs, 3)
        word_list.append(random.sample(self.adjectives, 1))
        word_list.shuffle()
        
        self.game_display.fill(PistolGame.WHITE)
        
        self.message_display_left(wordlist[0], (50, 50))
        self.message_display_left(wordlist[1], (50, PistolGame.DISPLAY_HEIGHT - 50))
        self.message_display_right(wordlist[2], (PistolGame.DISPLAY_WIDTH - 50, 50))
        self.message_display_right(wordlist[3], (PistolGame.DISPLAY_WIDTH - 50, PistolGame.DISPLAY_HEIGHT - 50))
        
        pygame.display.update()

    def run(self):
        camera = cv2.VideoCapture(0)
        
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.MOUSEBUTTONUP:# event.type == pygame.KEYUP, event.key == pygame.K_a
                    if 280 <= int_x <= 320 and 210 <= int_y <= 240:
                        self.sound_shot.play()
                        self.game_display.blit(self.image_shot, (280, 210))
                        pygame.display.update()
                        time.sleep(0.5)
                        self.new_round()
                        #if inside of correct box remove text and blow up
                    #elif #if inside wrong box
                    else:
                        self.sound_shot.play()
            self.game_display.fill(PistolGame.WHITE)
            pygame.draw.rect(self.game_display, PistolGame.BLACK, (280, 210, 40, 30), 2)
            self.message_display_left("cars", (50, 50))
            try:
                if 280 <= int_x <= 320 and 210 <= int_y <= 240:
                    pygame.draw.circle(self.game_display, PistolGame.RED,(int_x, int_y), 10)
                else:
                    pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), 10)
            except:
                pass
            pygame.display.update()

        camera.release()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
