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

    TARGET_CIRCLE_RADIUS = 10
    
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
        
        self.translations = {'father':'padre','mother':'madre','brother':'hermano','sister':'hermana',
                'husband':'esposo','wife':'esposa','son':'hijo','daughter':'hija',
                'great grandmother':'bisabuela','great grandfather':'bisabuelo','father-in-law':'suegro','grandfather':'abuelo',
                'mother-in-law':'suegra','grandmother':'abuela','uncle':'tio','aunt':'tia','cousin':'primo',
                'nephew':'sobrino','niece':'sobrina','brother-in-law':'cuñado','sister-in-law':'cuñada','stepfather':'padrastro',
                'stepmother':'madrastra','stepbrother':'hermanastro','stepsister':'hermanastra','half brother':'medio hermano','half sister':'media hermana'}
                
        self.professions = ['father','mother','brother','sister',
                'husband','wife','son','daughter',
                'great grandmother','great grandfather','father-in-law','grandfather',
                'mother-in-law','grandmother','uncle','aunt','cousin',
                'nephew','niece','brother-in-law','sister-in-law','stepfather',
                'stepmother','stepbrother','stepsister','half brother','half sister']

        self.finished = False

        self.game_display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pistolero Professions Game')
        self.display_width, self.display_height = pygame.display.get_surface().get_size()
        self.game_display.fill(PistolGame.WHITE)
        pygame.display.update()

    def text_objects(self, text, font):
        text_surface = font.render(text, True, PistolGame.BLACK)
        return text_surface, text_surface.get_rect()
        
    # these message display functions need to be combined!

    def message_display(self, text, loc_tuple, loc_int, score_flag):# loc_int: 1 center, 2 top left, 3 bottom left, 4 bottom right, 5 top right. score_flag; 0 default font size, 1 score font size
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.FONT_SIZE))# improve this section
        if score_flag == 1:
            text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, PistolGame.SCORE_SIZE))
        loc_dict = {1:'text_rect.center', 2:'text_rect.topleft', 3:'text_rect.bottomleft', 4:'text_rect.bottomright', 5:'text_rect.topright'}
        exec(loc_dict[loc_int] + ' = loc_tuple')
        self.game_display.blit(text_surf, text_rect)
        return text_rect   
        
    def new_round(self):
        self.selected_profession = random.choice(list(self.translations.keys()))
        self.professions_list = random.sample(self.professions, 3)
        while self.selected_profession in self.professions_list:
            self.professions_list = random.sample(self.professions, 3)
        self.professions_list.append(self.selected_profession)
        random.shuffle(self.professions_list)
        
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
        self.camera = cv2.VideoCapture(1)# change 1 to 0 if you only have one camera
        
        self.selected_profession = random.choice(list(self.translations.keys()))
        self.professions_list = random.sample(self.professions, 3)
        while self.selected_profession in self.professions_list:
            self.professions_list = random.sample(self.professions, 3)
        self.professions_list.append(self.selected_profession)
        random.shuffle(self.professions_list)
        
        self.score = 0
        int_x, int_y = 0, 0
        rect0_edge_x, rect0_edge_y = 0, 0
        rect1_edge_x, rect1_edge_y = 0, 0
        rect2_edge_x, rect2_edge_y = 0, 0
        rect3_edge_x, rect3_edge_y = 0, 0
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
            rect0 = self.message_display(self.professions_list[0], (100, 100), 2, 0)
            rect1 = self.message_display(self.professions_list[1], (100, self.display_height - 100), 3, 0)
            rect2 = self.message_display(self.professions_list[2], (self.display_width - 100, 100), 5, 0)
            rect3 = self.message_display(self.professions_list[3], (self.display_width - 100, self.display_height - 100), 4, 0)
            react_score = self.message_display("{0} {1}".format(str(self.score), int(PistolGame.GAME_TIME - seconds)),
                                               (int(self.display_width/2), int(self.display_height - 50)), 1, 1)
            base_verb = self.message_display(self.translations[self.selected_profession], (self.display_width/2, 50), 1, 1)
            pygame.draw.circle(self.game_display, PistolGame.BLUE, (int(self.display_width/2), int(self.display_height/2)), 40)# change tracking circle radius as necessary
            pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), PistolGame.TARGET_CIRCLE_RADIUS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    # update to use dictionary here?
                    # rect0
                    if int_x < rect0.left:
                        rect0_edge_x = rect0.left
                    elif int_x > rect0.right:
                        rect0_edge_x = rect0.right
                    if int_y > rect0.top:
                        rect0_edge_y = rect0.top
                    elif int_y < rect0.bottom:
                        rect0_edge_y = rect0.bottom
                    dist_x_r0 = int_x - rect0_edge_x
                    dist_y_r0 = int_y - rect0_edge_y
                    distance_r0 = math.sqrt((dist_x_r0 * dist_x_r0) + (dist_y_r0 * dist_y_r0))
                    # rect1
                    if int_x < rect1.left:
                        rect1_edge_x = rect1.left
                    elif int_x > rect1.right:
                        rect1_edge_x = rect1.right
                    if int_y > rect1.top:
                        rect1_edge_y = rect1.top
                    elif int_y < rect1.bottom:
                        rect1_edge_y = rect1.bottom
                    dist_x_r1 = int_x - rect1_edge_x
                    dist_y_r1 = int_y - rect1_edge_y
                    distance_r1 = math.sqrt((dist_x_r1 * dist_x_r1) + (dist_y_r1 * dist_y_r1))
                    # rect2
                    if int_x < rect2.left:
                        rect2_edge_x = rect2.left
                    elif int_x > rect2.right:
                        rect2_edge_x = rect2.right
                    if int_y > rect2.top:
                        rect2_edge_y = rect2.top
                    elif int_y < rect2.bottom:
                        rect2_edge_y = rect2.bottom
                    dist_x_r2 = int_x - rect2_edge_x
                    dist_y_r2 = int_y - rect2_edge_y
                    distance_r2 = math.sqrt((dist_x_r2 * dist_x_r2) + (dist_y_r2 * dist_y_r2))
                    # rect3
                    if int_x < rect3.left:
                        rect3_edge_x = rect3.left
                    elif int_x > rect3.right:
                        rect3_edge_x = rect3.right
                    if int_y > rect3.top:
                        rect3_edge_y = rect3.top
                    elif int_y < rect3.bottom:
                        rect3_edge_y = rect3.bottom
                    dist_x_r3 = int_x - rect3_edge_x
                    dist_y_r3 = int_y - rect3_edge_y
                    distance_r3 = math.sqrt((dist_x_r3 * dist_x_r3) + (dist_y_r3 * dist_y_r3))
                    print("dr0:{0},dx0:{1},dy0:{2}".format(distance_r0, dist_x_r0, dist_y_r0))
                    # scoring logic
                    if ((distance_r0 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[0] == self.selected_profession):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r1 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[1] == self.selected_profession):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r2 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[2] == self.selected_profession):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r3 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[3] == self.selected_profession):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r0 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[0] != self.selected_profession):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r1 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[1] != self.selected_profession):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r2 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[2] != self.selected_profession):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif ((distance_r3 < PistolGame.TARGET_CIRCLE_RADIUS) and self.professions_list[3] != self.selected_profession):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    else:
                        self.sound_miss.play()

                    self.new_round()

            pygame.display.update()

        self.camera.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
