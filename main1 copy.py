import pygame

from maze_generator import generator, randomGap, addDecorations
from maze_charactermov import Player
from game import Game
from sprites import Sprites


# -------------------
# MAPA
# -------------------
n = 30
maze = generator(n)
maze = randomGap(maze, 10, n)
maze = addDecorations(maze, 8)


ROWS = len(maze)
COLS = len(maze[0])


# -------------------
# CONFIG
# -------------------
CELL_SIZE = 50
VIEW_SIZE = 5   # cámara 5x5

WIDTH = VIEW_SIZE * CELL_SIZE
HEIGHT = VIEW_SIZE * CELL_SIZE


# -------------------
# PLAYER + GAME
# -------------------
player = Player()
goal = (COLS - 2, ROWS - 1)

game = Game(maze, player, goal)


# -------------------
# PYGAME INIT
# -------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sprites = Sprites(CELL_SIZE)


running = True


# -------------------
# LOOP
# -------------------
while running:
    clock.tick(10)

    # -------------------
    # EVENTS
    # -------------------
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

            # recalcular IA
            game.recalculate()


    # -------------------
    # WIN CONDITION
    # -------------------
    if (player.x, player.y) == goal:
        pygame.display.set_caption("¡HAS GANADO!")


    # -------------------
    # SCREEN
    # -------------------
    screen.fill((0, 0, 0))


    # -------------------
    # CAMERA
    # -------------------
    start_x = player.x - VIEW_SIZE // 2
    start_y = player.y - VIEW_SIZE // 2


    # -------------------
    # DRAW MAP
    # -------------------
    for y in range(start_y, start_y + VIEW_SIZE):
        for x in range(start_x, start_x + VIEW_SIZE):

            screen_x = (x - start_x) * CELL_SIZE
            screen_y = (y - start_y) * CELL_SIZE

            if 0 <= x < COLS and 0 <= y < ROWS:

                tile = maze[y][x]
                img = sprites.get_tile(tile)

                if img:
                    screen.blit(img, (screen_x, screen_y))
                else:
                    pygame.draw.rect(
                        screen,
                        (50, 50, 50),
                        (screen_x, screen_y, CELL_SIZE, CELL_SIZE)
                    )

            else:
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (screen_x, screen_y, CELL_SIZE, CELL_SIZE)
                )


    # -------------------
    # IA PATH (solo visible)
    # -------------------
    for x, y in game.closed:
        if start_x <= x < start_x + VIEW_SIZE and start_y <= y < start_y + VIEW_SIZE:
            pygame.draw.rect(
                screen,
                (255, 80, 80),
                ((x - start_x) * CELL_SIZE,
                 (y - start_y) * CELL_SIZE,
                 CELL_SIZE,
                 CELL_SIZE)
            )

    for x, y in game.path:
        if start_x <= x < start_x + VIEW_SIZE and start_y <= y < start_y + VIEW_SIZE:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                ((x - start_x) * CELL_SIZE,
                 (y - start_y) * CELL_SIZE,
                 CELL_SIZE,
                 CELL_SIZE)
            )


    # -------------------
    # GOAL
    # -------------------
    if start_x <= goal[0] < start_x + VIEW_SIZE and start_y <= goal[1] < start_y + VIEW_SIZE:
        screen.blit(
            sprites.goal,
            ((goal[0] - start_x) * CELL_SIZE,
             (goal[1] - start_y) * CELL_SIZE)
        )


    # -------------------
    # PLAYER (siempre centro pantalla)
    # -------------------
    pygame.draw.rect(
        screen,
        (0, 100, 255),
        (
            (VIEW_SIZE // 2) * CELL_SIZE,
            (VIEW_SIZE // 2) * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )


    pygame.display.flip()


pygame.quit()