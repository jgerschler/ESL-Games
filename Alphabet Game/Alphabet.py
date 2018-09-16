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
    sentence_list = ["My hair is longer than your hair.", "Oxford is more beautiful than Birmingham.",
                     "I’m taller than you.", "People are more intelligent than animals.",
                     "Barcelona is bigger than Santander.", "Bikes are cheaper than cars.",
                     "Pedro is taller than Maggie", "Antonia is noisier than Gemma.",
                     "Laura is more beautiful than Jane.", "Radios are cheaper than TVs.",
                     "Buses are longer than cars.", "Carlos is taller than Sergio. ",
                     "London is bigger than Madrid. ", "Cats are more intelligent than rabbits.",
                     "MP3 players are cheaper than laptops. ", "I’m more beautiful than you. ",
                     "The skateboard is worse than the mobile phone.",
                     "The computer is quieter than the mobile phone.",
                     "The mobile phone is better than the skateboard.",
                     "The computer is bigger than the mobile phone.", "The Nile is the longest river.",
                     "Cheetahs are the fastest animals.", "Sharks are the most dangerous animals.",
                     "Chihuahuas are the smallest dogs.", "A “10” exam result is the best result.",
                     "Madrid is the biggest city in Spain.", "Dolphins are the most intelligent animals.",
                     "The Rolls Royce is the most expensive car.",
                     "The teacher is the oldest person in the class.",
                     "Champagne is the most expensive drink.", "Russia is the biggest country.",
                     "A “0” exam result is the worst result.", "Pau Gasol is the tallest Spanish player.",
                     "Antartica is the windiest place in the world.",
                     "Lake Baikal is the deepest lake in the world.",
                     "Yakutsk, Russia is the coldest city in the world.",
                     "The Nile is the longest river in the world.",
                     "Bangkok, Thailand is the hottest city in the world.",
                     "Río de la Plata is the widest river in the world.",
                     "Mount Everest is the highest mountain in the world."]
    
    constructed_sentence = ""
    sentence = random.choice(sentence_list)
    fragmentlist = sentence_gen(sentence)
    frag0 = fragmentlist[0]
    frag1 = fragmentlist[1]
    frag2 = fragmentlist[2]
    frag3 = fragmentlist[3]

    display.fill(WHITE)
    #rendered_text = render_textrect(sentenceunderline, my_font, my_rect, BLACK, WHITE, 1)
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

    #display.blit(rendered_text, my_rect.topleft)
    display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
    display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
    display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
    display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

    pygame.display.update()

    return frag0, frag1, frag2, frag3, sentence, constructed_sentence

def refresh_screen(fragment):
    global sentence
    global constructed_sentence
    global frag0
    global frag1
    global frag2
    global frag3
    global score
    global time_remaining

    if constructed_sentence == "":
        constructed_sentence = constructed_sentence + fragment
    else:
        constructed_sentence = constructed_sentence + " " + fragment

    if fragment == frag0:
        frag0 = ""
    elif fragment == frag1:
        frag1 = ""
    elif fragment == frag2:
        frag2 = ""
    elif fragment == frag3:
        frag3 = ""

    if frag0 == frag1 == frag2 == frag3 == "" and sentence == constructed_sentence:#winner!
        display.fill(WHITE)
        rendered_text = render_textrect(sentence, my_font, my_rect, GREEN, WHITE, 1)
        rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
        rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
        rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
        rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

        display.blit(rendered_text, my_rect.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

        pygame.display.update()
        score += 1
        soundwin.play()
        time.sleep(0.5)
        frag0, frag1, frag2, frag3, sentence, constructed_sentence = new_user()

    elif frag0 == frag1 == frag2 == frag3 == "" and sentence != constructed_sentence:#loser
        display.fill(WHITE)
        rendered_text = render_textrect(constructed_sentence, my_font, my_rect, RED, WHITE, 1)
        rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
        rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
        rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
        rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

        display.blit(rendered_text, my_rect.topleft)
        display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
        display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
        display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
        display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

        pygame.display.update()
        score -= 1
        soundloss.play()
        time.sleep(0.5)
        frag0, frag1, frag2, frag3, sentence, constructed_sentence = new_user()

    display.fill(WHITE)
    rendered_text = render_textrect(constructed_sentence, my_font, my_rect, BLACK, WHITE, 1)
    rendered_text_frag_1 = render_textrect(frag0, my_font, my_rect_frag_1, RED, WHITE, 0)
    rendered_text_frag_2 = render_textrect(frag1, my_font, my_rect_frag_2, YELLOW, WHITE, 0)
    rendered_text_frag_3 = render_textrect(frag2, my_font, my_rect_frag_3, GREEN, WHITE, 0)
    rendered_text_frag_4 = render_textrect(frag3, my_font, my_rect_frag_4, BLUE, WHITE, 0)

    display.blit(rendered_text, my_rect.topleft)
    display.blit(rendered_text_frag_1, my_rect_frag_1.topleft)
    display.blit(rendered_text_frag_2, my_rect_frag_2.topleft)
    display.blit(rendered_text_frag_3, my_rect_frag_3.topleft)
    display.blit(rendered_text_frag_4, my_rect_frag_4.topleft)

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
my_rect_frag_1 = pygame.Rect((20, display_height - 200, display_width - 20, 50))
my_rect_frag_2 = pygame.Rect((20, display_height - 150, display_width - 20, 50))
my_rect_frag_3 = pygame.Rect((20, display_height - 100, display_width - 20, 50))
my_rect_frag_4 = pygame.Rect((20, display_height - 50, display_width - 20, 50))
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
