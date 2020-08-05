from logs import logs

logger = logs.get_logger(__name__)

class AI:
    def __init__(self, game, event_dispatcher):
        self.game = game
        self.event_dispatcher = event_dispatcher
        self.path = self.find_path()
        logger.info(self.path)

    def find_path(self):
        paths = [[[] for _ in range(self.game.map.height)] for _ in range(self.game.map.width)]
        visited = [[False for _ in range(self.game.map.height)] for _ in range(self.game.map.width)]

        x, y = self.game.map.start_pos
        paths[x][y] = [(x, y)]
        pile = [(x, y)]

        while pile:
            x, y = pile.pop()
            visited[x][y] = True

            path = paths[x][y]

            neighbours = self.game.map.neighbours(x, y)
            for xn, yn in neighbours:
                if not paths[xn][yn] or len(paths[xn][yn]) >= len(path) + 1:
                    p = path.copy()
                    p.append((xn, yn))
                    paths[xn][yn] = p

            pile.extend((x, y) for x, y in neighbours if not visited[x][y])

        wx, wy = self.game.map.winning_pos
        return paths[wx][wy]

    def update(self):
        if self.path:
            p = self.path[0]
            self.path = self.path[1:]

            dx = p[0] - self.game.player.position_x
            dy = p[1] - self.game.player.position_y
            logger.info("{} {}".format(dx, dy))
            if dx == -1:
                self.event_dispatcher.add_event("movePlayer", "left")
            if dx == 1:
                self.event_dispatcher.add_event("movePlayer", "right")
            if dy == -1:
                self.event_dispatcher.add_event("movePlayer", "down")
            if dy == 1:
                self.event_dispatcher.add_event("movePlayer", "up")
