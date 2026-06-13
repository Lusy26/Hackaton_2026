import pygame

from maze_generator import generator, randomGap, addDecorations
from maze_charactermov import Player
from game import Game
from sprites import Sprites




n = 30
maze = generator(n)
maze = randomGap(maze, 10, n)
maze = addDecorations(maze, 8)
maze = addDecorations(maze, 8)





ROWS = len(maze)
COLS = len(maze[0])

CELL_SIZE = 10

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE




player = Player()
goal = (COLS - 2, ROWS - 1)

game = Game(maze, player, goal)




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sprites = Sprites(CELL_SIZE)

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
            # render tile using sprites
            tile_surf = sprites.get_tile(tile)
            if tile_surf is not None:
                screen.blit(tile_surf, (x * CELL_SIZE, y * CELL_SIZE))
            else:
                # fallback: draw a rect if no sprite available
                pygame.draw.rect(
                    screen,
                    (200, 200, 200),
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )


    


    
    for x, y in game.path:
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )


    
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )
    # draw goal and player using sprites
    screen.blit(sprites.goal, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE))

    screen.blit(sprites.player, (player.x * CELL_SIZE, player.y * CELL_SIZE))



    pygame.display.flip()

pygame.quit()