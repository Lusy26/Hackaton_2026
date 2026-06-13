from algorithm_A import maze_resolve_A

class Game:
    def __init__(self, maze, player, goal):
        self.maze = maze
        self.player = player
        self.goal = goal
        self.path = []
        self.closed = []
        self.recalculate()

    def recalculate(self):
        self.path, self.closed, _ = maze_resolve_A(
            self.maze,
            (self.player.x, self.player.y),
            self.goal
        )

    def reset(self):
        self.player.reset()
        self.recalculate()