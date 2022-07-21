import pygame
import sys
import time
import random
from pygame import mixer
speed = 10

# windows sizes
frame_size_x = 1380
frame_size_y = 840
check_errors = pygame.init()

if(check_errors[1] > 0):
    print("Error " + check_errors[1])
else:
    print("Game Succesfully initialized")

# initialise game window
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors
snake_color = (242, 242, 242)
food_color = (242, 183, 5)
white = (255, 255, 255)
bgcol = (38, 38, 38)
pause_bg = (21, 21, 21)
black = (0, 0, 0)
red = (255, 0, 0)
font = pygame.font.SysFont('Arial', 40)
white_image = pygame.image.load("white.png")
black_image = pygame.image.load('black.png')

# Text
font_pause = pygame.font.Font("font.ttf", 70)
resume_text = font_pause.render("resume", False, 'black')
resume_alt_text = font_pause.render("resume", False, 'orange')
exit_text = font_pause.render("exit", False, 'black')
exit_alt_text = font_pause.render("exit", False, 'red')

#background image, if is needed can change with other image whith name 'bg.png'
bg = pygame.image.load("bg.png")
# bg = pygame.image.load("100.jpg")

fps_controller = pygame.time.Clock()

# one snake square size
square_size = 30
score = 0 
#Playlist, can modify to add the music that you need
# play_list=[]
# play_list.append("resources/01.mp3")
# play_list.append("resources/02.mp3")
# play_list.append("resources/03.mp3")
# play_list.append("resources/04.mp3")
# songnum=1

# def play_toonz(play_list):
#     random.shuffle(play_list)
#     pygame.mixer.music.load(play_list[songnum])
#     pygame.mixer.music.play(10)
#     for num, song in enumerate(play_list):
#         if num == songnum:
#             continue
#         pygame.mixer.music.queue(song)
# a function that draw the score in the game window

def show_score(choice, color, font, size):
    score_font = pygame.font.Font('Pcoleco.otf', 40)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        gameover_font = pygame.font.Font('font.ttf', 90)
        game_over_surface = gameover_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

#function that reproduces sound effects
def play_sound(sound):
    point = mixer.Sound("resources/Point.wav")
    crash = mixer.Sound("resources/crash.wav")
    if sound == 0:
        mixer.Sound.play(crash)
    if sound == 1:
        mixer.Sound.play(point)

#function to initialize the variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, fps_controller, direction, gameover
    gameover = False
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True

#define a interactive pause menu
def paused():
    loop = 1
    # Transparent White Layer
    white = pygame.transform.scale(white_image, (frame_size_x, frame_size_y))
    white.set_colorkey('black')
    white.set_alpha(100)
    game_window.blit(white, (0, 0))
    while loop:
        if gameover == 0:  # fix the overlay into the gameover screen and pause
            mixer.music.pause()
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            # Resume Button
            resume_rect = pygame.Rect(
                frame_size_x-resume_text.get_width()-5, 5, resume_text.get_width(), resume_text.get_height())
            game_window.blit(resume_text, (resume_rect.x, resume_rect.y))
            
            if resume_rect.collidepoint(mouse_pos):
                # changing the color of the text
                resume_rect = pygame.Rect(frame_size_x-resume_alt_text.get_width(
                )-5, 5, resume_alt_text.get_width(), resume_alt_text.get_height())
                game_window.blit(resume_alt_text, (resume_rect.x, resume_rect.y))
                
                if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                    loop = 0
                    clicked = True
                    mixer.music.unpause()

            if pygame.mouse.get_pressed()[0] == 0:
                clicked = False
                
            # Exit Button
            exit_rect = pygame.Rect(frame_size_x-exit_text.get_width(
            )-5, resume_text.get_height()+10, exit_text.get_width(), exit_text.get_height())
            
            game_window.blit(exit_text, (exit_rect.x, exit_rect.y))
            
            # Exit Button Clicking Function
            if exit_rect.collidepoint(mouse_pos):
                exit_rect = pygame.Rect(frame_size_x-exit_alt_text.get_width(
                )-5, resume_text.get_height()+10, exit_alt_text.get_width(), exit_alt_text.get_height())
                
                game_window.blit(exit_alt_text, (exit_rect.x, exit_rect.y))
                
                if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    pygame.quit()
                    sys.exit()
                    
            if pygame.mouse.get_pressed()[0] == 0:
                clicked = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = 0
                        mixer.music.unpause()
            pygame.display.update()
            fps_controller.tick(60)

#define the principal parts of the game
def game_intro():
    pygame
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    intro = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #represent the title in the middle
        menu_image=pygame.image.load('menu.png')
        game_window.blit(menu_image,(0,0))
        intro_font = pygame.font.Font('font.ttf', 90)
        intro_txt_color=(255,220,100)
        intro_surface = intro_font.render('Snake Game', True, intro_txt_color)
        intro_rect = intro_surface.get_rect()
        intro_rect.midtop = (frame_size_x/2, frame_size_y/2+100)
        game_window.blit(intro_surface, intro_rect)
        #represent the sub title
        option_surface = font.render('Press any key to start', True, intro_txt_color)
        option_rect = option_surface.get_rect()
        option_rect.midtop = (frame_size_x/2, frame_size_y/2+250)
        game_window.blit(option_surface, option_rect)
        #screen update
        pygame.display.update()
        fps_controller.tick(15)
def game_loop():
    global head_pos, snake_body, food_pos, food_spawn, fps_controller, direction, gameover, running, score
    # play_toonz(play_list)
    running=True
    while running:
        #if the gameover flag is down
        if not gameover:
            #recognize all movement possibilities
            if direction == "UP":
                head_pos[1] -= square_size
            elif direction == "DOWN":
                head_pos[1] += square_size
            elif direction == "LEFT":
                head_pos[0] -= square_size
            else:
                head_pos[0] += square_size
            #conditions that allows the no-walls condition in the game
            if head_pos[0] < 0:
                head_pos[0] = frame_size_x - square_size
            elif head_pos[0] > frame_size_x - square_size:
                head_pos[0] = 0
            elif head_pos[1] < 0:
                head_pos[1] = frame_size_y - square_size
            elif head_pos[1] > frame_size_y - square_size:
                head_pos[1] = 0
            # eating apple
            snake_body.insert(0, list(head_pos))
            if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
                score += 1
                food_spawn = False
                play_sound(1)
            else:
                snake_body.pop()
            # spawn food in a random place
            if not food_spawn:
                #note: the floor division // rounds the result down to the nearest whole number
                food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                            random.randrange(1, (frame_size_y // square_size)) * square_size]
                food_spawn = True

            # food and snake screen draw
            game_window.blit(bg, (0, 0))
            for pos in snake_body:
                pygame.draw.rect(game_window, snake_color, pygame.Rect(
                    pos[0] + 2, pos[1] + 2, square_size - 2, square_size - 2))
            pygame.draw.rect(game_window, food_color, pygame.Rect(
                food_pos[0], food_pos[1], square_size, square_size))

            # game over condiditons
            for block in snake_body[1:]:
                if head_pos[0] == block[0] and head_pos[1] == block[1]:
                    gameover = True
                    play_sound(0)
                    mixer.music.stop()
                    #play_background_music(0)
            show_score(1, white, 'consolas', 30)
        else:
            show_score(0, red, 'Arial', 40)
            option_surface = font.render(
                'You lost! Press \'Q\' to quit, or Spacebar to play again', True, snake_color)
            option_rect = option_surface.get_rect()
            option_rect.midtop = (frame_size_x/2, frame_size_y/2+200)
            game_window.blit(option_surface, option_rect)
        pygame.display.update()
        fps_controller.tick(speed)

        # Event Loop
        # Get the next events from the queue
        # For each event returned from get(),
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == ord("w")
                        and direction != "DOWN"):
                    direction = "UP"
                if (event.key == pygame.K_DOWN or event.key == ord("s")
                        and direction != "UP"):
                    direction = "DOWN"
                if (event.key == pygame.K_LEFT or event.key == ord("a")
                        and direction != "RIGHT"):
                    direction = "LEFT"
                if (event.key == pygame.K_RIGHT or event.key == ord("d")
                        and direction != "LEFT"):
                    direction = "RIGHT"
                if (event.key == pygame.K_ESCAPE):
                    mixer.music.pause()
                    paused()
                if gameover == True:
                    if event.key == pygame.K_SPACE:
                        init_vars()
                        # play_toonz(play_list)
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
#call the init_vars function
init_vars()
#game loop
game_intro()
game_loop()