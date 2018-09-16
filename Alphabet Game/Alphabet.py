import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)
YELLOW = (230,230,0)
RED = (255,0,0)
BLUE = (0,0,255)
BROWN = (97,65,38)

soundwinfile = "audio\\ping.ogg"
soundlossfile = "audio\\buzzer.ogg"

finished = False

constructed_sentence = ''
points = 0
game_time = 60
previous_time = 0
time_remaining = 60
score = 0




def new_user():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    display.fill(WHITE)

    #display.blit(rendered_text, my_rect.topleft)

    pygame.display.update()


def refresh_screen(fragment):

    if frag0 == frag1 == frag2 == frag3 == "" and sentence == constructed_sentence:#winner!
        display.fill(WHITE)
        rendered_text = render_textrect(sentence, my_font, my_rect, GREEN, WHITE, 1)

        display.blit(rendered_text, my_rect.topleft)

        pygame.display.update()
        score += 1
        soundwin.play()
        time.sleep(0.5)
        frag0, frag1, frag2, frag3, sentence, constructed_sentence = new_user()

    elif frag0 == frag1 == frag2 == frag3 == "" and sentence != constructed_sentence:#loser
        display.fill(WHITE)
        rendered_text = render_textrect(constructed_sentence, my_font, my_rect, RED, WHITE, 1)

        display.blit(rendered_text, my_rect.topleft)

        pygame.display.update()
        score -= 1
        soundloss.play()
        time.sleep(0.5)
        frag0, frag1, frag2, frag3, sentence, constructed_sentence = new_user()

    display.fill(WHITE)
    rendered_text = render_textrect(constructed_sentence, my_font, my_rect, BLACK, WHITE, 1)

    display.blit(rendered_text, my_rect.topleft)

    pygame.display.update()

    return


pygame.init()
pygame.mixer.init()

soundwin = pygame.mixer.Sound(soundwinfile)
soundloss = pygame.mixer.Sound(soundlossfile)

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_width = display.get_width()
display_height = display.get_height()

my_font = pygame.font.Font(None, 48)
my_rect = pygame.Rect((20, 50, display_width - 20, 388))
rect_score = pygame.Rect((display_width - 50, 50, 50, 50))
rect_time = pygame.Rect((display_width - 50, 0, 50, 50))

display.fill(WHITE)

pygame.display.update()

clock = pygame.time.Clock()

while not finished:
    if pygame.time.get_ticks() - previous_time >= 1000:
        previous_time = pygame.time.get_ticks()
        time_remaining -= 1
        if time_remaining == 0:
            display.fill(WHITE)
            score_text = my_font.render("SCORE: " + str(score), 1, (148, 0, 201))
            display.blit(score_text, (display_width / 2, display_height / 2))
            pygame.display.update()
            time.sleep(5)
            finished = True
    time_text = my_font.render(str(time_remaining), 1, (148, 0, 201))
    score_text = my_font.render(str(score), 1, (255, 0, 0))
    display.fill(WHITE, rect_time)
    display.fill(WHITE, rect_score)
    display.blit(time_text, rect_time)
    display.blit(score_text, rect_score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                frag0, frag1, frag2, frag3, sentence, constructed_sentence = new_user()
            if event.key in (pygame.K_a,pygame.K_e,pygame.K_i,pygame.K_m,pygame.K_q,pygame.K_u):
                if frag0 != "":
                    refresh_screen(frag0)
                else:
                    pass
            if event.key in (pygame.K_b,pygame.K_f,pygame.K_j,pygame.K_n,pygame.K_r,pygame.K_v):
                if frag1 != "":
                    refresh_screen(frag1)
                else:
                    pass
            if event.key in (pygame.K_c,pygame.K_g,pygame.K_k,pygame.K_o,pygame.K_s,pygame.K_w):
                if frag2 != "":
                    refresh_screen(frag2)
                else:
                    pass
            if event.key in (pygame.K_d,pygame.K_h,pygame.K_l,pygame.K_p,pygame.K_t,pygame.K_x):
                if frag3 != "":
                    refresh_screen(frag3)
                else:
                    pass

    clock.tick(30)        
    pygame.display.update()

pygame.quit()
