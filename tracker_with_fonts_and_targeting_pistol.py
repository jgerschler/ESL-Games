from collections import deque
from pygame.locals import *
import numpy as np
import argparse, imutils, cv2, pygame, time, random

pygame.init()
pygame.mixer.init()

sound_shot = pygame.mixer.Sound('audio\\shot.ogg')

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

verbs = ['eat','walk','talk','run','speak','read','be','watch','see','hear','listen','allow','permit']
adjectives = ['red','green','blue','furry','hairy','happy']

finished = False

objectLower = (0, 112, 208)
objectUpper = (19, 255, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Object Tracker')
gameDisplay.fill(white)
pygame.display.update()

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def message_display(text, tuple_center):
    large_text = pygame.font.Font('arial.ttf',18)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = tuple_center
    gameDisplay.blit(text_surf, text_rect)

camera = cv2.VideoCapture(0)

while not finished:
    (grabbed, frame) = camera.read()

    frame = imutils.resize(frame, width=800)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, objectLower, objectUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        int_x, int_y = int(x), int(y)
        if radius > 10:
            cv2.circle(frame, (int_x, int_y), int(radius), (0, 255, 255), 2)
    cv2.imshow("Frame", frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONUP:
            sound_shot.play()
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, (280, 210, 40, 30), 2)
    message_display("cars", (50, 50))
    try:
        if 280 <= int_x <= 320 and 210 <= int_y <= 240:
            pygame.draw.circle(gameDisplay, red,(int_x, int_y), 10)
        else:
            pygame.draw.circle(gameDisplay, black,(int_x, int_y), 10)
    except:
        pass
    pygame.display.update()

camera.release()
cv2.destroyAllWindows()
