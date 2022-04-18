# Author: Angel Hernán Zini (hernan.zini@gmail.com)
# Year: 2021

import pygame, random
from pygame.locals import *

class Grid:
    colors = []
    def __init__(self, blockSize, blocksWidth, blocksHeight, top, left, visibleGridLines):
        self.blockSize = blockSize
        self.blocksWidth = blocksWidth
        self.blocksHeight = blocksHeight
        self.width = blocksWidth * blockSize
        self.height = blocksHeight * blockSize
        self.top = top
        self.left = left
        self.visibleGridLines = visibleGridLines
        self.blockSurface = pygame.Surface((blockSize, blockSize))

    def draw(self, surface, color):
        surface.fill(color)
        #draw a frame
        pygame.draw.rect(surface, (0, 0, 200), (self.left-2, self.top-2, self.width+6, self.height+6), 3)

        #draw grid lines
        if self.visibleGridLines:
            for x in range(0, self.width + self.blockSize, self.blockSize): # Draw vertical lines
                pygame.draw.line(screen, (40, 40, 40), (self.left + x, self.top), (self.left + x, self.top + self.height) )
            for y in range(0, self.height + self.blockSize, self.blockSize): # Draw horizontal lines
                pygame.draw.line(screen, (40, 40, 40), (self.left, self.top + y), (self.left + self.width, self.top + y) )

    def setBlock(self, surface, coordinates, color):
        self.blockSurface.fill(color)
        gridCoordinates = ()
        gridCoordinates = (coordinates[0] * self.blockSize + self.left, coordinates[1] * self.blockSize + self.top)
        surface.blit(self.blockSurface, gridCoordinates)

    def getIndex(self, coordinates):
        return coordinates[0] + coordinates[1] * self.blocksWidth

    def addText(self, surface, coordinates, font, text, color):
        _font = font.render(text, True, color)
        _rect = _font.get_rect()
        _rect.topleft = (coordinates)
        surface.blit(_font, _rect)
#Grid class


def getPattern(pattern):
    if pattern == -2:
        states = [random.randint(0, 1) for _ in range( grid.blocksWidth * grid.blocksHeight)]
    elif pattern == -1:
        states = [1] * grid.blocksWidth * grid.blocksHeight 
    else:
        states = [0] * grid.blocksWidth * grid.blocksHeight #initializes an array of width x height
        
        patterns = [
                ['.X.', 
                '..X',
                'XXX'],

                ['XXX.X', 
                'X....',
                '...XX', 
                '.XX.X',
                'X.X.X'],

                ['......X.', 
                '....X.XX',
                '....X.X.', 
                '....X...',
                '..X.....', 
                'X.X.....'],

                ['XXXXXXXX.XXXXX...XXX......XXXXXXX.XXXXX'],

                ['...X...', 
                '...X...',
                '...X...'],

                ['........................X...........', 
                '......................X.X...........',
                '............XX......XX............XX', 
                '...........X...X....XX............XX',
                'XX........X.....X...XX..............', 
                'XX........X...X.XX....X.X...........',
                '..........X.....X.......X...........', 
                '...........X...X....................',
                '............XX......................']
                ]

        x_offset = grid.blocksWidth // 2 - 20
        y_offset = grid.blocksHeight // 2 - 10

        for y in range(0, len(patterns[pattern])):
            for x in range(0, len(patterns[pattern][y])):
                if patterns[pattern][y][x] == 'X':
                    states[grid.getIndex( (x + x_offset, y + y_offset)) ] = 1

    return states
#getPattern function


pygame.init()
pygame.display.set_caption('Game Of Life (and Death) by @HernanZini')
font1 = pygame.font.Font('freesansbold.ttf', 18)
font2 = pygame.font.Font('freesansbold.ttf', 16)
grid = Grid(6, 160, 110, 60, 50, False)
screen = pygame.display.set_mode((grid.width + grid.left * 2, grid.height + grid.top * 2))
clock = pygame.time.Clock()

#parameters initial values
fps = 0
pattern = -2 #choose the pattern to start with (-1 = Full, -2 = Random pattern)
generation = 0
population = 0
states = getPattern(pattern)
color = (255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_KP_PLUS:
                fps = 0 if fps == 24 else fps + 1
            if event.key == K_KP_MINUS:
                fps = 24 if fps == 0 else fps - 1
            if event.key == K_UP:
                pattern = -2 if pattern == 5 else pattern + 1
                generation = 0
                states = getPattern(pattern)
            if event.key == K_DOWN:
                pattern = 5 if pattern == -2 else pattern - 1
                generation = 0
                states = getPattern(pattern)
            if event.key == K_RETURN:
                generation = 0
                states = getPattern(pattern)
            if event.key == K_LEFT:
                color = color = (255, 255, 255)
            if event.key == K_RIGHT:
                color = (random.randrange(100, 255, 1), random.randrange(100, 255, 1), random.randrange(100, 255, 1))
            if event.key == K_SPACE:
                grid.visibleGridLines = not grid.visibleGridLines

    grid.draw(screen, (0, 0, 0))
    output = states.copy()
    population = 0

    for x in range(1, grid.blocksWidth-1):
        for y in range(1, grid.blocksHeight-1):
            
            i = grid.getIndex((x, y))  #converts coordiantes into vector index
  
            if output[i]:   
                grid.setBlock(screen, (x, y), color)
  
            #Get next generation
            neighbours =    output[grid.getIndex((x - 1, y - 1))] +  output[grid.getIndex((x, y - 1))] +  output[grid.getIndex((x + 1 , y - 1))] + \
                            output[grid.getIndex((x - 1, y))]     +              0                     +  output[grid.getIndex((x + 1, y))]      + \
                            output[grid.getIndex((x - 1, y + 1))] +  output[grid.getIndex((x, y + 1))] +  output[grid.getIndex((x + 1, y + 1))]

            if states[i]:
                population += 1
                states[i] = 1 if (neighbours == 2 or neighbours == 3) else 0
            else:
                states[i] = 1 if neighbours == 3 else 0

    generation += 1
    grid.addText(screen, (grid.left, grid.top - 30), font1, "Generation: %s - Population %s    FPS %s (0 fastest)" % (generation, population, fps), (180, 180, 0))
    grid.addText(screen, (grid.left, grid.height + 70), font2, "Change pattern: [Up/Down]  Speed: [+/-]  Color: [Right=white/Left=random]  Restart: [Return]  Grid lines: [Space]", (0, 180, 180))
    pygame.display.update()
    clock.tick(fps) #FPS  

