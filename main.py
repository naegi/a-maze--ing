from logs import logs
from game import Game

logger = logs.get_logger(__name__)

def main():
    logger.info("Hi!")
    logger.debug("Debug logs activated")

    Game().run()

    logger.info("Bye!")


if __name__ == "__main__":
    main()
