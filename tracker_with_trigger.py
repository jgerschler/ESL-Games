from collections import deque
from pygame.locals import *
import numpy as np
import argparse, imutils, cv2, pygame, time

pygame.init()
pygame.mixer.init()

sound_shot = pygame.mixer.Sound('audio\\shot.ogg')

display_width = 600
display_height = 450

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

finished = False

objectLower = (0, 112, 208)
objectUpper = (19, 255, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Object Tracker')
gameDisplay.fill(white)
pygame.display.update()

camera = cv2.VideoCapture(0)

while not finished:
    (grabbed, frame) = camera.read()

    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, objectLower, objectUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        int_x, int_y = int(x), int(y)
        if radius > 10:
            # draw the circle and centroid on the frame,
            cv2.circle(frame, (int_x, int_y), int(radius), (0, 255, 255), 2)
            # print int(x), int(y)
            # centroid:
            # cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    # key = cv2.waitKey(1) & 0xFF

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONUP:
            sound_shot.play()
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, (280, 210, 40, 30), 2)
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
