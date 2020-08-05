import signal

from event_dispatcher import EventDispatcher

from logs import logs
import player
import ai

import gamegraphics
import gamemap

import utility

logger = logs.get_logger(__name__)

class Game:
    def __init__(self):
        self.running = False

        self.event_dispatcher = EventDispatcher()
        self.graphics = gamegraphics.Graphics(self, self.event_dispatcher)
        self.map = gamemap.Map()
        self.player = player.Player(self, self.event_dispatcher)

        self.ai = ai.AI(self, self.event_dispatcher)


        def sigint_handler(sig, frame):
            self.event_dispatcher.add_event("quit", "Ctrl-C")

        signal.signal(signal.SIGINT, sigint_handler)

        self.event_dispatcher.register("quit", self.quit)

    def quit(self, cause=None):
        logger.info("Stopping game, cause: {}".format(cause))
        self.running = False


    def get_move(self):
        move = input(">> ")
        self.event_dispatcher.add_event("movePlayer", move)

    def run(self):
        self.running = True
        self.graphics.setup_sprites()

        utility.repeat(self.event_dispatcher, "ai_update", 0.1, self.ai.update)
        while self.running:
            self.graphics.update()
            self.event_dispatcher.dispatch()
