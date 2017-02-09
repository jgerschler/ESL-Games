from collections import deque
import numpy as np
import argparse, imutils, cv2, pygame, time

pygame.init()

display_width = 600
display_height = 450

black = (0,0,0)
white = (255,255,255)

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
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        # print int(x), int(y)
                        # centroid:
                        # cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    finished = True
        gameDisplay.fill(white)
        try:
            pygame.draw.circle(gameDisplay,black,(int(x),int(y)),10)
        except:
            pass
        pygame.display.update()

camera.release()
cv2.destroyAllWindows()
