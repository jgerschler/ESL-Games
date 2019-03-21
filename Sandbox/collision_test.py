import math
import pygame

pygame.init()

Surface = pygame.display.set_mode((400,300))

##test_rect.topleft
##test_rect.topright
##test_rect.bottomleft
##test_rect.bottomright
##
##test_rect.top
##test_rect.bottom
##test_rect.left
##test_rect.right
##
##
##circle.x
##circle.y
##circle.radius

# logic tests

rect_edge_x = 0
rect_edge_y = 0

if circle.x < test_rect.left:
    rect_edge_x = test_rect.left
elif circle.x > test_rect.right:
    rect_edge_x = test_rect.right

if circle.y > test_rect.top:
    rect_edge_y = test_rect.top
elif circle.y < test_rect.bottom:
    rect_edge_y = test_rect.bottom

dist_x = circle.x - rect_edge_x
dist_y = circle.y - rect_edge_y
distance = math.sqrt( (dist_x * dist_x) + (dist_y * dist_y) )

if distance <= circle.radius:
    return True


