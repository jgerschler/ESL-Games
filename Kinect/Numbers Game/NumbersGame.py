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
import threading
import win32com.client as wincl

TRACKING_COLOR = pygame.color.Color("green")
HIGHLIGHT_COLOR = pygame.color.Color("red")
BG_COLOR = pygame.color.Color("white")
GAME_TIME = 60# seconds

class Speaker(threading.Thread):
    def __init__(self, chosen_number):
        threading.Thread.__init__(self)
        self.speak = wincl.Dispatch("SAPI.SpVoice")
        self.chosen_number = chosen_number

    def run(self):
        self.speak.Speak(self.chosen_number)
        self.speak.Speak(self.chosen_number)

class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()      

        self.beep_sound = pygame.mixer.Sound('audio\\beep.ogg')
        self.buzz_sound = pygame.mixer.Sound('audio\\buzz.ogg')
        self._infoObject = pygame.display.Info()
##        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1,
##                                                self._infoObject.current_h >> 1),
##                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)

        pygame.display.set_caption("Numbers Game")

        self.finished = False
        self._clock = pygame.time.Clock()
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                                       PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width,
                                              self._kinect.color_frame_desc.Height), 0, 32)
        self._bodies = None

        self.score = 0

        self._frame_surface.fill((255, 255, 255))

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()

    def message_display(self, text, loc_tuple, loc_int):
        # loc_int: 1 center, 2 top left, 3 bottom left, 4 bottom right, 5 top right
        text_surf, text_rect = self.text_objects(text, pygame.font.Font(None, 128))
        loc_dict = {1:'text_rect.center', 2:'text_rect.topleft', 3:'text_rect.bottomleft',
                    4:'text_rect.bottomright', 5:'text_rect.topright'}
        exec(loc_dict[loc_int] + ' = loc_tuple')
        self._frame_surface.blit(text_surf, text_rect)
        return text_rect 

    def draw_ind_point(self, joints, jointPoints, color, highlight_color, rect0, rect1, rect2, joint0, numbers, chosen_number):
        joint0State = joints[joint0].TrackingState;
        
        if (joint0State == PyKinectV2.TrackingState_NotTracked or
            joint0State == PyKinectV2.TrackingState_Inferred):
            return

        center = (int(jointPoints[joint0].x), int(jointPoints[joint0].y))

        if ((rect0.collidepoint(center) and numbers[0] == chosen_number) or
            (rect1.collidepoint(center) and numbers[1] == chosen_number) or
            (rect2.collidepoint(center) and numbers[2] == chosen_number)):
            self.score += 1
            self.beep_sound.play()
            pygame.time.delay(500)
            self.new_round()
        elif rect0.collidepoint(center) or rect1.collidepoint(center) or rect2.collidepoint(center):
            try:
                pygame.draw.circle(self._frame_surface, highlight_color, center, 40, 0)
                self.score -= 1
                self.buzz_sound.play()
                pygame.time.delay(500)
                self.new_round()
            except: # need to catch it due to possible invalid positions (with inf)
                pass
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

    def update_screen(self, joints, jointPoints, color, highlight_color, numbers, chosen_number, seconds):
        self._frame_surface.fill(BG_COLOR)# blank screen before drawing points
        # need to make these coordinates relative
        rect0 = self.message_display(numbers[0], (400, 300), 1)
        rect1 = self.message_display(numbers[1], (self._frame_surface.get_width()/2, 200), 1)
        rect2 = self.message_display(numbers[2], (self._frame_surface.get_width() - 400, 300), 1)
        self.message_display(str(self.score), (self._frame_surface.get_width() / 2, 800), 1)
        self.message_display(str(seconds), (self._frame_surface.get_width() - 300, 800), 1)

        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_Head, numbers, chosen_number)
        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_WristRight, numbers, chosen_number)
        # may change PyKinectV2.JointType_WristRight to PyKinectV2.JointType_ElbowRight
        self.draw_ind_point(joints, jointPoints, color, highlight_color, rect0,
                            rect1, rect2, PyKinectV2.JointType_WristLeft, numbers, chosen_number)

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
        numbers = [str(x) for x in random.sample(range(0, 100), 3)]
        chosen_number = str(random.sample(numbers, 1)[0])
        speaker = Speaker(chosen_number)
        speaker.start()
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
                    self.update_screen(joints, joint_points, TRACKING_COLOR, HIGHLIGHT_COLOR, numbers, chosen_number, seconds)# here

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
