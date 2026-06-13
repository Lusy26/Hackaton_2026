class Player:
    def __init__(self, start_x=1, start_y=0):
        self.start_x = start_x
        self.start_y = start_y
        self.reset()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy

        # límites del mapa
        if new_x < 0 or new_y < 0:
            return
        if new_y >= len(maze) or new_x >= len(maze[0]):
            return

        # colisión con paredes
        if maze[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y