# Pong game
# CodeSpace
# https://youtu.be/iFVPhP5VJz8
import pygame

# Game constants
white = (255, 255, 255) # White color RGB
black = (0, 0, 0) # Black color RGB
green = (0, 255, 0) # Green color RGB
width = 800 # Game screen width
height = 800 # Game screen height

pygame.init() 
gameFont = pygame.font.SysFont('Ubuntu', 40) # Font used in game text

delay = 30

# Paddle constants
paddleSpeed = 20 
paddleWidth = 10 
paddleHeight = 100 

# Start positions for paddles
p1_position_x = 10 
p1_position_y = height / 2 - paddleHeight / 2 
p2_position_x = width - paddleWidth - 10 
p2_position_y = height / 2 - paddleHeight / 2 

# Game score at the start
p1_score = 0
p2_score = 0

# Movement indicators
p1_up = False
p1_down = False
p2_up = False
p2_down = False

# Start ball variables
ball_position_x = width / 2
ball_position_y = height / 2
ball_size = 8
ball_velocity_x = -10
ball_velocity_y = 0

screen = pygame.display.set_mode((width, height))

# Function to draw all game objects om the screen
def draw():
    pygame.draw.rect(screen, green, (int(p1_position_x), int(p1_position_y), paddleWidth, paddleHeight))
    pygame.draw.rect(screen, green, (int(p2_position_x), int(p2_position_y), paddleWidth, paddleHeight))
    pygame.draw.circle(screen, green, (ball_position_x, ball_position_y), ball_size)
    score = gameFont.render(f"Game Score {str(p1_score)} : {str(p2_score)}", False, white)
    screen.blit(score, (width / 20, 30))

# Function to work with player movement
def player_movement():
    global p1_position_y
    global p2_position_y

    if p1_up:
        p1_position_y = max(p1_position_y - paddleSpeed, 0)
    elif p1_down:
        p1_position_y = min(p1_position_y + paddleSpeed, height - paddleHeight)
    if p2_up:
        p2_position_y = max(p2_position_y - paddleSpeed, 0)
    elif p2_down:
        p2_position_y = min(p2_position_y + paddleSpeed, height - paddleHeight)

#Function to work with ball movement and score
def ball_movement():
    global ball_position_x
    global ball_position_y
    global ball_velocity_x
    global ball_velocity_y
    global p1_score
    global p2_score

    if((ball_position_x + ball_velocity_x) < (p1_position_x + paddleWidth)) and (p1_position_y < (ball_position_y + ball_velocity_y + ball_size) < (p1_position_y + paddleHeight)):
        ball_velocity_x = -ball_velocity_x
        ball_velocity_y = (p1_position_y + paddleHeight / 2 - ball_position_y) / 15
        ball_velocity_y = -ball_velocity_y

    elif(ball_position_x + ball_velocity_x < 0):
        p2_score += 1
        ball_position_x = width / 2
        ball_position_y = height / 2
        ball_velocity_x = 10
        ball_velocity_y = 0
    
    if(ball_position_x + ball_velocity_x > p2_position_x - paddleWidth) and (p2_position_y < ball_position_y + ball_velocity_y + ball_size < p2_position_y + paddleHeight):
        ball_velocity_x = -ball_velocity_x
        ball_velocity_y = (p2_position_y + paddleHeight / 2 - ball_position_y) / 15
        ball_velocity_y = -ball_velocity_y

    elif(ball_position_x + ball_velocity_x > width):
        p1_score += 1
        ball_position_x = width / 2
        ball_position_y = height / 2
        ball_velocity_x = -10
        ball_velocity_y = 0

    if(ball_position_y + ball_velocity_y > height) or (ball_position_y + ball_velocity_y < 0):
        ball_velocity_y = -ball_velocity_y

    ball_position_x += ball_velocity_x
    ball_position_y += ball_velocity_y

pygame.display.set_caption('Pong Game v0.1 Alpha')
screen.fill(black)
pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                running = False
            if(event.key == pygame.K_w):
                p1_up = True
            if(event.key == pygame.K_s):
                p1_down = True
            if(event.key == pygame.K_UP):
                p2_up = True
            if(event.key == pygame.K_DOWN):
                p2_down = True

        if(event.type == pygame.KEYUP):
            if(event.key == pygame.K_w):
                p1_up = False
            if(event.key == pygame.K_s):
                p1_down = False
            if(event.key == pygame.K_UP):
                p2_up = False
            if(event.key == pygame.K_DOWN):
                p2_down = False

    screen.fill(black)
    player_movement()
    ball_movement()
    draw()
    pygame.display.flip()
    pygame.time.wait(delay)
