#Burger-Dog
import random

import pygame

#initialize pygame
pygame.init()

#game constants
GAME_FOLDER = 'd:/burger_dog/'

WINDOW_WIDHT = 1300
WINDOW_HEIGHT = 700

FPS = 60

BLACK = pygame.Color(0,0,0)
ORANGE = pygame.Color(255,157,60)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)

DOG_VELOCITY = 10
MAX_BOOST = 25

DEFAULT_BURGER_VELOCITY = 5
INCREASED_BURGER_VELOCITY = 0.25
BUFFER_DISTANCE = -200

MAX_LIVES = 5
DEAULT_SCORE = 0

#create the window
display_surface = pygame.display.set_mode((WINDOW_WIDHT,WINDOW_HEIGHT))
pygame.display.set_caption('Burger Dog')

#assets
left_dog = pygame.image.load(GAME_FOLDER + 'dog.png')
right_dog = pygame.transform.flip(left_dog, flip_x= True, flip_y=False)
dog = right_dog
dog_rect = dog.get_rect()
dog_rect.bottom = WINDOW_HEIGHT
dog_rect.centerx = WINDOW_WIDHT//2

burger = pygame.image.load(GAME_FOLDER + 'burger.png')
burger_rect = burger.get_rect()
burger_rect.top = BUFFER_DISTANCE
burger_rect.left = random.randint(0, WINDOW_WIDHT- burger_rect.width)

#font
game_font_big  = pygame.font.Font(GAME_FOLDER+ 'SunnyspellsRegular.otf', 60)
game_font  = pygame.font.Font(GAME_FOLDER+ 'SunnyspellsRegular.otf', 40)


#sounds
woof = pygame.mixer.Sound(GAME_FOLDER + 'woof.mp3')
woof.set_volume(0.2)
loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
pygame.mixer.music.load(GAME_FOLDER + 'instrumental.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#game values
current_burger_velocity = DEFAULT_BURGER_VELOCITY
current_dog_velocity = DOG_VELOCITY
booster = MAX_BOOST
score = DEAULT_SCORE
lives = MAX_LIVES
game_status = 1

#generate texts
game_title = game_font_big.render('Burger-Dog', True, ORANGE)
game_title_rect = game_title.get_rect()
game_title_rect.centerx = WINDOW_WIDHT//2
game_title_rect.top = 10

game_score = game_font.render('Score: '+ str(score), True, ORANGE)
game_score_rect = game_score.get_rect()
game_score_rect.left = 50
game_score_rect.top= 10

game_lives = game_font.render('Lives: '+ str(lives), True, ORANGE)
game_lives_rect = game_lives.get_rect()
game_lives_rect.right = WINDOW_WIDHT-50
game_lives_rect.top = 10

game_ends = game_font_big.render('GAME OVER!!!', True, RED)
game_ends_rect = game_ends.get_rect()
game_ends_rect.center = (WINDOW_WIDHT//2, WINDOW_HEIGHT//2)

game_restart = game_font.render('Press r to restart!!!', True, GREEN)
game_restart_rect = game_restart.get_rect()
game_restart_rect.center = (WINDOW_WIDHT//2, WINDOW_HEIGHT//2 +60)


#main game loop (defines the life of the games)
clock = pygame.time.Clock()
running = True
while running:
    # erase the window, so that everything can be redrawn afresh
    display_surface.fill(BLACK)

    #read the events (object that represents user-action)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False


    #know to the key's pressed
    keys = pygame.key.get_pressed()
    if game_status == 1:
        if keys[pygame.K_LEFT]:
            dog = left_dog
            if dog_rect.left >= 0:
                dog_rect.left -= current_dog_velocity
        if keys[pygame.K_RIGHT]:
            dog = right_dog
            if dog_rect.right <= WINDOW_WIDHT:
                dog_rect.left += current_dog_velocity
        if keys[pygame.K_UP]:
            if dog_rect.top >= 0:
                dog_rect.top -= current_dog_velocity
        if keys[pygame.K_DOWN]:
            if dog_rect.bottom <= WINDOW_HEIGHT:
                dog_rect.top += current_dog_velocity

        if keys[pygame.K_SPACE]:
            current_dog_velocity+= booster
            booster = 0

        #burger movement
        burger_rect.top += current_burger_velocity

        #catch the  burger
        if dog_rect.colliderect(burger_rect):
            burger_rect.top = BUFFER_DISTANCE
            burger_rect.left = random.randint(0, WINDOW_WIDHT - burger_rect.width)
            current_burger_velocity += INCREASED_BURGER_VELOCITY
            if booster < MAX_BOOST:
                booster+=5
            woof.play()
            score += (WINDOW_HEIGHT - dog_rect.top)
            game_score = game_font.render('Score: ' + str(score), True, ORANGE)

        #uncaught burger
        elif burger_rect.bottom > WINDOW_HEIGHT:
            burger_rect.top = BUFFER_DISTANCE
            burger_rect.left = random.randint(0, WINDOW_WIDHT-burger_rect.width)
            current_burger_velocity = DEFAULT_BURGER_VELOCITY
            loss.play()
            lives -=1
            game_lives = game_font.render('Lives: ' +str(lives), True, ORANGE)
            if lives == 0:
                game_status = 2
                pygame.mixer.music.stop()

        #loss in boost
        if current_dog_velocity > DOG_VELOCITY:
            current_dog_velocity -= 0.1

        # draw the assets
        display_surface.blit(dog, dog_rect)
        display_surface.blit(burger, burger_rect)


    elif game_status == 2:
        display_surface.blit(game_ends, game_ends_rect)
        display_surface.blit(game_restart, game_restart_rect)
        if keys[pygame.K_r]:
            #restart
            game_status = 1

            dog_rect.centerx = WINDOW_WIDHT//2
            dog_rect.bottom = WINDOW_HEIGHT

            burger_rect.top = BUFFER_DISTANCE
            burger_rect.left = random.randint(0, WINDOW_WIDHT - burger_rect.width)

            score = DEAULT_SCORE
            game_score = game_font.render('Score: ' + str(score), True, ORANGE)

            lives = MAX_LIVES
            game_lives = game_font.render('Lives: ' + str(lives), True, ORANGE)

            booster = MAX_BOOST
            current_burger_velocity = DEFAULT_BURGER_VELOCITY
            current_dog_velocity = DOG_VELOCITY

            pygame.mixer.music.play(-1)

    #blit the hud
    display_surface.blit(game_title, game_title_rect)
    display_surface.blit(game_score, game_score_rect)
    display_surface.blit(game_lives, game_lives_rect)


    #refesh the display
    pygame.display.update()

    #to moderate the rate of iteration (cooperative multitasking)
    #game runs at the same speed across different CPU's
    clock.tick(FPS)

#quit pygame
pygame.quit()
