import pygame
import random

# Define constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 20

# Define the shapes of the tetrominoes
TETROMINOES = {
    'I': [
        [(0, -1), (0, 0), (0, 1), (0, 2)],
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [(0, -1), (0, 0), (0, 1), (0, 2)],
        [(-1, 0), (0, 0), (1, 0), (2, 0)]
    ],
    'J': [
        [(-1, -1), (0, -1), (0, 0), (0, 1)],
        [(-1, 1), (-1, 0), (0, 0), (1, 0)],
        [(0, -1), (0, 0), (0, 1), (1, 1)],
        [(-1, 0), (0, 0), (1, 0), (1, -1)]
    ],
    'L': [
        [(1, -1), (0, -1), (0, 0), (0, 1)],
        [(-1, -1), (-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (0, 0), (0, -1)],
        [(-1, 0), (0, 0), (1, 0), (1, 1)]
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ],
    'S': [
        [(0, -1), (0, 0), (-1, 0), (-1, 1)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(0, -1), (0, 0), (-1, 0), (-1, 1)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)]
    ],
    'T': [
        [(-1, 0), (0, 0), (1, 0), (0, -1)],
        [(0, -1), (0, 0), (0, 1), (1, 0)],
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(0, -1), (0, 0), (0, 1), (-1, 0)]
    ],
    'Z': [
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(0, -1), (-1, 0), (0, 0), (-1, 1)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(0, -1), (-1, 0), (0, 0), (-1, 1)]
    ]
}

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game_over = False

def new_tetromino():
    shape = random.choice(list(TETROMINOES.keys()))
    return {'shape': shape, 'x': SCREEN_WIDTH // 2 // BLOCK_SIZE, 'y': 0, 'rotation': 0}

def draw_tetromino(screen, tetromino):
    for x, y in TETROMINOES[tetromino['shape']][tetromino['rotation']]:
        pygame.draw.rect(screen, (255, 255, 255), (tetromino['x'] * BLOCK_SIZE + x * BLOCK_SIZE, tetromino['y'] * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

current_tetromino = new_tetromino()

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino['x'] -= 1
            elif event.key == pygame.K_RIGHT:
                current_tetromino['x'] += 1
            elif event.key == pygame.K_UP:
                current_tetromino['rotation'] = (current_tetromino['rotation'] + 1) % len(TETROMINOES[current_tetromino['shape']])
            elif event.key == pygame.K_DOWN:
                current_tetromino['y'] += 1
    

    screen.fill((0, 0, 0))

    draw_tetromino(screen, current_tetromino)

    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()