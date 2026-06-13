import pygame

from maze_generator import generator, randomGap, addDecorations
from maze_charactermov import Player
from game import Game


n = 30
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

            # Mostrar solo un área 5x5 (25 bloques) alrededor del jugador;
            # lo demás se pinta en gris oscuro
            radius = 2  # 2 en cada dirección -> 5x5 = 25 bloques
            if abs(x - player.x) > radius or abs(y - player.y) > radius:
                color = (80, 80, 80)
            else:
                if tile == 0:
                    color = (255, 255, 255)
                elif tile == 1 or tile == -1:
                    color = (40, 40, 40)
                else:
                    color = (200, 200, 200)  # fallback seguro

            pygame.draw.rect(
                screen,
                color,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )



    # PLAYER
    pygame.draw.circle(
        screen,
        (0, 100, 255),
        (CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 2
    )
    
    pygame.display.flip()

pygame.quit()