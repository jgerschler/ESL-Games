#!/usr/bin/env python
from collections import deque
from pygame.locals import *
import numpy as np
import argparse, imutils, cv2, pygame, random, sys

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
        self.sound_wrong_shot = pygame.mixer.Sound('audio\\nelsonlaugh.ogg')
        self.sound_miss = pygame.mixer.Sound('audio\\ricochet.ogg')
        self.image_shot = pygame.image.load('images\\bang.png')

##        self.object_lower = (89, 230, 230)# HSV color range for object to be tracked
##        self.object_upper = (108, 255, 255)
        self.object_lower = (94, 126, 129)# HSV color range for object to be tracked
        self.object_upper = (131, 255, 255)
        
        self.translations = {'electrician':'electricista','gardener':'jardinero','mechanic':'mecanico','bus driver':'chofer de autobus',
				'hairdresser':'estilista','construction worker':'obrero','mason':'albañil','pump attendant':'despachador',
				'garbage man':'recogedor de basura','mailman':'cartero','architect':'arquitecto','cook':'cocinero',
				'photographer':'fotografo','butcher':'carnicero','waiter':'mesero','waitress':'mesera','dentist':'dentista',
				'baker':'panadero','cleaning lady':'limpiadora','salesman':'vendedor','actress':'actriz','artist':'artista',
				'doctor':'doctor','engineer':'ingeniero','fireman':'bombero','housewife':'ama de casa','nurse':'enfermera',
				'pilot':'piloto','policeman':'policia','cashier':'cajera','painter':'pintor','secretary':'secretaria',
				'singer':'cantante','veterinarian':'veterinario','soldier':'soldado','carpenter':'carpintero',
				'businessman':'hombre de negocios','detective':'detective','plumber':'plomero','surgeon':'cirujano',
				'writer':'escritor','farmer':'campesino','spy':'espia','lawyer':'abogado','judge':'juez','journalist':'periodista',
				'teacher':'maestro','delivery boy':'repartidor'}
                
		self.professions = ['electrician', 'gardener', 'mechanic', 'bus driver', 'hairdresser', 'construction worker', 'mason', 
                'pump attendant', 'garbage man', 'mailman', 'architect', 'cook', 'photographer', 'butcher', 'waiter', 
                'waitress', 'dentist', 'baker',	'cleaning lady', 'salesman', 'actress', 'artist', 'doctor', 'engineer', 
				'fireman', 'housewife', 'nurse', 'pilot', 'policeman', 'cashier', 'painter', 'secretary', 'singer',
                'veterinarian', 'soldier', 'carpenter', 'businessman', 'detective', 'plumber', 'surgeon', 'writer',
                'farmer', 'spy', 'lawyer', 'judge', 'journalist', 'teacher', 'delivery boy']

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
    def message_display_center(self, text, tuple_center):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', PistolGame.SCORE_SIZE))
        text_rect.center = tuple_center
        self.game_display.blit(text_surf, text_rect)
        return text_rect        

    def message_display_topleft(self, text, tuple_topleft):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', PistolGame.FONT_SIZE))
        text_rect.topleft = tuple_topleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
       
    def message_display_bottomleft(self, text, tuple_bottomleft):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', PistolGame.FONT_SIZE))
        text_rect.bottomleft = tuple_bottomleft
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_topright(self, text, tuple_topright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', PistolGame.FONT_SIZE))
        text_rect.topright = tuple_topright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def message_display_bottomright(self, text, tuple_bottomright):
        text_surf, text_rect = self.text_objects(text, pygame.font.Font('arial.ttf', PistolGame.FONT_SIZE))
        text_rect.bottomright = tuple_bottomright
        self.game_display.blit(text_surf, text_rect)
        return text_rect
        
    def new_round(self):
        self.selected_verb_list = self.professions[random.randint(0, len(self.professions)-1)]
        random.shuffle(self.selected_verb_list[1])
        
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
        self.camera = cv2.VideoCapture(0)
        
        self.selected_verb_list = self.professions[random.randint(0, len(self.professions)-1)]
        random.shuffle(self.selected_verb_list[1])

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
            rect0 = self.message_display_topleft(self.selected_verb_list[1][0][0], (100, 100))
            rect1 = self.message_display_bottomleft(self.selected_verb_list[1][1][0], (100, self.display_height - 100))
            rect2 = self.message_display_topright(self.selected_verb_list[1][2][0], (self.display_width - 100, 100))
            rect3 = self.message_display_bottomright(self.selected_verb_list[1][3][0], (self.display_width - 100, self.display_height - 100))
            react_score = self.message_display_center("{0} {1}".format(str(self.score), PistolGame.GAME_TIME - seconds), (self.display_width/2, self.display_height - 50))
            base_verb = self.message_display_center(self.selected_verb_list[0], (self.display_width/2, 50))
            pygame.draw.circle(self.game_display, PistolGame.BLUE, (self.display_width/2, self.display_height/2), 40)# change tracking circle radius as necessary
            if rect0.collidepoint(int_x, int_y) or rect1.collidepoint(int_x, int_y) or rect2.collidepoint(int_x, int_y) or rect3.collidepoint(int_x, int_y):
                pygame.draw.circle(self.game_display, PistolGame.RED,(int_x, int_y), 10)
            else:
                pygame.draw.circle(self.game_display, PistolGame.BLACK,(int_x, int_y), 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    # update to use dictionary here?
                    if (rect0.collidepoint(int_x, int_y) and self.selected_verb_list[1][0][1] == "a"):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect1.collidepoint(int_x, int_y) and self.selected_verb_list[1][1][1] == "a"):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect2.collidepoint(int_x, int_y) and self.selected_verb_list[1][2][1] == "a"):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect3.collidepoint(int_x, int_y) and self.selected_verb_list[1][3][1] == "a"):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect0.collidepoint(int_x, int_y) and self.selected_verb_list[1][0][1] == "q"):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect1.collidepoint(int_x, int_y) and self.selected_verb_list[1][1][1] == "q"):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect2.collidepoint(int_x, int_y) and self.selected_verb_list[1][2][1] == "q"):
                        self.sound_wrong_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect3.collidepoint(int_x, int_y) and self.selected_verb_list[1][3][1] == "q"):
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
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
