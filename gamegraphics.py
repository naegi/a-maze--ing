import pygame

import gamemap
from logs import logs

logger = logs.get_logger(__name__)

class Graphics:
    def __init__(self, game, event_dispatcher):
        pygame.init()

        self.game = game
        self.event_dispatcher = event_dispatcher

        self.screen = pygame.display.set_mode((640,480))

        self.font = pygame.font.SysFont("arial", 72)
        self.text_to_show = False

        self.event_dispatcher.register("win", lambda: self.set_text("Won !", (120, 120, 0)))
        self.event_dispatcher.register("trap", lambda: self.set_text("TRAPPED !", (255, 80, 0)))


    def setup_sprites(self):
        background = pygame.Surface(self.screen.get_size())
        background.fill((255,255,255))
        self.background = background.convert()

        width, height = self.screen.get_size()

        self.sprite_height =height // self.game.map.height
        self.sprite_width = width // self.game.map.width

        wall_sprite = pygame.Surface((self.sprite_width, self.sprite_height))
        wall_sprite.fill((0,0,0))
        self.wall_sprite = wall_sprite.convert()

        trap_sprite = pygame.Surface((self.sprite_width, self.sprite_height))
        trap_sprite.fill((255,80,70))
        self.trap_sprite = trap_sprite.convert()

        flag_winning_sprite = pygame.Surface((self.sprite_width, self.sprite_height))
        flag_winning_sprite.fill((255,255,140))
        self.flag_winning_sprite = flag_winning_sprite.convert()

        player_sprite = pygame.Surface((self.sprite_width, self.sprite_height))
        player_sprite.fill((69,69,125))
        self.player_sprite = player_sprite.convert()


    def set_text(self, text, color):
        self.text = self.font.render(text, True, color, (60, 60, 60, 60))
        self.text_to_show = True

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_dispatcher.add_event("quit", "pygame quit")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_dispatcher.add_event("quit", "key escape")
                if event.key == pygame.K_q:
                    self.event_dispatcher.add_event("quit", "key Q")
                if event.key == pygame.K_LEFT:
                    self.event_dispatcher.add_event("movePlayer", "left")
                if event.key == pygame.K_RIGHT:
                    self.event_dispatcher.add_event("movePlayer", "right")
                if event.key == pygame.K_UP:
                    self.event_dispatcher.add_event("movePlayer", "up")
                if event.key == pygame.K_DOWN:
                    self.event_dispatcher.add_event("movePlayer", "down")
            elif event.type == pygame.VIDEORESIZE:
                self.setup_sprites()
                surface = pygame.display.set_mode((event.w, event.h),
                                            pygame.RESIZABLE)
        def blit_sprite(sprite, x, y):
            if sprite:
                self.screen.blit(sprite, (x*self.sprite_width, (self.game.map.height - y - 1)*self.sprite_height))

        self.screen.blit(self.background, (0, 0))
        for i in range(self.game.map.width):
            for j in range(self.game.map.height):
                tile_type = self.game.map.tile_map[i][j]
                sprite = None
                if tile_type == gamemap.TileType.WALL:
                    sprite = self.wall_sprite
                if tile_type == gamemap.TileType.FLAG_WINNING:
                    sprite = self.flag_winning_sprite
                if tile_type == gamemap.TileType.TRAP:
                    sprite = self.trap_sprite
                blit_sprite(sprite, i, j)

        blit_sprite(self.player_sprite, self.game.player.position_x, self.game.player.position_y)


        if self.text_to_show:
            width, height = self.screen.get_size()
            text_width, text_height = self.text.get_size()
            self.screen.blit(self.text, ((width-text_width) // 2 , (height - text_height) // 2))



        pygame.display.flip()

