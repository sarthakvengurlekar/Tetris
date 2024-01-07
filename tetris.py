import pygame
import random

# Define constants for the game

BLOCK_SIZE = 30
FPS = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
move_down_time = 0
move_down_speed = 300
base_speed = 400
score = 0
level = 1
lines_cleared_total = 0


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

def check_collision(tetromino, grid):
    for x, y in TETROMINOES[tetromino['shape']][tetromino['rotation']]:
        grid_x = tetromino['x'] + x
        grid_y = tetromino['y'] + y

        # Check if the tetromino is outside the grid boundaries
        if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
            return True

        # Check if the tetromino collides with settled blocks
        if grid_y >= 0 and grid[grid_y][grid_x] == 1:
            return True

    return False

def settle_tetromino(tetromino, grid):
    for x, y in TETROMINOES[tetromino['shape']][tetromino['rotation']]:
        grid_x = tetromino['x'] + x
        grid_y = tetromino['y'] + y
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            grid[grid_y][grid_x] = 1

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:  # If the cell is not empty
                pygame.draw.rect(screen, (255, 255, 255), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def clear_lines(grid):
    # Create a new grid with only the rows that are not full
    new_grid = [row for row in grid if not all(row)]
    
    # Calculate the number of lines cleared
    lines_cleared = GRID_HEIGHT - len(new_grid)

    #Update score
    global score
    score += lines_cleared * 100 #100 points per line
    
    # Add empty rows at the top for each line cleared
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])

    global lines_cleared_total, level
    lines_cleared_total += lines_cleared

    # Increase level every 10 lines cleared, for example
    if lines_cleared_total >= level * 5:
        level += 1

    return new_grid, lines_cleared

# Game loop
while not game_over:
    # Adjust falling speed based on level
    move_down_speed = base_speed - (level - 1) * 50  # Decrease speed by 50 ms per level
    move_down_speed = max(50, move_down_speed)  # Set a lower limit to prevent it from becoming too fast
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino['x'] -= 1
                if check_collision(current_tetromino, grid):
                    current_tetromino['x'] += 1
            elif event.key == pygame.K_RIGHT:
                current_tetromino['x'] += 1
                if check_collision(current_tetromino, grid):
                    current_tetromino['x'] -= 1
            elif event.key == pygame.K_UP:
                original_rotation = current_tetromino['rotation']
                current_tetromino['rotation'] = (current_tetromino['rotation'] + 1) % len(TETROMINOES[current_tetromino['shape']])
                if check_collision(current_tetromino, grid):
                    current_tetromino['rotation'] = original_rotation
            elif event.key == pygame.K_DOWN:
                current_tetromino['y'] += 1
                if check_collision(current_tetromino, grid):
                    current_tetromino['y'] -= 1
                    settle_tetromino(current_tetromino, grid)
                    grid, lines_cleared = clear_lines(grid)  # Clear completed lines
                    current_tetromino = new_tetromino()  # Spawn a new Tetromino
                    if check_collision(current_tetromino, grid):
                        game_over = True

    time_passed = clock.tick(FPS)
    move_down_time += time_passed

     # Automatically move the Tetromino down at regular intervals
    if move_down_time > move_down_speed:
        move_down_time = 0
        current_tetromino['y'] += 1
        if check_collision(current_tetromino, grid):
            # If moving down causes a collision, move it back and settle it
            current_tetromino['y'] -= 1
            settle_tetromino(current_tetromino, grid)
            grid, lines_cleared = clear_lines(grid)  # Clear completed lines
            current_tetromino = new_tetromino()  # Spawn a new Tetromino

            if check_collision(current_tetromino, grid):
                game_over = True
    

    screen.fill((0, 0, 0))

    draw_grid(screen, grid)
    draw_tetromino(screen, current_tetromino)

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (5, 5))  # Position the score in the top-left corner
    # Display Level
    level_text = font.render(f'Level: {level}', True, (255, 255, 255))
    screen.blit(level_text, (5, 30))  # Adjust position as needed
    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()