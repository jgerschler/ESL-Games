import pygame
import random
import sys
from pygame.locals import *

class TimedWordsTeamGame(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (230, 230, 0)
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 255)
    INV_PLAY_TIME = 0.5
    NUM_TEAM_MEMBERS = 30

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.sound_right = pygame.mixer.Sound('audio\\beep.ogg')
        self.sound_wrong = pygame.mixer.Sound('audio\\buzzer.ogg')
        self.sound_win = pygame.mixer.Sound('audio\\win.ogg')

        self.xRes = 1024
        self.yRes = 768

        self.DISPLAYSURF = pygame.display.set_mode((self.xRes, self.yRes), 0, 32)
        pygame.display.set_caption('Timed Words Team Game')
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        self.font = pygame.font.SysFont(None, 72)
        self.team_font = pygame.font.SysFont(None, 32)

        self.team_1_name = "Team 1"
        self.team_2_name = "Team 2"

        self.active_team = random.sample([1, 2], 1)[0]

        self.team_1_score = 0
        self.team_2_score = 0
        
        self.words = [[["q11","q"],["q12","q"],["q13","q"],["a14","a"]],# add desired content here
                      [["q21","q"],["q22","q"],["q23","q"],["a24","a"]],
                      [["q31","q"],["q32","q"],["q33","q"],["a34","a"]],
                      [["q41","q"],["q42","q"],["q43","q"],["a44","a"]]]

    def refresh_display(self):     
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)
        
        active_team_label = self.font.render("Team {0}".format(self.active_team), True, TimedWordsTeamGame.BLACK)
        team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
        team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

        active_team_label_rect = active_team_label.get_rect()
        team_1_label_rect = team_1_label.get_rect()
        team_2_label_rect = team_2_label.get_rect()

        active_team_label_rect.center = (self.xRes / 2, self.yRes / 2)
        team_1_label_rect.left = 10
        team_2_label_rect.right = self.xRes - 10
        team_1_label_rect.bottom = self.yRes - 10
        team_2_label_rect.bottom = self.yRes - 10

        self.DISPLAYSURF.blit(active_team_label, active_team_label_rect)
        self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
        self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)

        team_1_rect = pygame.Rect(10,
                                ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                40,
                                (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
        
        team_2_rect = pygame.Rect(self.xRes - 50,
                                ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                40,
                                (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
        pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.new_word()

    def game_score(self, key):
        self.end_ticks = pygame.time.get_ticks()
        team_scores = [self.team_1_score, self.team_2_score]
        points = 1000 / (self.end_ticks - self.start_ticks)

        if key == 'a':
            if self.word_list[0][1] == 'a':
                team_scores[self.active_team - 1] += points
                self.team_1_score, self.team_2_score = team_scores[0], team_scores[1]
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.GREEN)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.BLACK)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.BLACK)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLACK)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_right.play()
            else:
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.RED)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.BLACK)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.BLACK)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLACK)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_wrong.play()

        if key == 'b':
            if self.word_list[1][1] == 'a':
                team_scores[self.active_team - 1] += points
                self.team_1_score, self.team_2_score = team_scores[0], team_scores[1]
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.GREEN)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.BLACK)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLACK)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_right.play()
            else:
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.RED)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.BLACK)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLACK)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_wrong.play()
                
        if key == 'c':
            if self.word_list[2][1] == 'a':
                team_scores[self.active_team - 1] += points
                self.team_1_score, self.team_2_score = team_scores[0], team_scores[1]
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.BLACK)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.GREEN)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLACK)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_right.play()
            else:
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.BLACK)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.RED)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLACK)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_wrong.play()
                
        if key == 'd':
            if self.word_list[3][1] == 'a':
                team_scores[self.active_team - 1] += points
                self.team_1_score, self.team_2_score = team_scores[0], team_scores[1]
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.BLACK)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.BLACK)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.GREEN)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_right.play()
            else:
                self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

                team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
                team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

                team_1_label_rect = team_1_label.get_rect()
                team_2_label_rect = team_2_label.get_rect()

                team_1_label_rect.left = 10
                team_2_label_rect.right = self.xRes - 10
                team_1_label_rect.bottom = self.yRes - 10
                team_2_label_rect.bottom = self.yRes - 10

                team_1_rect = pygame.Rect(10,
                                        ((self.yRes - 40) - ((self.team_1_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_1_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))
                
                team_2_rect = pygame.Rect(self.xRes - 50,
                                        ((self.yRes - 40) - ((self.team_2_score) * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS)))),
                                        40,
                                        (self.team_2_score * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))))

                frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
                frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.BLACK)
                frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.BLACK)
                frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.RED)

                frag_1_text_rect = frag_1_text.get_rect()
                frag_2_text_rect = frag_1_text.get_rect()
                frag_3_text_rect = frag_1_text.get_rect()
                frag_4_text_rect = frag_1_text.get_rect()

                frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
                frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
                frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
                frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

                self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
                self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
                self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
                self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
                self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
                self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
                pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
                pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

                pygame.display.update()
                self.sound_wrong.play()

        if (team_scores[self.active_team - 1] * ((self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME * TimedWordsTeamGame.NUM_TEAM_MEMBERS))) >= (self.yRes - 80):
            self.game_over()

        pygame.time.delay(3000)# modify according to needs
            
        self.active_team = 1 if self.active_team == 2 else 2
        
        self.refresh_display()
    
    def game_over(self): 
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        text = self.font.render("Team {0} wins!".format(self.active_team), True, TimedWordsTeamGame.GREEN)
        textpos = text.get_rect()
        textpos.center = (self.xRes / 2, self.yRes / 2)
        self.DISPLAYSURF.blit(text,textpos)

        self.team_1_score = 0
        self.team_2_score = 0

        pygame.display.update()

        self.sound_win.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.run()

    def new_word(self):
        self.word_list = random.sample(self.words, 1)[0]
        random.shuffle(self.word_list)
        
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
        team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

        team_1_label_rect = team_1_label.get_rect()
        team_2_label_rect = team_2_label.get_rect()

        team_1_label_rect.left = 10
        team_2_label_rect.right = self.xRes - 10
        team_1_label_rect.bottom = self.yRes - 10
        team_2_label_rect.bottom = self.yRes - 10

        team_1_rect = pygame.Rect(10,
                                ((self.yRes - 40) - (self.team_1_score) *
                                (self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME *
                                                  TimedWordsTeamGame.NUM_TEAM_MEMBERS)),
                                40,
                                (self.team_1_score) *
                                (self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME *
                                                  TimedWordsTeamGame.NUM_TEAM_MEMBERS))
        
        team_2_rect = pygame.Rect(self.xRes - 50,
                                ((self.yRes - 40) - (self.team_2_score) *
                                (self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME *
                                                  TimedWordsTeamGame.NUM_TEAM_MEMBERS)),
                                40,
                                (self.team_2_score) *
                                (self.yRes - 80) / (TimedWordsTeamGame.INV_PLAY_TIME *
                                                  TimedWordsTeamGame.NUM_TEAM_MEMBERS))

        frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.RED)
        frag_2_text = self.team_font.render(self.word_list[1][0], True, TimedWordsTeamGame.YELLOW)
        frag_3_text = self.team_font.render(self.word_list[2][0], True, TimedWordsTeamGame.GREEN)
        frag_4_text = self.team_font.render(self.word_list[3][0], True, TimedWordsTeamGame.BLUE)

        frag_1_text_rect = frag_1_text.get_rect()
        frag_2_text_rect = frag_1_text.get_rect()
        frag_3_text_rect = frag_1_text.get_rect()
        frag_4_text_rect = frag_1_text.get_rect()

        frag_1_text_rect.center = (self.xRes / 2, (1 / 5) * self.yRes)
        frag_2_text_rect.center = (self.xRes / 2, (2 / 5) * self.yRes)
        frag_3_text_rect.center = (self.xRes / 2, (3 / 5) * self.yRes)
        frag_4_text_rect.center = (self.xRes / 2, (4 / 5) * self.yRes)

        self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
        self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)
        self.DISPLAYSURF.blit(frag_1_text, frag_1_text_rect)
        self.DISPLAYSURF.blit(frag_2_text, frag_2_text_rect)
        self.DISPLAYSURF.blit(frag_3_text, frag_3_text_rect)
        self.DISPLAYSURF.blit(frag_4_text, frag_4_text_rect)

        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
        pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

        pygame.display.update()
                
        self.start_ticks = pygame.time.get_ticks()
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.refresh_display()
                    if event.key == pygame.K_d:#these pygame keys (a, e, i, m) will depend on your hardware setup
                        self.game_score('a')
                    if event.key == pygame.K_h:
                        self.game_score('b')
                    if event.key == pygame.K_l:
                        self.game_score('c')
                    if event.key == pygame.K_p:
                        self.game_score('d')
                    
            pygame.display.update()

if __name__ == '__main__':
    new_instance = TimedWordsTeamGame()
    new_instance.run()
