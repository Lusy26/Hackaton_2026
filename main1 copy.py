import pygame

from maze_generator import generator, randomGap, addDecorations
from maze_charactermov import Player
from game import Game

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

    # Dibuja solo una vista 3x3 centrada en el jugador.
    for view_y in range(VIEW_SIZE):
        for view_x in range(VIEW_SIZE):
            world_x = player.x + view_x - 1
            world_y = player.y + view_y - 1

            if 0 <= world_x < COLS and 0 <= world_y < ROWS:
                tile = maze[world_y][world_x]
                if tile == 0:
                    color = (255, 255, 255)
                elif tile == 1 or tile == -1:
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
                    color = (200, 200, 200)
            else:
                color = (80, 80, 80)

            pygame.draw.rect(
                screen,
                color,
                (view_x * CELL_SIZE, view_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    pygame.draw.rect(
        screen,
        (0, 100, 255),
        (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )

    pygame.display.flip()

pygame.quit()
