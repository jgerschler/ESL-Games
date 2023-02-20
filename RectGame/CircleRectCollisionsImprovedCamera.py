import pygame
from pygame.locals import *
import imutils
import cv2
import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(0)

words_dict = {"eat":"verb", "talk":"verb",
              "red":"adjective", "nice":"adjective"}

sound_shot = pygame.mixer.Sound('audio\\shot.ogg')

shot_dict = {}

score_font = pygame.font.Font(None, 32)

score = 0
countdown = 30

Surface = pygame.display.set_mode((800,600))

display_width, display_height = pygame.display.get_surface().get_size()

left_border = (display_height/display_width) * 0.02 * display_width
right_border = (display_width -
                (display_height/display_width) * 0.02 * display_width)
top_border = 0.02 * display_height
bottom_border = 0.98 * display_height

circle_radius = 40
center_width = display_width/2
center_height = display_height/2

PRETTY_BLUE = (255, 0, 0)
BLUE = (0, 162, 232)

Words = []

rect1 = pygame.Rect(center_width-circle_radius, center_height-circle_radius, 2*circle_radius, 2*circle_radius)

class Word:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.word = random.choice(list(words_dict.keys()))
        self.rendered_word = self.font.render(self.word, 1, (255,100,0))
        self.rect = self.rendered_word.get_rect()
        self.x = random.randint(left_border + self.rect.width,
                                right_border - self.rect.width)
        self.y = random.randint(top_border + self.rect.height,
                                bottom_border - self.rect.height)
        self.speedx = 0.5*(random.random()+0.01)
        self.speedy = 0.5*(random.random()+0.01)
        self.shrink_level = 1
        
    def shrink(self):
        if self.shrink_level == 1:
            self.font = pygame.font.Font(None, 32)
            self.rendered_word = self.font.render(self.word, 1, (255,255,000))
            self.shrink_level = 2
            self.speedx+=0.2
            self.speedy+=0.2
        elif self.shrink_level == 2:
            self.font = pygame.font.Font(None, 16)
            self.rendered_word = self.font.render(self.word, 1, (255,0,0))
            self.shrink_level = 3
        else:
            del(Words[Words.index(self)])

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
        
def CollisionDetect():
    for Word in Words:
        if ((Word.x < left_border + Word.rect.width / 2) or
            (Word.x > right_border - Word.rect.width / 2)):
            Word.speedx *= -1            
        if (Word.y < top_border + Word.rect.height / 2 or
            Word.y > bottom_border - Word.rect.height / 2):
            Word.speedy *= -1
        if Word.rect.colliderect(rect1):
            if abs(rect1.top - Word.rect.bottom) < 10 and Word.speedy > 0:
                Word.speedy *= -1
            if abs(rect1.bottom - Word.rect.top) < 10 and Word.speedy < 0:
                Word.speedy *= -1
            if abs(rect1.right - Word.rect.left) < 10 and Word.speedx < 0:
                Word.speedx *= -1
            if abs(rect1.left - Word.rect.right) < 10 and Word.speedx > 0:
                Word.speedx *= -1
    
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
    # draw tracking circle
    pygame.draw.circle(Surface, BLUE, (center_width, center_height), circle_radius)
    #pygame.draw.rect(Surface, BLUE, rect1)
    

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
    pygame.display.update()
    
def GetInput():
    global score
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for Word in Words:
                if Word.rect.collidepoint(mouse_x, mouse_y):
                    Word.shrink()
                    sound_shot.play()
                    #del(Words[Words.index(Word)])
                    if words_dict[Word.word] == "verb":
                        score += 1
                    else:
                        score -= 1
                                                      
def main():
    camera = cv2.VideoCapture(0)# change 1 to 0 if you only have one camera
    object_lower = (94, 126, 129)# HSV color range for object to be tracked
    object_upper = (131, 255, 255)
    start_ticks = pygame.time.get_ticks()
    while True:

        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=display_width)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, object_lower, object_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            mouse_x, mouse_y = display_width - int(x), display_height - int(y)
            # if radius > 10:# left here for troubleshooting purposes
                # cv2.circle(frame, (int_x, int_y), int(radius), (0, 255, 255), 2)
        # cv2.imshow("Frame", frame)
        
        GetInput()
        Move()
        CollisionDetect()
        secs_remaining = (countdown -
                          (pygame.time.get_ticks() - start_ticks) / 1000)
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        
        #Draw(mouse_x, mouse_y, secs_remaining)
        if secs_remaining == 0:
            pygame.quit()
            sys.exit()
            
if __name__ == '__main__': main()
