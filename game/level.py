import pygame
from tile import Tile
from settings import *
from entieties import Player

class Level:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.get_surface()

        self.visible = CameraGrup()
        self.obstacles = pygame.sprite.Group()
        self.player = None

        self.load_map(MAP)

    def load_map(self, map):
        for i, row in enumerate(map):
            for j, t in enumerate(row):
                if t==1:
                    Tile((TILE_SIZE*i, TILE_SIZE*j), [self.visible, self.obstacles])
                elif t==2:
                    self.player = Player((TILE_SIZE*i, TILE_SIZE*j), [self.visible], self.obstacles)

    def update(self) -> None:
        self.visible.update()
        self.visible.show(self.player)


class CameraGrup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.pos = pygame.math.Vector2(0, 0)
        self.view = pygame.Rect(0, 0, WIDTH, HEIGHT)

        self.window_w = self.screen.get_size()[0]//2
        self.window_h = self.screen.get_size()[1]//2

    def show(self, p: Player):
        self.pos.x, self.pos.y = p.rect.centerx - self.window_w, p.rect.centery - self.window_h
        self.view.x = self.pos.x
        self.view.y = self.pos.y
        for sprite in [s for s in sorted(self.sprites(), key = lambda s: s.rect.centery) if s.rect.colliderect(self.view)]:
            self.screen.blit(sprite.image, sprite.rect.topleft - self.pos)