import pygame

class Sprites:
    def __init__(self, cell_size):

        self.tree = pygame.image.load("assets/tree.png")
        self.rock = pygame.image.load("assets/rock.png")
        self.house = pygame.image.load("assets/house.png")
        self.crystal = pygame.image.load("assets/crystal.png")
        self.cross = pygame.image.load("assets/cross.png")
        self.hole = pygame.image.load("assets/hole.png")
        self.figure = pygame.image.load("assets/figure.png")

        self.goal = pygame.image.load("assets/goal.png")

        self.cell_size = cell_size

       
        self.tree = pygame.transform.scale(self.tree, (cell_size, cell_size))
        self.rock = pygame.transform.scale(self.rock, (cell_size, cell_size))
        self.house = pygame.transform.scale(self.house, (cell_size, cell_size))
        self.crystal = pygame.transform.scale(self.crystal, (cell_size, cell_size))
        self.cross = pygame.transform.scale(self.cross, (cell_size, cell_size))
        self.hole = pygame.transform.scale(self.hole, (cell_size, cell_size))
        self.figure = pygame.transform.scale(self.figure, (cell_size, cell_size))
        self.goal = pygame.transform.scale(self.goal, (cell_size, cell_size))

def get_tile(self, tile):
    if tile == 10:
        return self.tree
    elif tile == 11:
        return self.rock
    elif tile == 12:
        return self.house
    elif tile == 13:
        return self.crystal
    elif tile == 14:
        return self.cross
    elif tile == 15:
        return self.hole
    elif tile == 16:
        return self.figure
    else:
        return None