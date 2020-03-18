# for python 3
# You'll need to customize this according to your needs. Proper orientation of
# the kinect is vital; if participants are able to maintain their head or wrists
# continuously inside the word rects, they will repeatedly trigger the collision
# detection
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
from math import ceil

import pygame
import random
import sys

TRACKING_COLOR = pygame.color.Color("green")
HIGHLIGHT_COLOR = pygame.color.Color("red")
BG_COLOR = pygame.color.Color("white")
GAME_TIME = 60# seconds


class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.beep_sound = pygame.mixer.Sound('audio\\beep.ogg')
        self.buzz_sound = pygame.mixer.Sound('audio\\buzz.ogg')
        self.click_sound = pygame.mixer.Sound('audio\\click.ogg')
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)

        pygame.display.set_caption("Sentence Builder Game")

        self.finished = False
        self._clock = pygame.time.Clock()
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                                       PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width,
                                              self._kinect.color_frame_desc.Height), 0, 32)
        self._bodies = None

        self.score = 0

        self.sentence_list = [
            "It is not acceptable to eat with your mouth open",
            "It is acceptable to use a napkin",
            "You shouldn't talk with food in your mouth",
            "You shouldn't use bad words at the dinner table",
            "This is a test sentence for the game",
            "These sentences don't have any periods",
            "Giraffes are herbivores, and don't eat elephants",
            "Elvia came to visit the teacher in his office",
            "My favorite fruits are rambutans and chirimoyas",
            "The cat likes to eat the dog's food",
            "Sometimes the dog gets angry and barks at the cat",
            "The 19-year-old is not an exception.", 
            "She is like many other young women in Nuh, where she lives, in northern India.", 
            "Only about 30 percent of the women there can read and write.", 
            "That is about half the national average.", 
            "Wasima Khan left school because she had to do housework and help her mother with younger brothers and sisters, she said.", 
            "And there was no middle school in her community.", 
            "At the same time, boys living in Papika, in Haryana state, walk to the nearest high school, about four kilometers away.", 
            "Yet girls are not permitted to leave the small village.", 
            "In Papika, many of the women work in fields or care for farm animals.", 
            "Young girls get water, while children play.", 
            "Men often sit outside their homes in the sun after a cold winter.",
            "This saying comes to us from Benjamin Franklin.",
            "In addition to being a writer, Franklin was a printer, political thinker, politician, scientist, inventor and diplomat.",
            "He was also one of the Founding Fathers of the United States.",
            "So, he was a busy man.",
            "But Franklin still found time to write and offer his advice to others.",
            "If he were alive today, he could probably make a good living as a life coach.",
            "Now, Franklin lived during the 1700s, before the metric system took effect in Europe.",
            "The word ounce means something really small – just two-one-hundredths of a kilogram to be exact.",
            "So, his expression meant that, when dealing with a problem, spending a small amount of time and effort early on is a good investment.",
            "It can save you more trouble in the end.",
            "Education officials and industry experts are debating the future of online learning.",
            "The discussion is important because recently hundreds of universities in the United States have moved classes online because of the spread of the new coronavirus.",
            "Colleges and universities worldwide have been looking for ways to provide high quality education off campus and outside of normal business hours.",
            "The decision by many schools in the United States to suspend in-person classes during the recent coronavirus crisis has shown how important online teaching can be.",
            "And demand for such programs is increasing.",
            "Pearson Education is one of a growing number of companies that have partnered with schools to create online study aids and full degree programs.",
            "Classes meet online through video conferencing.",
            "In this way, students are able to communicate with each other and their professors even when they are far away from school.",
            "Online learning also permits older students, who work full-time and support families, to work on their education in their free time.",
            "It can be helpful for people who might have difficulty coming to a college campus, such as disabled students or those who live far from any college or university."
            ]

        self._frame_surface.fill((255, 255, 255))

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()

    def message_display(self, text, loc_tuple, loc_int):
        # loc_int: 1 center, 2 top left, 3 bottom left, 4 bottom right, 5 top right
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, 36))
        loc_dict = {1:'text_rect.center', 2:'text_rect.topleft', 3:'text_rect.bottomleft',
                    4:'text_rect.bottomright', 5:'text_rect.topright'}
        exec(loc_dict[loc_int] + ' = loc_tuple')
        self._frame_surface.blit(text_surf, text_rect)
        return text_rect 

    def fragment_sentence(self, sentence):
        sentence_list = sentence.split()
        sentence_word_count = len(sentence_list)
        max_frag_size = ceil(sentence_word_count/3)
        frag_list = []
        i = 0
        while i * max_frag_size <= sentence_word_count:
            frag_list.append(sentence_list[i*max_frag_size:(i + 1)*max_frag_size])
            i += 1 
        frag_list = [' '.join(words) for words in frag_list][0:3]
        return frag_list

    def draw_ind_point(self, joints, jointPoints, color, highlight_color,
                       rect0, rect1, rect2, joint0, frag_list):
        joint0State = joints[joint0].TrackingState;
        
        if (joint0State == PyKinectV2.TrackingState_NotTracked or
            joint0State == PyKinectV2.TrackingState_Inferred):
            return

        center = (int(jointPoints[joint0].x), int(jointPoints[joint0].y))

        if rect0.collidepoint(center):
            self.built_frag = self.built_frag + " " + frag_list[0]
            self.click_sound.play()
            frag_list[0] = ""
        elif rect1.collidepoint(center):
            self.built_frag = self.built_frag + " " + frag_list[1]
            self.click_sound.play()
            frag_list[1] = ""
        elif rect2.collidepoint(center):
            self.built_frag = self.built_frag + " " + frag_list[2]
            self.click_sound.play()
            frag_list[2] = ""

        if frag_list[0] == "" and frag_list[1] == "" and frag_list[2] == "":
            self.built_frag = self.built_frag[1:]
            if self.built_frag == self.sentence:
                self.score += 1
                self.beep_sound.play()
                self.end_round(frag_list)
            else:
                self.score -= 1
                self.buzz_sound.play()
                self.end_round(frag_list)
        else:
            try:
                pygame.draw.circle(self._frame_surface, color, center, 40, 0)
            except:
                pass

    def draw_ind_intro_point(self, joints, jointPoints, color, joint0):
        joint0State = joints[joint0].TrackingState;
        
        if (joint0State == PyKinectV2.TrackingState_NotTracked or
            joint0State == PyKinectV2.TrackingState_Inferred):
            return

        center = (int(jointPoints[joint0].x), int(jointPoints[joint0].y))

        try:
            pygame.draw.circle(self._frame_surface, color, center, 40, 0)
        except:
            pass

    def update_intro_screen(self, joints, jointPoints, color):
        self._frame_surface.fill(BG_COLOR)# blank screen before drawing points
        pygame.draw.rect(self._frame_surface, HIGHLIGHT_COLOR, (400, 300, 50, 50), 0)
        pygame.draw.rect(self._frame_surface, HIGHLIGHT_COLOR, (self._frame_surface.get_width() / 2, 200, 50, 50), 0)
        pygame.draw.rect(self._frame_surface, HIGHLIGHT_COLOR, (self._frame_surface.get_width() - 400, 300, 50, 50), 0)
        # draw rects here as examples

        self.draw_ind_intro_point(joints, jointPoints, color, PyKinectV2.JointType_Head)
        self.draw_ind_intro_point(joints, jointPoints, color, PyKinectV2.JointType_WristLeft)
        # may change PyKinectV2.JointType_WristRight to PyKinectV2.JointType_ElbowRight
        self.draw_ind_intro_point(joints, jointPoints, color, PyKinectV2.JointType_WristRight)

    def update_screen(self, joints, jointPoints, color, highlight_color, frag_list, seconds):
        self._frame_surface.fill(BG_COLOR)# blank screen before drawing points

        self.message_display(self.built_frag, (300, 750), 2)
        rect0 = self.message_display(frag_list[0], (400, 300), 1)
        rect1 = self.message_display(frag_list[1], (self._frame_surface.get_width()/2, 200), 1)
        rect2 = self.message_display(frag_list[2], (self._frame_surface.get_width() - 400, 300), 1)
        self.message_display(str(self.score), (self._frame_surface.get_width() / 2, 800), 1)
        self.message_display(str(seconds), (self._frame_surface.get_width() - 300, 800), 1)

        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_Head, frag_list)
        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_WristRight, frag_list)
        # may change PyKinectV2.JointType_WristRight to PyKinectV2.JointType_ElbowRight
        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_WristLeft, frag_list)

    def end_round(self, frag_list):
        self._frame_surface.fill(BG_COLOR)

        self.message_display(self.built_frag, (300, 750), 2)
        rect0 = self.message_display(frag_list[0], (300, 300), 1)
        rect1 = self.message_display(frag_list[1], (self._frame_surface.get_width() / 2, 100), 1)
        rect2 = self.message_display(frag_list[2], (self._frame_surface.get_width() - 300, 300), 1)
        self.message_display(str(self.score), (self._frame_surface.get_width() / 2, 800), 1)
        h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
        target_height = int(h_to_w * self._screen.get_width())
        surface_to_draw = pygame.transform.scale(self._frame_surface,
                                                     (self._screen.get_width(), target_height));
        self._screen.blit(surface_to_draw, (0,0))
        surface_to_draw = None
        pygame.display.update()
        pygame.time.delay(500)
        self.new_round()        
                  
    def end_game(self):
        self._frame_surface.fill(BG_COLOR)
        self.message_display("Score: {}".format(self.score), (self._frame_surface.get_width() / 2, self._frame_surface.get_height() / 2), 1)
        h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
        target_height = int(h_to_w * self._screen.get_width())
        surface_to_draw = pygame.transform.scale(self._frame_surface,
                                                     (self._screen.get_width(), target_height));
        self._screen.blit(surface_to_draw, (0,0))
        surface_to_draw = None
        pygame.display.update()
        pygame.time.delay(3000)
        self._kinect.close()
        pygame.quit()
        sys.exit()

    def new_round(self):
        self.sentence = random.sample(self.sentence_list, 1)[0]
        self.built_frag = ""
        frag_list = self.fragment_sentence(self.sentence)
        random.shuffle(frag_list)
        pygame.time.delay(500)
        
        while not self.finished:
            seconds = int(GAME_TIME - (pygame.time.get_ticks() - self.start_ticks) / 1000)
            if seconds <= 0:
                self.end_game()
                             
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            if self._bodies is not None:
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.update_screen(joints, joint_points, TRACKING_COLOR,
                                       HIGHLIGHT_COLOR, frag_list, seconds)# check here

            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface,
                                                     (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            self._clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True 

        self.end_game()

    def run(self):
        self.score = 0
        while not self.finished:
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            if self._bodies is not None:
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.update_intro_screen(joints, joint_points, TRACKING_COLOR)

            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface,
                                                     (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            self._clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.start_ticks = pygame.time.get_ticks()
                    self.new_round()
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True              

        self._kinect.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BodyGameRuntime()
    game.run()
