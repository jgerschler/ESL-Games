# for python 3
# You'll need to customize this according to your needs. Proper orientation of
# the kinect is vital; if participants are able to maintain their head or wrists
# continuously inside the word rects, they will repeatedly trigger the collision
# detection
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import pygame
import random
import sys

TRACKING_COLOR = pygame.color.Color("purple")
HIGHLIGHT_COLOR = pygame.color.Color("red")
BG_COLOR = pygame.color.Color("white")
GAME_TIME = 60# seconds

class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.beep_sound = pygame.mixer.Sound('audio\\beep.ogg')
        self.buzz_sound = pygame.mixer.Sound('audio\\buzz.ogg')
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)

        pygame.display.set_caption("Adjective Adverb Game")

        self.finished = False
        self._clock = pygame.time.Clock()
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                                       PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width,
                                              self._kinect.color_frame_desc.Height), 0, 32)
        self._bodies = None

        self.score = 0

        self.vocab_dict = {"She liked the _____ cat.":("happy", "happily", "happy"),
                      "He _____ ate his food.":("quick", "quickly", "quickly"),
                      "That is a _____ puppy!":("cute", "cutely", "cute"),
                      "The pozole smells _____.":("tasty", "tastily", "tasty"),
                      "The dead fish looks _____.":("gross", "grossly", "gross"),
                      "He speaks _____.":("slow", "slowly", "slowly"),
                      "The girl moves _____.":("quick", "quickly", "quickly"),
                      "I feel _____.":("angry", "angrily", "angry"),
                      "The woman looked _____ at the paint stains.":("angry", "angrily", "angrily"),
                      "Rosario feels _____ about the news.":("bad", "badly", "bad"),
                      "Your nose is very senstive. You smell _____.":("good", "well", "well"),
                      "Nice perfume! You smell _____.":("good", "well", "good"),
                      "Concha seems _____. She broke up with her boyfriend.":("sad", "sadly", "sad"),
                      "Elvia was nervous and spoke very _____.":("quick", "quickly", "quickly"),
                      "Monse _____ swallowed the taco.":("rapid", "rapidly", "rapidly"),
                      "Chivis _____ watched the new movie.":("excited", "excitedly", "excitedly"),
                      "Tizoc _____ cut in line at the cafeteria.":("rude", "rudely", "rudely"),
                      "We did a _____ job on our homework.":("good", "well", "good"),
                      "Roberto feels _____.":("bad", "badly", "bad"),
                      "This old sushi tastes _____.":("disgusting", "disgustingly", "disgusting"),
                      "The gross man _____ spit on the floor.":("disgusting", "disgustingly", "disgustingly"),
                      "Salma Hayek is a _____ actress.":("beautiful", "beautifully", "beautiful"),
                      "Eugenio Derbez acts _____.":("beautiful", "beautifully", "beautifully"),
                      "She is a _____ runner!":("slow", "slowly", "slow"),
                      "She drinks _____.":("thirsty", "thirstily", "thirstily"),
                      "Oliver _____ ate the burrito.":("hungry", "hungrily", "hungrily"),
                      "Five fish swam _____.":("quick", "quickly", "quickly"),
                      "The black crow squawks _____.":("loud", "loudly", "loudly"),
                      "Race cars drive _____.":("careful", "carefully", "carefully"),
                      "Jennifer _____ read her book.":("quiet", "quietly", "quietly"),
                      "Luis is a _____ person.":("quiet", "quietly", "quiet"),
                      "He is a _____ driver.":("safe", "safely", "safe"),
                      "Your brother is so _____.":("kind", "kindly", "kind"),
                      "I always work _____ during the week.":("hard", "hardly", "hard"),
                      "Paco did _____ on his test.":("bad", "badly", "badly"),
                      "It is natural to feel _____ before a job interview.":("nervous", "nervously", "nervous")}

        self._frame_surface.fill((255, 255, 255))

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()

    def message_display(self, text, loc_tuple, loc_int):
        # loc_int: 1 center, 2 top left, 3 bottom left, 4 bottom right, 5 top right
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, 64))
        loc_dict = {1:'text_rect.center', 2:'text_rect.topleft', 3:'text_rect.bottomleft',
                    4:'text_rect.bottomright', 5:'text_rect.topright'}
        exec(loc_dict[loc_int] + ' = loc_tuple')
        self._frame_surface.blit(text_surf, text_rect)
        return text_rect 

    def draw_ind_point(self, joints, jointPoints, color, highlight_color, rect0, rect1, rect2, joint0, selected_sentence):
        joint0State = joints[joint0].TrackingState;
        
        if (joint0State == PyKinectV2.TrackingState_NotTracked or
            joint0State == PyKinectV2.TrackingState_Inferred):
            return

        center = (int(jointPoints[joint0].x), int(jointPoints[joint0].y))

        if ((rect0.collidepoint(center) and self.vocab_dict[selected_sentence][0] == self.vocab_dict[selected_sentence][2]) or
            (rect2.collidepoint(center) and self.vocab_dict[selected_sentence][1] == self.vocab_dict[selected_sentence][2])):
            self.score += 1
            self.beep_sound.play()
            pygame.time.delay(500)
            self.new_round()
        elif rect0.collidepoint(center) or rect1.collidepoint(center) or rect2.collidepoint(center):
            try:
                pygame.draw.circle(self._frame_surface, highlight_color, center, 20, 0)
                self.buzz_sound.play()               
            except: # need to catch it due to possible invalid positions (with inf)
                pass
        else:
            try:
                pygame.draw.circle(self._frame_surface, color, center, 20, 0)
            except:
                pass

    def update_screen(self, joints, jointPoints, color, highlight_color, selected_sentence, seconds):
        self._frame_surface.fill(BG_COLOR)# blank screen before drawing points
        # not optimum placement -- fix later
        screen_width = self._frame_surface.get_width()
        screen_height = self._frame_surface.get_height()
        rect0 = self.message_display(self.vocab_dict[selected_sentence][0], (screen_width / 3, screen_height / 3), 1)
        rect1 = self.message_display(selected_sentence, (screen_width / 2, 50), 1)
        rect2 = self.message_display(self.vocab_dict[selected_sentence][1], (screen_width - 300, screen_height / 3), 1)
        self.message_display(str(self.score), (screen_width / 2, screen_height - 100), 1)
        self.message_display(str(seconds), (screen_width - 300, screen_height - 100), 1)

        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_Head, selected_sentence)
        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_WristRight, selected_sentence)
        # may change PyKinectV2.JointType_WristRight to PyKinectV2.JointType_ElbowRight
        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_WristLeft, selected_sentence)

    def end_game(self):
        self._frame_surface.fill(BG_COLOR)
        self.message_display("Score: {}".format(self.score), (self._frame_surface.get_width() / 2, self._frame_surface.get_height() / 2), 1)
        self._screen.blit(self._frame_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(3000)
        self.run()

    def new_round(self):
        selected_sentence = random.choice(list(self.vocab_dict.keys()))
        pygame.time.delay(500)
        
        while not self.finished:
            seconds = GAME_TIME - int((pygame.time.get_ticks() - self.start_ticks)/1000)
            if seconds <= 0:
                self.end_game()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()              
                             
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            if self._bodies is not None:
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.update_screen(joints, joint_points, TRACKING_COLOR, HIGHLIGHT_COLOR, selected_sentence, seconds)

            self._screen.blit(self._frame_surface, (0,0))
            pygame.display.update()

            self._clock.tick(60)
            
        self.end_game()

    def run(self):
        self.score = 0
        while not self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.start_ticks = pygame.time.get_ticks()
                    self.new_round()

        self._kinect.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BodyGameRuntime()
    game.run()
