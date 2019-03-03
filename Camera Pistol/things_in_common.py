#!/usr/bin/env python
from pygame.locals import *
import imutils
import cv2
import pygame
import random
import sys

class PistolGame(object):
    FONT_SIZE = 64# font size for words
    SCORE_SIZE = 32# font size for score
    
    GAME_TIME = 60# number of seconds to complete the game

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,162,232)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.sound_shot = pygame.mixer.Sound('audio\\shot.ogg')
        self.sound_wrong_shot = pygame.mixer.Sound('audio\\scream.ogg')
        self.sound_miss = pygame.mixer.Sound('audio\\ricochet.ogg')
        self.image_shot = pygame.image.load('images\\bang.png')

##        self.object_lower = (89, 230, 230)# HSV color range for object to be tracked
##        self.object_upper = (108, 255, 255)
        self.object_lower = (94, 126, 129)# HSV color range for object to be tracked
        self.object_upper = (131, 255, 255)
        
        self.sentence_dict = {"""I don't like fish.""":["""I don't either.""", """Me neither."""],
                         """I don't know how to swim.""":["""I don't either.""", """Me neither."""],
                         """I don't like potatoes.""":["""I don't either.""", """Me neither."""],
                         """I don't eat donuts at night.""":["""I don't either.""", """Me neither."""],
                         """I don't watch scary movies.""":["""I don't either.""", """Me neither."""],
                         """I don't yell when I get angry.""":["""I don't either.""", """Me neither."""],
                         """I can't ride a bicycle.""":["""I can't either.""", """Me neither."""],
                         """I can't swim.""":["""I can't either.""", """Me neither."""],
                         """I can't drive a car.""":["""I can't either.""", """Me neither."""],
                         """I can't do a pushup.""":["""I can't either.""", """Me neither."""],
                         """I can't run faster than a bus.""":["""I can't either.""", """Me neither."""],
                         """I can't flap my arms and fly.""":["""I can't either.""", """Me neither."""],
                         """I'm not fat.""":["""I'm not either.""", """Me neither."""],
                         """I'm not skinny.""":["""I'm not either.""", """Me neither."""],
                         """I'm not an angry person.""":["""I'm not either.""", """Me neither."""],
                         """I'm not hungry.""":["""I'm not either.""", """Me neither."""],
                         """I'm not happy.""":["""I'm not either.""", """Me neither."""],
                         """I'm not a purple hippopotamus.""":["""I'm not either.""", """Me neither."""],
                         """I like papayas.""":["""I do too.""", """Me too."""],
                         """I know how to drive.""":["""I do too.""", """Me too."""],
                         """I know how to swim.""":["""I do too.""", """Me too."""],
                         """I like oranges.""":["""I do too.""", """Me too."""],
                         """I eat cake on Fridays.""":["""I do too.""", """Me too."""],
                         """I love comedies.""":["""I do too.""", """Me too."""],
                         """I can eat 12 hamburgers at once.""":["""I can too.""", """Me too."""],
                         """I can fly an airplane.""":["""I can too.""", """Me too."""],
                         """I can write quickly.""":["""I can too.""", """Me too."""],
                         """I can run faster than a snail.""":["""I can too.""", """Me too."""],
                         """I can calculate faster than a calculator.""":["""I can too.""", """Me too."""],
                         """I can swim with my eyes open.""":["""I can too.""", """Me too."""],
                         """I'm angry.""":["""I am too.""", """Me too."""],
                         """I'm hungry.""":["""I am too.""", """Me too."""],
                         """I'm sad.""":["""I am too.""", """Me too."""],
                         """I'm busy with work.""":["""I am too.""", """Me too."""],
                         """I'm studying right now.""":["""I am too.""", """Me too."""],
                         """I'm at school at the moment.""":["""I am too.""", """Me too."""]}

        self.reply_list = ["""I don't either.""", """Me neither.""", """I can't either.""",
                      """I'm not either.""", """I do too.""", """Me too.""", """I can too.""",
                      """I am too.""", """I do either.""", """I can either.""", """I am either.""",
                      """I do neither.""", """I can neither.""", """I am neither.""",
                      """I am not too.""", """I don't too.""", """I can't too."""]

        self.finished = False

        self.game_display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pistolero Simple Past Game')
        self.display_width, self.display_height = pygame.display.get_surface().get_size()
        self.game_display.fill(PistolGame.WHITE)
        pygame.display.update()

    def text_objects(self, text, font):
        text_surface = font.render(text, True, PistolGame.BLACK)
        return text_surface, text_surface.get_rect()
        
    def message_display_center(self, text, tuple_center):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.SCORE_SIZE))
        text_rect.center = tuple_center
        self.game_display.blit(text_surf, text_rect)
        return text_rect        

    def message_display_topleft(self, text, tuple_topleft):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.FONT_SIZE))
        text_rect.topleft = tuple_topleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
       
    def message_display_bottomleft(self, text, tuple_bottomleft):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.FONT_SIZE))
        text_rect.bottomleft = tuple_bottomleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_topright(self, text, tuple_topright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.FONT_SIZE))
        text_rect.topright = tuple_topright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_bottomright(self, text, tuple_bottomright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.FONT_SIZE))
        text_rect.bottomright = tuple_bottomright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def new_round(self):
        self.selected_sentence = random.choice(list(self.sentence_dict.keys()))
        self.selected_answer = random.sample(self.sentence_dict[self.selected_sentence], 1)
        self.filler_replies = random.sample(self.reply_list, 3)
        while ((self.sentence_dict[self.selected_sentence][0] in self.filler_replies) or
               (self.sentence_dict[self.selected_sentence][1] in self.filler_replies)):
            self.filler_replies = random.sample(self.reply_list, 3)
        self.filler_replies += self.selected_answer
        random.shuffle(self.filler_replies)
        
    def end_game(self):
        self.game_display.fill(PistolGame.WHITE)
        self.message_display_center("GAME OVER", (self.display_width/2, self.display_height/2))
        self.message_display_center("SCORE: {0}".format(str(self.score)), (self.display_width/2, self.display_height/3))
        pygame.display.update()
        pygame.time.delay(3000)
        self.finished = True
        self.camera.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()

    def run(self):
        self.camera = cv2.VideoCapture(0)# 0 if only one camera

        self.selected_sentence = random.choice(list(self.sentence_dict.keys()))
        self.selected_answer = random.sample(self.sentence_dict[self.selected_sentence], 1)
        self.filler_replies = random.sample(self.reply_list, 3)
        while ((self.sentence_dict[self.selected_sentence][0] in self.filler_replies) or
               (self.sentence_dict[self.selected_sentence][1] in self.filler_replies)):
            self.filler_replies = random.sample(self.reply_list, 3)
        self.filler_replies += self.selected_answer
        random.shuffle(self.filler_replies)
        
        self.score = 0
        int_x, int_y = 0, 0
        start_ticks = pygame.time.get_ticks()
        
        while not self.finished:
            seconds = (pygame.time.get_ticks() - start_ticks)/1000
            if PistolGame.GAME_TIME - seconds <= 0:
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
            rect0 = self.message_display_topleft(self.filler_replies[0], (100, 100))
            rect1 = self.message_display_bottomleft(self.filler_replies[1], (100, self.display_height - 100))
            rect2 = self.message_display_topright(self.filler_replies[2], (self.display_width - 100, 100))
            rect3 = self.message_display_bottomright(self.filler_replies[3], (self.display_width - 100, self.display_height - 100))
            react_score = self.message_display_center("{0} {1}".format(str(self.score), int(PistolGame.GAME_TIME - seconds)),
                                                      (int(self.display_width/2), int(self.display_height - 50)))
            base_verb = self.message_display_center(self.selected_sentence, (self.display_width/2, 50))
            pygame.draw.circle(self.game_display, PistolGame.BLUE, (int(self.display_width/2), int(self.display_height/2)), 40)# change tracking circle radius as necessary
            if rect0.collidepoint(int_x, int_y) or rect1.collidepoint(int_x, int_y) or rect2.collidepoint(int_x, int_y) or rect3.collidepoint(int_x, int_y):
                pygame.draw.circle(self.game_display, PistolGame.RED,(int_x, int_y), 10)
            else:
                pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    if (rect0.collidepoint(int_x, int_y) and self.filler_replies[0] == self.selected_answer[0]):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect1.collidepoint(int_x, int_y) and self.filler_replies[1] == self.selected_answer[0]):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect2.collidepoint(int_x, int_y) and self.filler_replies[2] == self.selected_answer[0]):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect3.collidepoint(int_x, int_y) and self.filler_replies[3] == self.selected_answer[0]):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect0.collidepoint(int_x, int_y)):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect1.collidepoint(int_x, int_y)):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect2.collidepoint(int_x, int_y)):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect3.collidepoint(int_x, int_y)):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    else:
                        self.sound_miss.play()

                    self.new_round()

            pygame.display.update()

        camera.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
