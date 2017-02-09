from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pygame
import time

pygame.init()

display_width = 600
display_height = 450

black = (0,0,0)
white = (255,255,255)

finished = False

greenLower = (24, 162, 73)
greenUpper = (35, 255, 231)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pixel Tracker')
gameDisplay.fill(white)
pygame.display.update()

camera = cv2.VideoCapture(0)

while not finished:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        # center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                # M = cv2.moments(c)
                # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        # print int(x), int(y)
                        # centroid
                        # cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    finished = True
        # time.sleep(0.1)
        gameDisplay.fill(white)
        try:
            pygame.draw.circle(gameDisplay,black,(int(x),int(y)),10)
        except:
            pass
        pygame.display.update()

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
