import pygame

from maze_generator import generator, randomGap, addDecorations
from maze_charactermov import Player
from game import Game

from sprites import Sprites



n = 30
maze = generator(n)
maze = randomGap(maze, 10, n)

ROWS = len(maze)
COLS = len(maze[0])

CELL_SIZE = 50
VIEW_SIZE = 3
WIDTH = VIEW_SIZE * CELL_SIZE
HEIGHT = VIEW_SIZE * CELL_SIZE

player = Player()
goal = (COLS - 2, ROWS - 1)

game = Game(maze, player, goal)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.reset()

            elif event.key == pygame.K_w:
                player.move(0, -1, maze)
            elif event.key == pygame.K_s:
                player.move(0, 1, maze)
            elif event.key == pygame.K_a:
                player.move(-1, 0, maze)
            elif event.key == pygame.K_d:
                player.move(1, 0, maze)

            game.recalculate()

    if player.x == goal[0] and player.y == goal[1]:
        pygame.display.set_caption("¡HAS GANADO!")

    screen.fill((0, 0, 0))

    for y in range(ROWS):
        for x in range(COLS):
            tile = maze[y][x]

            if tile == 0:
                color = (255, 255, 255)
            elif tile == 1:
                color = (40, 40, 40)
            elif tile == 10:
                color = (120, 200, 120)
            elif tile == 11:
                color = (0, 200, 255)
            elif tile == 12:
                color = (120, 120, 120)
            elif tile == 13:
                color = (255, 150, 200)
            else:
                color = (200, 200, 200)  # fallback seguro

            screen.blit(
                sprites.get_tile(tile),
                (x * CELL_SIZE, y * CELL_SIZE)
            )


    for x, y in game.closed:
        pygame.draw.rect(
            screen,
            (255, 80, 80),
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )


    for x, y in game.path:
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )


        img = sprites.get_tile(tile)

        if img:
            screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))    
        
        

    # PLAYER
    pygame.draw.rect(
        screen,
        (0, 100, 255),
        (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )

    pygame.display.flip()

pygame.quit()
