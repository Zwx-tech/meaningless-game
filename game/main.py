import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("7 Spirits")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            self.screen.fill((0,0,0))

            self.level.update()
            debug(f"DIR: {self.level.player.direction}")

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()

    game.run()