import pygame
from pygame.locals import *
import random, math, sys
pygame.init()

words_list = ["w1","w2","w3","w4","w5"]

Surface = pygame.display.set_mode((400,300))

Words = []
class Word:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.word = random.choice(words_list)
        self.rendered_word = self.font.render(self.word, 1, (100,100,255))
        self.rect = self.rendered_word.get_rect()
        self.x = random.randint(self.rect.width, 400-self.rect.width)
        self.y = random.randint(self.rect.height, 300-self.rect.height)
        self.speedx = 0.1*(random.random()+0.1)
        self.speedy = 0.1*(random.random()+0.1)

for x in range(5):
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
def CollisionDetect():#currently treated as circles--fix this!
    for Word in Words:
        if Word.x < Word.rect.width or Word.x > 400-Word.rect.width:    Word.speedx *= -1
        if Word.y < Word.rect.height or Word.y > 300-Word.rect.height:    Word.speedy *= -1
    for Word in Words:
        for Word2 in Words:
            if Word != Word2:
                if math.sqrt(  ((Word.x-Word2.x)**2)  +  ((Word.y-Word2.y)**2)  ) <= (Word.rect.width+Word2.rect.width):
                    WordCollide(Word,Word2)
def Draw():
    Surface.fill((25,0,0))
    for Word in Words:
        Word.rect.topright = (Word.x, Word.y)
        Surface.blit(Word.rendered_word, Word.rect)
    pygame.display.update()
def GetInput():
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit(); sys.exit()
def main():
    while True:
        GetInput()
        Move()
        CollisionDetect()
        Draw()
if __name__ == '__main__': main()
