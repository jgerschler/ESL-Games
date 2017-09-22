import pygame
import random
import sys
from pygame.locals import *

class TimedWordsTeamGame(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    INV_PLAY_TIME = 0.5
    NUM_TEAM_MEMBERS = 30
    TEST_TIME_S = 10

    def __init__(self):
        pygame.init()

        self.xRes = 1024
        self.yRes = 768

        self.DISPLAYSURF = pygame.display.set_mode((self.xRes, self.yRes), 0, 32)
        pygame.display.set_caption('Timed Words Team Game')
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        self.font = pygame.font.SysFont(None, 72)
        self.team_font = pygame.font.SysFont(None, 32)

        self.team_1_name = "Team 1"
        self.team_2_name = "Team 2"

        self.team_1_score = 0
        self.team_2_score = 0
        
        self.words = [[["q11","q"],["q12","q"],["q13","q"],["a14","a"]],
                      [["q21","q"],["q22","q"],["q23","q"],["a24","a"]],
                      [["q31","q"],["q32","q"],["q33","q"],["a34","a"]],
                      [["q41","q"],["q42","q"],["q43","q"],["a44","a"]]]

    def refresh_display(self):
        team_1_label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
        team_2_label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

        team_1_label_rect = team_1_label.get_rect()
        team_2_label_rect = team_2_label.get_rect()

        team_1_label_rect.left = 10
        team_2_label_rect.right = self.xRes - 10
        team_1_label_rect.bottom = self.yRes - 10
        team_2_label_rect.bottom = self.yRes - 10

        self.DISPLAYSURF.blit(team_1_label, team_1_label_rect)
        self.DISPLAYSURF.blit(team_2_label, team_2_label_rect)

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

        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team_1_rect)
        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, team_2_rect)
        pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLACK, (0, 40), (self.xRes, 40), 4)

        pygame.display.update()
        return

    def game_over(self, team): 
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        text = self.font.render(team + ' wins!', True, TimedWordsTeamGame.RED)
        textpos = text.get_rect()
        textpos.centerx = self.DISPLAYSURF.get_rect().centerx
        textpos.y = self.yRes/4
        self.DISPLAYSURF.blit(text,textpos)

        self.refresh_display()

        self.team_1_score = 0
        self.team_2_score = 0

        randomWordInt = randint(0,len(self.vocab_tuples)-1)
        self.active_word = self.vocab_tuples[randomWordInt][0]
        self.active_word_class = self.vocab_tuples[randomWordInt][1]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    return
                
    def deactivate_keys(self):
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        text = self.font.render(self.active_word, True, TimedWordsTeamGame.BLACK)
        textpos = text.get_rect()
        textpos.centerx = self.DISPLAYSURF.get_rect().centerx
        textpos.y = self.yRes/4
        self.DISPLAYSURF.blit(text,textpos)

        self.refresh_display()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    return

    def new_word(self):
        self.word_list = random.sample(self.words, 1)[0]
        random.shuffle(self.word_list)
        print(self.word_list)
        
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

        frag_1_text = self.team_font.render(self.word_list[0][0], True, TimedWordsTeamGame.BLACK)
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

        self.refresh_display()

    def team_1_score_update(self, score):
        self.team_1_score += score
        if self.team_1_score < 0:
            self.team_1_score = 0
        if self.team_1_score >= self.winning_score:
            self.game_over(self.team_1_name)

    def team_2_score_update(self, score):
        self.team_2_score += score
        if self.team_2_score < 0:
            self.team_2_score = 0
        if self.team_2_score >= self.winning_score:
            self.game_over(self.team_2_name)

    def run(self):
        self.refresh_display()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.new_word()
                    if event.key == pygame.K_a:
                        pass
                    if event.key == pygame.K_e:
                        pass
                    if event.key == pygame.K_i:
                        pass
                    if event.key == pygame.K_m:
                        pass
                    
                        



            pygame.display.update()

if __name__ == '__main__':
    new_instance = TimedWordsTeamGame()
    new_instance.run()
