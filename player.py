from logs import logs
import gamemap

logger = logs.get_logger(__name__)

class Player:
    def __init__(self, game, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.game = game

        self.position_x, self.position_y = self.game.map.start_pos
        self.event_dispatcher.register("movePlayer", self.move)

    def move(self, direction):
        position_x = self.position_x
        position_y = self.position_y

        if direction == "right":
            position_x = position_x + 1
        if direction == "left":
            position_x = position_x - 1
        if direction == "up":
            position_y = position_y + 1
        if direction == "down":
            position_y = position_y - 1

        logger.info("Trying to set player position to {}:{}".format(position_x, position_y))
        if not self.game.map.can_go(position_x, position_y):
            return

        tile_type = self.game.map.tile_map[position_x][position_y]

        if tile_type == gamemap.TileType.WALL:
            return

        self.position_x = position_x
        self.position_y = position_y
        logger.info("Set player position to {}:{}".format(self.position_x, self.position_y))

        if tile_type == gamemap.TileType.FLAG_WINNING:
            self.event_dispatcher.add_event("win")
        if tile_type == gamemap.TileType.TRAP:
            self.event_dispatcher.add_event("trap")
