import pygame

from maze_generator import generator, randomGap, addDecorations
from maze_charactermov import Player
from game import Game




n = 64
maze = generator(n)
maze = randomGap(maze, 10, n)





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

running = True




while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
     




    if player.x == goal[0] and player.y == goal[1]:
        pygame.display.set_caption("¡HAS GANADO!")



    screen.fill((0, 0, 0))

    for y in range(ROWS):
        for x in range(COLS):

            tile = maze[y][x]

            if tile == 0:
                color = (255, 255, 255)

            elif maze[y][x] == 1 or maze[y][x] == -1:
                 color = (40, 40, 40)

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

            pygame.draw.rect(
                screen,
                color,
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
    pygame.draw.rect(
        screen,
        (0, 100, 255),
        (CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
    )



    pygame.display.flip()

pygame.quit()