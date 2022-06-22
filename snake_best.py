import pygame
import random
from pygame import mixer
# Initialization
pygame.init()  # necessary to initialize the pygame library
font = pygame.font.SysFont('Arial', 40)

# Colours
blue = (0, 0, 255)  # hex code for blue
black = (0, 0, 0)  # hex code for black
red = (255, 0, 0)  # hex code for red
snake_color = (242,242,242)
food_color = (242,183,5)
white = (255, 255, 255)
bgcol=(38,38,38)
pause_bg = (21,21,21)
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the snake in the middle of the screen
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_speed = 15
snake_size = 10
snake_length = 4
snake_blocks = []

fruit_x = 300
fruit_y = 400

speed_x = 0
speed_y = 10

game_over = False
pause = False
running = True
clock = pygame.time.Clock()

# def color():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     rgb = [r,g,b]
#     return rgb

def paused():
    if game_over==0: #fix the overlay into the gameover screen and pause
        mixer.music.pause()
        loop = 1
        screen.fill(pause_bg)
        text = font.render('Game in pause, press esc to continue', False, red)    
        screen.blit(text, (320, screen_height / 2))
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = 0
                        mixer.music.unpause()
                    if event.key==pygame.K_q:
                        running=False        #bug
            pygame.display.update()
            # screen.fill((0, 0, 0))
            clock.tick(60)

def play_background_music():
        mixer.init()
        mixer.music.load('resources/music.mp3')
        mixer.music.play()
        
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(snake_length), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (screen_width/23, 15)
    else:
        score_rect.midtop = (screen_width/2, screen_height/1.25)
    screen.blit(score_surface, score_rect)
    # pygame.display.flip()
pygame.mixer.init()
play_background_music()
# While "running" is true (always true unless user quits):
while running:
    #random colors for food
    
    # If the user hasn't lost the game:
    if not game_over:
        screen.fill(bgcol)
        # Set the snake head to the current position, append to snake blocks to
        # keep track
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_blocks.append(snake_head)
        
        # Ensure the snake is only as big as the length we've set
        if len(snake_blocks) > snake_length:
            del snake_blocks[0]

        # Not counting the last block, check if any other existing snake
        # blocks are crossing over the snake head (dead)
        for x in snake_blocks[:-1]:
            if x == snake_head:
                game_over = True

        # Draw a snake block for each point the user has
        for block in snake_blocks:
            pygame.draw.rect(screen, snake_color, [block[0], block[1], snake_size, snake_size])#the last part defines the area to draw
        pygame.draw.rect(screen, food_color, [fruit_x, fruit_y, snake_size, snake_size])

        # Update the speed vector of the snake
        snake_x += speed_x
        snake_y += speed_y

        # If the snake is touching fruit (x and y position match for snake head and
        # fruit), set the fruit to a new, random position and update snake length
        if snake_x == fruit_x and snake_y == fruit_y:
            fruit_x = round(random.randrange(0, screen_width - snake_size) / 10.0) * 10.0
            fruit_y = round(random.randrange(0, screen_height - snake_size) / 10.0) * 10.0
            snake_length += 1
            snake_speed+=0.05 
        # If the snake goes beyond the left or right side of the screen,
        if (snake_x >= screen_width or snake_x < 0 or
            # if the snake goes beyond the top of bottom of the screen,
                snake_y >= screen_height or snake_y < 0):
            # Set game over to true
            game_over = True
        show_score(1, white, 'consolas', 20)

    # Game over logic (screen showing users score + how to continue)
    else:
        mixer.music.stop()
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (screen_width/2, screen_height/4)
        screen.fill(black)
        screen.blit(game_over_surface, game_over_rect)
        score = font.render('You scored ' + str(snake_length), False, red)
        screen.blit(score, (320, screen_height / 2 +100))
        text = font.render('You lost! Press \'Q\' to quit, or Spacebar to play again', False, red)
        screen.blit(text, (320, screen_height / 2 +200))
    # Update the screen
    pygame.display.flip()
    clock.tick(snake_speed)

    # Event Loop
    # Get the next events from the queue
    # For each event returned from get(),
    for event in pygame.event.get():
        # If the event is "KEYDOWN"
        if event.type == pygame.KEYDOWN:
            # If "Q" is pressed, stop game
            if event.key == pygame.K_q:
                running = False
            # If space is pressed, reset game
            if event.key == pygame.K_SPACE:
                game_over = False
                snake_x = screen_width / 2
                snake_y = screen_height / 2
                snake_blocks = []
                snake_length = 1
                mixer.music.play()
            # Movement (up, down, left, right arrow keys)
            if event.key == pygame.K_UP:
                speed_x = 0
                speed_y = -10
            if event.key == pygame.K_DOWN:
                speed_x = 0
                speed_y = 10
            if event.key == pygame.K_LEFT:
                speed_y = 0
                speed_x = -10
            if event.key == pygame.K_RIGHT:
                speed_y = 0
                speed_x = 10
            #if the esc key is pressed, enter to pause state
            if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()
        # If the event is "QUIT" (when user clicks X on window)
        if event.type == pygame.QUIT:
            # Set running to False, stop event loop
            running = False
