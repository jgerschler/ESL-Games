import pygame
from pygame.locals import *
import random, math, sys
pygame.init()
pygame.mouse.set_visible(0)

words_dict = {"eat":"verb", "talk":"verb",
              "red":"adjective", "nice":"adjective"}

shot_dict = {}

score_font = pygame.font.Font(None, 32)

score = 0
countdown = 30

Surface = pygame.display.set_mode((800,600))

display_width, display_height = pygame.display.get_surface().get_size()

left_border = (display_height/display_width) * 0.05 * display_width
right_border = (display_width -
                (display_height/display_width) * 0.05 * display_width)
top_border = 0.05 * display_height
bottom_border = 0.95 * display_height

PRETTY_BLUE = (0, 0, 128)
Words = []

class Word:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.word = random.choice(list(words_dict.keys()))
        self.rendered_word = self.font.render(self.word, 1, (100,100,255))
        self.rect = self.rendered_word.get_rect()
        self.x = random.randint(left_border + self.rect.width,
                                right_border - self.rect.width)
        self.y = random.randint(top_border + self.rect.height,
                                bottom_border - self.rect.height)
        self.speedx = 0.1*(random.random()+0.01)
        self.speedy = 0.1*(random.random()+0.01)
        self.shrink_level = 1
    def shrink(self):
        if self.shrink_level == 1:
            self.font = pygame.font.Font(None, 32)
            self.rendered_word = self.font.render(self.word, 1, (255,255,000))
            self.shrink_level = 2
        elif self.shrink_level == 2:
            self.font = pygame.font.Font(None, 16)
            self.rendered_word = self.font.render(self.word, 1, (255,0,0))
            self.shrink_level = 3
        else:
            del(Words[Words.index(self)])

for x in range(10):
    Words.append(Word())

def WordCollide(C1,C2):
    C1Speed = math.sqrt((C1.speedx**2)+(C1.speedy**2))
    XDiff = -(C1.x-C2.x)
    YDiff = -(C1.y-C2.y)
    if XDiff > 0:
        if YDiff > 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff < 0:
        if YDiff > 0:
            Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff == 0:
        if YDiff > 0:
            Angle = -90
        else:
            Angle = 90
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    elif YDiff == 0:
        if XDiff < 0:
            Angle = 0
        else:
            Angle = 180
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    C1.speedx = XSpeed
    C1.speedy = YSpeed
    
def Move():
    for Word in Words:
        Word.x += Word.speedx
        Word.y += Word.speedy
        
def CollisionDetect():
    for Word in Words:
        if (Word.x < left_border + Word.rect.width / 2 or
            Word.x > right_border - Word.rect.width / 2):
            Word.speedx *= -1
        if (Word.y < top_border + Word.rect.height / 2 or
            Word.y > bottom_border - Word.rect.height / 2):
            Word.speedy *= -1
    for Word in Words:
        for Word2 in Words:
            if Word != Word2:
                if ((Word.rect.x + Word.rect.width >= Word2.rect.x) and
                    (Word.rect.x <= Word2.rect.x + Word2.rect.w) and
                    (Word.rect.y + Word.rect.height >= Word2.rect.y) and
                    (Word.rect.y <= Word2.rect.y + Word2.rect.height)):
                    WordCollide(Word,Word2)
                    
def Draw(mouse_x, mouse_y, secs_remaining):
    Surface.fill((25,0,0))
    # draw tracking rects
    pygame.draw.rect(Surface, PRETTY_BLUE,
                     (0, 0, display_width, top_border), 0)
    pygame.draw.rect(Surface, PRETTY_BLUE,
                     (0, bottom_border,
                      display_width, 0.05 * display_height), 0)
    pygame.draw.rect(Surface, PRETTY_BLUE,
                     (0, 0, left_border,
                      display_height), 0)
    pygame.draw.rect(Surface, PRETTY_BLUE,
                     (right_border,
                      0,
                      left_border,
                      display_height), 0)
    # draw score
    rendered_score = score_font.render(str(score), 1, (255, 0, 0))
    rendered_score_rect = rendered_score.get_rect()
    rendered_score_rect.center = (right_border - rendered_score_rect.width / 2,
                                  bottom_border - rendered_score_rect.height / 2)
    Surface.blit(rendered_score, rendered_score_rect)
    # draw countdown
    rendered_countdown = score_font.render(str(int(secs_remaining)), 1, (255, 0, 0))
    rendered_countdown_rect = rendered_countdown.get_rect()
    rendered_countdown_rect.center = (left_border + rendered_countdown_rect.width / 2,
                                  bottom_border - rendered_countdown_rect.height / 2)
    Surface.blit(rendered_countdown, rendered_countdown_rect)    
    # draw words
    for Word in Words:
        Word.rect.center = (Word.x, Word.y)
        Surface.blit(Word.rendered_word, Word.rect)
    # draw cursor
    pygame.draw.circle(Surface, (128,128,128), (mouse_x, mouse_y), 10)
    # draw tracking circle
    pygame.draw.circle(Surface, (0,162,232), (int(display_width/2), int(display_height/2)), 40)
    pygame.display.update()
    
def GetInput():
    global score
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for Word in Words:
                if Word.rect.collidepoint(mouse_x, mouse_y):
                    Word.shrink()
                    #del(Words[Words.index(Word)])
                    if words_dict[Word.word] == "verb":
                        score += 1
                    else:
                        score -= 1
                                                      
def main():
    start_ticks = pygame.time.get_ticks()
    while True:
        GetInput()
        Move()
        CollisionDetect()
        secs_remaining = (countdown -
                          (pygame.time.get_ticks() - start_ticks) / 1000)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        Draw(mouse_x, mouse_y, secs_remaining)
        
if __name__ == '__main__': main()
