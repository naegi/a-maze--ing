from enum import IntEnum
import random
from logs import logs


logger = logs.get_logger(__name__)

class TileType(IntEnum):
    GROUND = 0
    WALL = 1
    FLAG_WINNING = 2
    TRAP = 3

def get_neighbourhood_walls(maze, x, y):
    r = []
    if x - 1 >= 0:
        r.append((x-1, y))
    if y - 1 >= 0:
        r.append((x, y-1))
    if len(maze) > x+1:
        r.append((x+1, y))
    if len(maze[0]) > y+1:
        r.append((x, y+1))
    return r

def gen_maze(n, m, start):
    maze = [[TileType.WALL for _ in range(m)] for _ in range(n)] # All is wall
    walls = {start}

    while walls:
        current_x, current_y = random.choice(list(walls))
        walls.remove((current_x, current_y))

        neighbours = get_neighbourhood_walls(maze, current_x, current_y)

        def is_wall(x):
            return maze[x[0]][x[1]] == TileType.GROUND
        if sum(map(is_wall, neighbours)) <= 1:
            logger.debug("{}:{} will be ground".format(current_x, current_y))
            maze[current_x][current_y] = TileType.GROUND
            walls.update(neighbours)

    return maze


class Map:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.start_pos = (0, 0)
        self.tile_map = gen_maze(self.width, self.height, self.start_pos)

        winning_x, winning_y = random.choice([(x, y) for x in range(self.width) for y in range(self.height)
                                               if self.tile_map[x][y] == TileType.GROUND])
        self.tile_map[winning_x][winning_y] = TileType.FLAG_WINNING

        self.winning_pos = winning_x, winning_y

    def can_go(self, tile_x, tile_y):
        return 0 <= tile_x and tile_x < self.width and 0 <= tile_y and tile_y < self.height

    def neighbours(self, tile_x, tile_y):
        neighbours = [
            (tile_x, tile_y + 1),
            (tile_x - 1, tile_y),
            (tile_x + 1, tile_y),
            (tile_x, tile_y - 1),
        ]

        return [(x, y) for x, y in neighbours if self.can_go(x, y) and self.tile_map[x][y] != TileType.WALL]
