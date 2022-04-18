# Author: Angel Hernán Zini (hernan.zini@gmail.com)
# Year: 2021

import pygame, random
from pygame.locals import *

#GLOBAL Constants 
UP      = 0
DOWN    = 1
LEFT    = 2
RIGHT   = 3
FIELD_HEIGHT = 700
FIELD_WIDTH  = 1100
BLOCK_SIZE = 20
FPS = 12 #set initial game speed here

def get_random_pos():
    x = random.randint(BLOCK_SIZE, (FIELD_WIDTH-1)-BLOCK_SIZE)
    y = random.randint(BLOCK_SIZE, (FIELD_HEIGHT-1)-BLOCK_SIZE)
    return (x // BLOCK_SIZE * BLOCK_SIZE, y // BLOCK_SIZE * BLOCK_SIZE) 

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

score = 0
snake = [(200, 200), (210, 200), (220, 200)]
apple_pos = get_random_pos()
direction = LEFT

pygame.init()
screen = pygame.display.set_mode((FIELD_WIDTH, FIELD_HEIGHT))
snake_skin = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
snake_skin.fill((41, 163, 41)) 
apple = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
apple.fill((204, 0, 0)) 
pygame.display.set_caption('Nibbles by @HernanZini')
font = pygame.font.Font('freesansbold.ttf', 18)
clock = pygame.time.Clock()

game_over = False
while not game_over:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
        if event.type == KEYDOWN:
            if event.key == K_UP and direction != DOWN:
                direction = UP
            if event.key == K_DOWN and direction != UP:
                direction = DOWN
            if event.key == K_LEFT and direction != RIGHT:
                direction = LEFT
            if event.key == K_RIGHT and direction != LEFT:
                direction = RIGHT

    #border collision detection
    if snake[0][0] >= FIELD_WIDTH-BLOCK_SIZE or snake[0][0] < BLOCK_SIZE or snake[0][1] >= FIELD_HEIGHT-BLOCK_SIZE or snake[0][1] < BLOCK_SIZE:
        game_over = True
        # break

    #apple collision detection
    if collision(snake[0], apple_pos):
        apple_pos = get_random_pos()
        snake.append((0, 0))
        score = score + 1
        FPS += 1 #Increase speed

    #self-nibble
    for pos in snake[1:len(snake)]:
        if collision(pos, snake[0]):
            game_over = True
            # break

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    #Move the snake
    if direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - BLOCK_SIZE)
    if direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + BLOCK_SIZE)
    if direction == RIGHT:
        snake[0] = (snake[0][0] + BLOCK_SIZE, snake[0][1])
    if direction == LEFT:
        snake[0] = (snake[0][0] - BLOCK_SIZE, snake[0][1])
        
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (140, 140, 140), (0, 0, FIELD_WIDTH, FIELD_HEIGHT), BLOCK_SIZE )

    screen.blit(apple, apple_pos)

    for x in range(BLOCK_SIZE, FIELD_WIDTH-BLOCK_SIZE, BLOCK_SIZE): # Draw vertical lines
        pygame.draw.line(screen, (40, 40, 40), (x, BLOCK_SIZE), (x, (FIELD_HEIGHT-1)-BLOCK_SIZE))
    for y in range(BLOCK_SIZE, FIELD_HEIGHT-BLOCK_SIZE, BLOCK_SIZE): # Draw horizontal lines
        pygame.draw.line(screen, (40, 40, 40), (BLOCK_SIZE, y), ((FIELD_WIDTH-1)-BLOCK_SIZE, y))
    
    score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (FIELD_WIDTH - 150, 2)
    screen.blit(score_font, score_rect)

    #draw the snake!
    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()

    if game_over:
        score = 0
        FPS = 12
        snake = [(200, 200), (210, 200), (220, 200)]
        apple_pos = get_random_pos()
        direction = LEFT
        game_over = False
