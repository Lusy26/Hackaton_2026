import pygame

class Sprites:
    def __init__(self, cell_size):
        self.cell_size = cell_size

        def load(name):
            return pygame.transform.scale(pygame.image.load(f"assets/{name}"), (cell_size, cell_size))

        # cargar y escalar assets existentes
        self.tree = load('tree.png')
        self.rock = load('rock.png')
        self.house = load('house.png')
        self.crystal = load('crystal.png')
        self.cross = load('cross.png')
        self.hole = load('hole.png')
        self.figure = load('figure.png')

        # Sprites auxiliares
        self.floor = pygame.Surface((cell_size, cell_size))
        self.floor.fill((200, 200, 200))
        self.wall = self.rock
        self.player = self.figure
        self.goal = self.cross

    def get_tile(self, tile):
        if tile == 0:
            return self.floor
        if tile == 1 or tile == -1:
            return self.wall
        mapping = {
            10: self.tree,
            11: self.house,
            12: self.rock,
            13: self.crystal,
            14: self.cross,
            15: self.figure,
            16: self.hole,
        }
        return mapping.get(tile, self.floor)