import pygame
import sys
from pygame.locals import *
from random import randint

class TimedWordsTeamGame(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    def __init__(self):
        pygame.init()

        self.xRes = 1024
        self.yRes = 768

        self.DISPLAYSURF = pygame.display.set_mode((self.xRes, self.yRes), 0, 32)
        pygame.display.set_caption('Timed Words Team Game')
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        self.font = pygame.font.SysFont(None, 72)
        self.team_font = pygame.font.SysFont(None, 32)

        self.answers_to_win = 20
        self.winning_score = (self.yRes-40)/2#self.yRes minus 40px team name rectangle
        self.points_per_question = self.winning_score/self.answers_to_win

        self.team_1_name = "Team 1"
        self.team_2_name = "Team 2"

        self.team_1_score = 0
        self.team_2_score = 0

        self.active_word = ''
        self.active_word_class = ''
        
        self.words = [[["q11","q"],["q12","q"],["q13","q"],["a14","a"]],
                      [["q21","q"],["q22","q"],["q23","q"],["a24","a"]],
                      [["q31","q"],["q32","q"],["q33","q"],["a34","a"]],
                      [["q41","q"],["q42","q"],["q43","q"],["a44","a"]]]

    def refresh_display(self):
        team1Label = self.team_font.render(self.team_1_name, True, TimedWordsTeamGame.BLACK)
        team2Label = self.team_font.render(self.team_2_name, True, TimedWordsTeamGame.BLACK)

        team1LabelPos = team1Label.get_rect()
        team2LabelPos = team2Label.get_rect()

        team1LabelPos.centerx = (3*self.xRes/16)/2
        team2LabelPos.centerx = ((2*self.xRes/16)+(self.xRes/10)+(2*self.xRes/16)+(self.xRes/10)+(self.xRes/16))/2

        team1LabelPos.centery = (2*self.yRes-40)/2
        team2LabelPos.centery = (2*self.yRes-40)/2

        self.DISPLAYSURF.blit(team1Label,team1LabelPos)
        self.DISPLAYSURF.blit(team2Label,team2LabelPos)

        team1Rect = pygame.Rect(self.xRes/16,self.yRes-self.team_1_score-40,self.xRes/16,self.team_1_score)
        team2Rect = pygame.Rect((2*self.xRes/16)+(self.xRes/10),self.yRes-self.team_2_score-40,self.xRes/16,self.team_2_score)

        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team1Rect)
        pygame.draw.rect(self.DISPLAYSURF, TimedWordsTeamGame.RED, team2Rect)

        pygame.draw.line(self.DISPLAYSURF, TimedWordsTeamGame.BLUE, (0, (self.yRes-40)/2), (self.xRes, (self.yRes-40)/2), 4)

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
        randomWordInt = randint(0,len(self.vocab_tuples)-1)
        self.active_word = self.vocab_tuples[randomWordInt][0]
        self.active_word_class = self.vocab_tuples[randomWordInt][1]
        
        self.DISPLAYSURF.fill(TimedWordsTeamGame.WHITE)

        text = self.font.render(self.active_word, True, TimedWordsTeamGame.BLACK)
        textpos = text.get_rect()
        textpos.centerx = self.DISPLAYSURF.get_rect().centerx
        textpos.y = self.yRes/4
        self.DISPLAYSURF.blit(text,textpos)

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
##                if event.type == pygame.KEYUP:
##                    if event.key == pygame.K_SPACE:
##                        self.new_word()
##                    if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
##                        if self.active_word_class == 'adj':
##                            self.key_bindings_dict[event.key](self.points_per_question)
##                            self.deactivate_keys()#alter as needed to affect classroom speed, use delay if needed
##                        else:
##                            self.key_bindings_dict[event.key](-self.points_per_question)
##                            self.deactivate_keys()
##                    if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
##                        if self.active_word_class == 'noun':
##                            self.key_bindings_dict[event.key](self.points_per_question)
##                            self.deactivate_keys()
##                        else:
##                            self.key_bindings_dict[event.key](-self.points_per_question)
##                            self.deactivate_keys()
##                    if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
##                        if self.active_word_class == 'verb':
##                            self.key_bindings_dict[event.key](self.points_per_question)
##                            self.deactivate_keys()
##                        else:
##                            self.key_bindings_dict[event.key](-self.points_per_question)
##                            self.deactivate_keys()

            pygame.display.update()

if __name__ == '__main__':
    new_instance = TimedWordsTeamGame()
    new_instance.run()
