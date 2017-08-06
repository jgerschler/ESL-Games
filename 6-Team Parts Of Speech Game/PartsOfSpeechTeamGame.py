import pygame
import sys
from pygame.locals import *
from random import randint

class PartsOfSpeechTeamGame(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    def __init__(self):
        pygame.init()

        self.xRes = 1024
        self.yRes = 768

        self.DISPLAYSURF = pygame.display.set_mode((self.xRes, self.yRes), 0, 32)
        pygame.display.set_caption('Parts of Speech Game')
        self.DISPLAYSURF.fill(PartsOfSpeechTeamGame.WHITE)

        self.font = pygame.font.SysFont(None, 72)
        self.team_font = pygame.font.SysFont(None, 32)

        self.team_1_name = 'Team 1'
        self.team_2_name = 'Team 2'
        self.team_3_name = 'Team 3'
        self.team_4_name = 'Team 4'
        self.team_5_name = 'Team 5'
        self.team_6_name = 'Team 6'

        #starting scores (add handicap as necessary). Will affect answers required to win, effect varies based on screen resolution.

        self.team1Score = 0
        self.team2Score = 0
        self.team3Score = 0
        self.team4Score = 0
        self.team5Score = 0
        self.team6Score = 0

        self.answers_to_win = 20
        self.winning_score = (self.yRes-40)/2#self.yRes minus 40px team name rectangle
        self.points_per_question = self.winning_score/self.answers_to_win


        self.vocab_tuples = (('agree','verb'),('allow','verb'),('appear','verb'),('ask','verb'),('be','verb'),('become','verb'),
                       ('begin','verb'),('believe','verb'),('belong','verb'),('bring','verb'),('build','verb'),('carry','verb'),
                       ('choose','verb'),('come','verb'),('connect','verb'),('consider','verb'),('continue','verb'),
                       ('contribute','verb'),('correct','verb'),('create','verb'),('decide','verb'),('deliver','verb'),
                       ('destroy','verb'),('develop','verb'),('discover','verb'),('discuss','verb'),('eat','verb'),('encourage','verb'),
                       ('explain','verb'),('follow','verb'),('get','verb'),('give','verb'),('go','verb'),('happen','verb'),
                       ('have','verb'),('hear','verb'),('imagine','verb'),('include','verb'),('involve','verb'),('know','verb'),
                       ('learn','verb'),('let','verb'),('lose','verb'),('make','verb'),('obtain','verb'),('open','verb'),('pay','verb'),
                       ('read','verb'),('realize','verb'),('receive','verb'),('remember','verb'),('say','verb'),('see','verb'),
                       ('seem','verb'),('sell','verb'),('send','verb'),('serve','verb'),('sit','verb'),('speak','verb'),('spend','verb'),
                       ('suffer','verb'),('suggest','verb'),('take','verb'),('teach','verb'),('tell','verb'),('think','verb'),
                       ('try','verb'),('understand','verb'),('want','verb'),('write','verb'),

                       ('red','adj'),('green','adj'),('purple','adj'),('yellow','adj'),('brown','adj'),('different','adj'),
                       ('important','adj'),('other','adj'),('new','adj'),('old','adj'),('young','adj'),('fat','adj'),('skinny','adj'),
                       ('pretty','adj'),('ugly','adj'),('beautiful','adj'),('nice','adj'),('fantastic','adj'),('long','adj'),('short','adj'),
                       ('tall','adj'),('big','adj'),('small','adj'),('political','adj'),('best','adj'),('worst','adj'),('happiest','adj'),
                       ('saddest','adj'),('flirtatious','adj'),('stinky','adj'),('smelly','adj'),('squishy','adj'),('greasy','adj'),
                       ('hot','adj'),('cold','adj'),('warm','adj'),('environmental','adj'),('financial','adj'),('scientific','adj'),
                       ('medical','adj'),('smart','adj'),('dumb','adj'),('hairy','adj'),('smooth','adj'),('rough','adj'),('lonely','adj'),
                       ('natural','adj'),('wrong','adj'),('incorrect','adj'),('correct','adj'),('afraid','adj'),('alive','adj'),('bad','adj'),
                       ('good','adj'),('annoying','adj'),('irritating','adj'),('brave','adj'),('broken','adj'),('cheap','adj'),
                       ('expensive','adj'),('dangerous','adj'),('empty','adj'),('full','adj'),('dry','adj'),('wet','adj'),('exciting','adj'),
                       ('boring','adj'),('great','adj'),

                       ('year','noun'),('people','noun'),('way','noun'),('day','noun'),('man','noun'),('thing','noun'),('woman','noun'),
                       ('life','noun'),('child','noun'),('world','noun'),('family','noun'),('student','noun'),('country','noun'),
                       ('problem','noun'),('week','noun'),('company','noun'),('system','noun'),('government','noun'),('night','noun'),
                       ('house','noun'),('car','noun'),('I','noun'),('you','noun'),('they','noun'),('he','noun'),('she','noun'),('it','noun'),
                       ('we','noun'),('book','noun'),('elephant','noun'),('cat','noun'),('dog','noun'),('hippopotamus','noun'),
                       ('magazine','noun'),('eye','noun'),('leg','noun'),('brain','noun'),('job','noun'),('business','noun'),
                       ('teacher','noun'),('mother','noun'),('father','noun'),('boy','noun'),('girl','noun'),('triangle','noun'),
                       ('rectangle','noun'),('history','noun'),('war','noun'),('art','noun'),('science','noun'),('nursing','noun'),
                       ('chemistry','noun'),('biotechnology','noun'),('money','noun'),('person','noun'),('health','noun'),('door','noun'),
                       ('window','noun'),('ceiling','noun'),('roof','noun'),('office','noun'),('computer','noun'),('Xbox','noun'),
                       ('stethescope','noun'),('injection','noun'),('tree','noun'),('boat','noun'),('river','noun'),('lake','noun'),
                       ('sky','noun'),('mango','noun'))

#colors



#customize team names



#how many correct answers to win?


#starting word

activeWord = ''
activeWordClass = ''

def RefreshDisplay():
    team1Label = self.team_font.render(self.team_1_name, True, PartsOfSpeechTeamGame.BLACK)
    team2Label = self.team_font.render(self.team_2_name, True, PartsOfSpeechTeamGame.BLACK)
    team3Label = self.team_font.render(self.team_3_name, True, PartsOfSpeechTeamGame.BLACK)
    team4Label = self.team_font.render(self.team_4_name, True, PartsOfSpeechTeamGame.BLACK)
    team5Label = self.team_font.render(self.team_5_name, True, PartsOfSpeechTeamGame.BLACK)
    team6Label = self.team_font.render(self.team_6_name, True, PartsOfSpeechTeamGame.BLACK)

    team1LabelPos = team1Label.get_rect()
    team2LabelPos = team2Label.get_rect()
    team3LabelPos = team3Label.get_rect()
    team4LabelPos = team4Label.get_rect()
    team5LabelPos = team5Label.get_rect()
    team6LabelPos = team6Label.get_rect()

    team1LabelPos.centerx = (3*self.xRes/16)/2
    team2LabelPos.centerx = ((2*self.xRes/16)+(self.xRes/10)+(2*self.xRes/16)+(self.xRes/10)+(self.xRes/16))/2
    team3LabelPos.centerx = ((3*self.xRes/16)+(2*self.xRes/10)+(3*self.xRes/16)+(2*self.xRes/10)+(self.xRes/16))/2
    team4LabelPos.centerx = ((4*self.xRes/16)+(3*self.xRes/10)+(4*self.xRes/16)+(3*self.xRes/10)+(self.xRes/16))/2
    team5LabelPos.centerx = ((5*self.xRes/16)+(4*self.xRes/10)+(5*self.xRes/16)+(4*self.xRes/10)+(self.xRes/16))/2
    team6LabelPos.centerx = ((6*self.xRes/16)+(5*self.xRes/10)+(6*self.xRes/16)+(5*self.xRes/10)+(self.xRes/16))/2

    team1LabelPos.centery = (2*self.yRes-40)/2
    team2LabelPos.centery = (2*self.yRes-40)/2
    team3LabelPos.centery = (2*self.yRes-40)/2
    team4LabelPos.centery = (2*self.yRes-40)/2
    team5LabelPos.centery = (2*self.yRes-40)/2
    team6LabelPos.centery = (2*self.yRes-40)/2

    DISPLAYSURF.blit(team1Label,team1LabelPos)
    DISPLAYSURF.blit(team2Label,team2LabelPos)
    DISPLAYSURF.blit(team3Label,team3LabelPos)
    DISPLAYSURF.blit(team4Label,team4LabelPos)
    DISPLAYSURF.blit(team5Label,team5LabelPos)
    DISPLAYSURF.blit(team6Label,team6LabelPos)

    team1Rect = pygame.Rect(self.xRes/16,self.yRes-team1Score-40,self.xRes/16,team1Score)
    team2Rect = pygame.Rect((2*self.xRes/16)+(self.xRes/10),self.yRes-team2Score-40,self.xRes/16,team2Score)
    team3Rect = pygame.Rect((3*self.xRes/16)+(2*self.xRes/10),self.yRes-team3Score-40,self.xRes/16,team3Score)
    team4Rect = pygame.Rect((4*self.xRes/16)+(3*self.xRes/10),self.yRes-team4Score-40,self.xRes/16,team4Score)
    team5Rect = pygame.Rect((5*self.xRes/16)+(4*self.xRes/10),self.yRes-team5Score-40,self.xRes/16,team5Score)
    team6Rect = pygame.Rect((6*self.xRes/16)+(5*self.xRes/10),self.yRes-team6Score-40,self.xRes/16,team6Score)

    pygame.draw.rect(DISPLAYSURF, PartsOfSpeechTeamGame.RED, team1Rect)
    pygame.draw.rect(DISPLAYSURF, PartsOfSpeechTeamGame.RED, team2Rect)
    pygame.draw.rect(DISPLAYSURF, PartsOfSpeechTeamGame.RED, team3Rect)
    pygame.draw.rect(DISPLAYSURF, PartsOfSpeechTeamGame.RED, team4Rect)
    pygame.draw.rect(DISPLAYSURF, PartsOfSpeechTeamGame.RED, team5Rect)
    pygame.draw.rect(DISPLAYSURF, PartsOfSpeechTeamGame.RED, team6Rect)

    pygame.draw.line(DISPLAYSURF, PartsOfSpeechTeamGame.BLUE, (0, (self.yRes-40)/2), (self.xRes, (self.yRes-40)/2), 4)

    pygame.display.update()
    return

def GameOver(team):

    global team1Score
    global team2Score
    global team3Score
    global team4Score
    global team5Score
    global team6Score
    global activeWord
    global activeWordClass
    
    DISPLAYSURF.fill(PartsOfSpeechTeamGame.WHITE)

    text = font.render(team+' wins!', True, PartsOfSpeechTeamGame.RED)
    textpos = text.get_rect()
    textpos.centerx = DISPLAYSURF.get_rect().centerx
    textpos.y = self.yRes/4
    DISPLAYSURF.blit(text,textpos)

    RefreshDisplay()

    team1Score = 0
    team2Score = 0
    team3Score = 0
    team4Score = 0
    team5Score = 0
    team6Score = 0

    randomWordInt = randint(0,len(self.vocab_tuples)-1)
    activeWord = self.vocab_tuples[randomWordInt][0]
    activeWordClass = self.vocab_tuples[randomWordInt][1]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return
            
def DeactivateKeys():
    DISPLAYSURF.fill(PartsOfSpeechTeamGame.WHITE)

    text = font.render(activeWord, True, PartsOfSpeechTeamGame.BLACK)
    textpos = text.get_rect()
    textpos.centerx = DISPLAYSURF.get_rect().centerx
    textpos.y = self.yRes/4
    DISPLAYSURF.blit(text,textpos)

    RefreshDisplay()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return

def NewWord():
    global activeWord
    global activeWordClass
    randomWordInt = randint(0,len(self.vocab_tuples)-1)
    activeWord = self.vocab_tuples[randomWordInt][0]
    activeWordClass = self.vocab_tuples[randomWordInt][1]
    
    DISPLAYSURF.fill(PartsOfSpeechTeamGame.WHITE)

    text = font.render(activeWord, True, PartsOfSpeechTeamGame.BLACK)
    textpos = text.get_rect()
    textpos.centerx = DISPLAYSURF.get_rect().centerx
    textpos.y = self.yRes/4
    DISPLAYSURF.blit(text,textpos)

    RefreshDisplay()

def team1ScoreUpdate(score):
    global team1Score
    global self.team_1_name
    global self.winning_score
    team1Score += score
    if team1Score < 0:
        team1Score = 0
    if team1Score >= self.winning_score:
        GameOver(self.team_1_name)

def team2ScoreUpdate(score):
    global team2Score
    global self.team_2_name
    global self.winning_score
    team2Score += score
    if team2Score < 0:
        team2Score = 0
    if team2Score >= self.winning_score:
        GameOver(self.team_2_name)

def team3ScoreUpdate(score):
    global team3Score
    global self.team_3_name
    global self.winning_score
    team3Score += score
    if team3Score < 0:
        team3Score = 0
    if team3Score >= self.winning_score:
        GameOver(self.team_3_name)

def team4ScoreUpdate(score):
    global team4Score
    global self.team_4_name
    global self.winning_score
    team4Score += score
    if team4Score < 0:
        team4Score = 0
    if team4Score >= self.winning_score:
        GameOver(self.team_4_name)

def team5ScoreUpdate(score):
    global team5Score
    global self.team_5_name
    global self.winning_score
    team5Score += score
    if team5Score < 0:
        team5Score = 0
    if team5Score >= self.winning_score:
        GameOver(self.team_5_name)

def team6ScoreUpdate(score):
    global team6Score
    global self.team_6_name
    global self.winning_score
    team6Score += score
    if team6Score < 0:
        team6Score = 0
    if team6Score >= self.winning_score:
        GameOver(self.team_6_name)

keybindingsdict = {pygame.K_a:team1ScoreUpdate,
                   pygame.K_e:team2ScoreUpdate,
                   pygame.K_i:team3ScoreUpdate,
                   pygame.K_m:team4ScoreUpdate,
                   pygame.K_q:team5ScoreUpdate,
                   pygame.K_u:team6ScoreUpdate,
                   pygame.K_b:team1ScoreUpdate,
                   pygame.K_f:team2ScoreUpdate,
                   pygame.K_j:team3ScoreUpdate,
                   pygame.K_n:team4ScoreUpdate,
                   pygame.K_r:team5ScoreUpdate,
                   pygame.K_v:team6ScoreUpdate,
                   pygame.K_c:team1ScoreUpdate,
                   pygame.K_g:team2ScoreUpdate,
                   pygame.K_k:team3ScoreUpdate,
                   pygame.K_o:team4ScoreUpdate,
                   pygame.K_s:team5ScoreUpdate,
                   pygame.K_w:team6ScoreUpdate}

#display prep



RefreshDisplay()

#main loop

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                NewWord()
            if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
                if activeWordClass == 'adj':
                    keybindingsdict[event.key](self.points_per_question)
                    DeactivateKeys()#alter as needed to affect classroom speed, use time.sleep if needed
                else:
                    keybindingsdict[event.key](-self.points_per_question)
                    DeactivateKeys()
            if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
                if activeWordClass == 'noun':
                    keybindingsdict[event.key](self.points_per_question)
                    DeactivateKeys()
                else:
                    keybindingsdict[event.key](-self.points_per_question)
                    DeactivateKeys()
            if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
                if activeWordClass == 'verb':
                    keybindingsdict[event.key](self.points_per_question)
                    DeactivateKeys()
                else:
                    keybindingsdict[event.key](-self.points_per_question)
                    DeactivateKeys()

    pygame.display.update()
