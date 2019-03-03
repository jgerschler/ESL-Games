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
        self.sound_miss = pygame.mixer.Sound('audio\\ricochet.ogg')
        self.image_shot = pygame.image.load('images\\bang.png')

        self.object_lower = (94, 126, 129)# HSV color range for object to be tracked
        self.object_upper = (131, 255, 255)

        self.verbs = ['Accept', 'Care', 'Could', 'Enjoy', 'Happen', 'Lead', 'Open',
                      'Reduce', 'Settle', 'Teach', 'Carry', 'Count', 'Examine',
                      'Hate', 'Learn', 'Order', 'Refer', 'Shake', 'Tell', 'Catch',
                      'Cover', 'Exist', 'Have', 'Leave', 'Ought', 'Reflect', 'Shall',
                      'Tend', 'Cause', 'Create', 'Expect', 'Head', 'Lend', 'Own',
                      'Refuse', 'Share', 'Test', 'Change', 'Cross', 'Experience',
                      'Hear', 'Let', 'Pass', 'Regard', 'Shoot', 'Thank', 'Charge',
                      'Cry', 'Explain', 'Help', 'Lie', 'Pay', 'Relate', 'Should',
                      'Think', 'Check', 'Cut', 'Express', 'Hide', 'Like', 'Perform',
                      'Release', 'Shout', 'Throw', 'Choose', 'Damage', 'Extend',
                      'Hit', 'Limit', 'Pick', 'Remain', 'Show', 'Touch', 'Claim',
                      'Dance', 'Face', 'Hold', 'Link', 'Place', 'Remember', 'Shut',
                      'Train', 'Clean', 'Deal', 'Fail', 'Hope', 'Listen', 'Plan',
                      'Remove', 'Sing', 'Travel', 'Clear', 'Decide', 'Fall', 'Hurt',
                      'Live', 'Play', 'Repeat', 'Sit', 'Treat', 'Climb', 'Deliver',
                      'Fasten', 'Identify', 'Look', 'Point', 'Replace', 'Sleep', 'Try',
                      'Close', 'Demand', 'Feed', 'Imagine', 'Lose', 'Prefer', 'Reply',
                      'Smile', 'Turn', 'Collect', 'Deny', 'Feel', 'Improve', 'Love',
                      'Prepare', 'Report', 'Sort', 'Understand', 'Come', 'Depend',
                      'Fight', 'Include', 'Make', 'Present', 'Represent', 'Sound',
                      'Use', 'Commit', 'Describe', 'Fill', 'Increase', 'Manage',
                      'Press', 'Require', 'Speak', 'Compare', 'Design', 'Find',
                      'Indicate', 'Mark', 'Prevent', 'Rest', 'Stand', 'Visit',
                      'Complain', 'Destroy', 'Finish', 'Influence', 'Matter',
                      'Produce', 'Result', 'Start', 'Vote', 'Complete', 'Develop',
                      'Fit', 'Inform', 'May', 'Promise', 'Return', 'State', 'Wait',
                      'Concern', 'Die', 'Fly', 'Intend', 'Mean', 'Protect', 'Reveal',
                      'Stay', 'Walk', 'Confirm', 'Disappear', 'Fold', 'Introduce',
                      'Measure', 'Prove', 'Ring', 'Stick', 'Want', 'Connect',
                      'Discover', 'Follow', 'Invite', 'Meet', 'Provide', 'Rise',
                      'Stop', 'Warn', 'Consider', 'Discuss', 'Force', 'Involve',
                      'Mention', 'Publish', 'Roll', 'Study', 'Wash', 'Consist',
                      'Divide', 'Forget', 'Join', 'Might', 'Pull', 'Run', 'Succeed',
                      'Watch', 'Contact', 'Do', 'Forgive', 'Jump', 'Mind', 'Push',
                      'Save', 'Suffer', 'Wear', 'Contain', 'Draw', 'Form', 'Keep',
                      'Miss', 'Put', 'Say', 'Suggest', 'Will', 'Continue', 'Dress',
                      'Found', 'Kick', 'Move', 'Raise', 'See', 'Suit', 'Win',
                      'Contribute', 'Drink', 'Gain', 'Kill', 'Must', 'Reach',
                      'Seem', 'Supply', 'Wish', 'Control', 'Drive', 'Get', 'Knock',
                      'Need', 'Read', 'Sell', 'Support', 'Wonder', 'Cook', 'Drop',
                      'Give', 'Know', 'Notice', 'Realize', 'Send', 'Suppose', 'Work',
                      'Copy', 'Eat', 'Go', 'Last', 'Obtain', 'Receive', 'Separate',
                      'Survive', 'Worry', 'Correct', 'Enable', 'Grow', 'Laugh',
                      'Occur', 'Recognize', 'Serve', 'Take', 'Would', 'Cost',
                      'Encourage', 'Handle', 'Lay', 'Offer', 'Record', 'Set',
                      'Talk', 'Write']
        
        self.adjectives = ['Ambitious', 'Single-minded', 'Determined', 'Reliable',
                           'Honest', 'Stable', 'Independent', 'Confident', 'Calm ',
                           'Loyal', 'Sympathetic', 'Sociable', 'Creative',
                           'Energetic', 'Enthusiastic', 'Unambitious',
                           'Incompetent', 'Competent', 'Dependent',
                           'Experienced', 'Inexperienced', 'Formal', 'Informal',
                           'Reasonable', 'Unreasonable', 'Unreliable', 'Sensitive',
                           'Insensitive', 'Unsociable', 'Tolerant', 'Intolerant',
                           'Creative', 'Funny', 'Organized', 'Disorganized',
                           'Uncreative', 'Competitive', 'Uncompetitive', 'Arrogant',
                           'Humble', 'Timid', 'Shy', 'Introverted', 'Extroverted',
                           'Helpful', 'Unhelpful', 'Outgoing', 'Friendly',
                           'Unfriendly', 'Generous', 'Selfish', 'Easy-going',
                           'Laid-back', 'Practical', 'Down-to-earth', 'Rude',
                           'Patient', 'Considerate', 'Dishonest', 'Inconsiderate']

        self.finished = False

#        self.game_display = pygame.display.set_mode((800,600))
        self.game_display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pistolero Game')
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
        self.word_list = random.sample(self.verbs, 3)# update this with dictionary for more flexibility
        self.word_list.append(random.sample(self.adjectives, 1)[0])
        random.shuffle(self.word_list)
        
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
        self.camera = cv2.VideoCapture(0)# 0 if you only have one cam
        
        self.word_list = random.sample(self.verbs, 3)# update this with dictionary for more flexibility
        self.word_list.append(random.sample(self.adjectives, 1)[0])
        random.shuffle(self.word_list)

        self.score = 0
        int_x, int_y = 0, 0
        start_ticks = pygame.time.get_ticks()
        
        while not self.finished:
            seconds = (pygame.time.get_ticks()-start_ticks)/1000
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
##                if radius > 10:# left here for troubleshooting purposes
##                    cv2.circle(frame, (int_x, int_y), int(radius), (0, 255, 255), 2)
##            cv2.imshow("Frame", frame)
            
            self.game_display.fill(PistolGame.WHITE)
            rect0 = self.message_display_topleft(self.word_list[0], (100, 100))
            rect1 = self.message_display_bottomleft(self.word_list[1], (100, self.display_height - 100))
            rect2 = self.message_display_topright(self.word_list[2], (self.display_width - 100, 100))
            rect3 = self.message_display_bottomright(self.word_list[3], (self.display_width - 100, self.display_height - 100))
            react_score = self.message_display_center("{0} {1}".format(str(self.score), int(PistolGame.GAME_TIME - seconds)),
                                                      (int(self.display_width/2), int(self.display_height - 50)))
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
                    # update to use dictionary here?
                    if (rect0.collidepoint(int_x, int_y) and self.word_list[0] in self.adjectives):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect1.collidepoint(int_x, int_y) and self.word_list[1] in self.adjectives):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect2.collidepoint(int_x, int_y) and self.word_list[2] in self.adjectives):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect3.collidepoint(int_x, int_y) and self.word_list[3] in self.adjectives):
                        self.sound_shot.play()
                        self.score+=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect0.collidepoint(int_x, int_y) and self.word_list[0] in self.verbs):
                        self.sound_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect0.center[0]-self.image_shot.get_width()/2, rect0.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect1.collidepoint(int_x, int_y) and self.word_list[1] in self.verbs):
                        self.sound_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect1.center[0]-self.image_shot.get_width()/2, rect1.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect2.collidepoint(int_x, int_y) and self.word_list[2] in self.verbs):
                        self.sound_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect2.center[0]-self.image_shot.get_width()/2, rect2.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    elif (rect3.collidepoint(int_x, int_y) and self.word_list[3] in self.verbs):
                        self.sound_shot.play()
                        self.score-=1
                        self.game_display.blit(self.image_shot, (rect3.center[0]-self.image_shot.get_width()/2, rect3.center[1]-self.image_shot.get_height()/2))
                        pygame.display.update()
                        pygame.time.delay(300)
                    else:
                        self.sound_miss.play()

                    self.new_round()

                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.finished = True

            pygame.display.update()

        self.camera.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()
        
if __name__ == '__main__':
    pg = PistolGame()
    pg.run()
