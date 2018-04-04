import pygame
import random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('crosshair.png')
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def shoot(self, target):
        hitbox = self.rect.inflate(-5, -5)
        return hitbox.colliderect(target.rect), target.rect.center

class Star(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('star.png')
        self.rect = self.image.get_rect()
        
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 200, 100

    def update(self):
        newpos = self.rect.move((0, 1))
        if (self.rect.top < self.area.top or
            self.rect.bottom > self.area.bottom):
            self.rect.topleft = 200, 100
            newpos = self.rect.move((0, 1))
        self.rect = newpos


screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

pygame.display.set_caption('Star Shooter')
pygame.mouse.set_visible(0)
crosshair = Crosshair()
clock = pygame.time.Clock()

def main():

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption('Star Shooter')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

###Put Text On The Background, Centered
##    if pygame.font:
##        font = pygame.font.Font(None, 36)
##        text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
##        textpos = text.get_rect(centerx=background.get_width()/2)
##        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.display.update()

    clock = pygame.time.Clock()
    laser_sound = pygame.mixer.Sound('laser.ogg')
    explosion_sound = pygame.mixer.Sound('explosion.ogg')
    explosion_image = pygame.image.load('explosion.png')
    star = Star()
    crosshair = Crosshair()
    allsprites = pygame.sprite.RenderPlain((star, crosshair))

    going = True
    while going:
        clock.tick(30)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                outcome, pos = crosshair.shoot(star)
                if outcome:
                    explosion_sound.play()
                    screen.blit(explosion_image, (pos[0] - 120, pos[1] - 120))
                    pygame.display.update()
                    pygame.time.delay(300)
                else:
                    laser_sound.play()

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
