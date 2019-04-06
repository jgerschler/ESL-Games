import imutils
import cv2
import random
import sys
import numpy as np
from math import atan2, cos, sin, sqrt, pi

color_blue = (0,162,232)
object_lower = (94, 126, 129)
object_upper = (131, 255, 255)

def getOrientation(pts, img):
    
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i,0] = pts[i,0,0]
        data_pts[i,1] = pts[i,0,1]
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    cntr = (int(mean[0,0]), int(mean[0,1]))
    
    
    cv2.circle(img, cntr, 3, (255, 0, 255), 2)
    cv2.circle(img, (640-cntr[0], 480-cntr[1]), 4, (0,0,255), 2)
    p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
    p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
    print(cntr)
    cv2.line(img, cntr, (int(p1[0]),int(p1[1])), (0, 255, 0), 1)
    cv2.line(img, cntr, (int(p2[0]),int(p2[1])), (255, 255, 0), 1)
    angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    
    return angle

src = cv2.imread("test.png")

cv2.imshow('src', src)
#gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)# not gray!
mask = cv2.inRange(gray, object_lower, object_upper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
#ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
for i, c in enumerate(contours):
    area = cv2.contourArea(c);
    if area < 1e2:
        continue
    cv2.drawContours(src, contours, i, (0, 0, 255), 2)
    getOrientation(c, src)
cv2.imshow('output', src)
cv2.waitKey()


##            frame = imutils.resize(frame, width=self.display_width)
##            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
##
##            mask = cv2.inRange(hsv, self.object_lower, self.object_upper)
##            mask = cv2.erode(mask, None, iterations=2)
##            mask = cv2.dilate(mask, None, iterations=2)
##
##            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
##            if len(cnts) > 0:
##                c = max(cnts, key=cv2.contourArea)
##                ((x, y), radius) = cv2.minEnclosingCircle(c)
##                int_x, int_y = self.display_width - int(x), self.display_height - int(y)
