import pygame
from tile import Tile
from settings import *
from entieties import Player, TestEnemy

class Level:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.get_surface()

        self.visible = CameraGrup()
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = None

        self.load_map(MAP)

    def load_map(self, map):
        for i, row in enumerate(map):
            for j, t in enumerate(row):
                if t==1:
                    Tile((TILE_SIZE*j, TILE_SIZE*i), [self.visible, self.obstacles])
                elif t==2:
                    self.player = Player((TILE_SIZE*j, TILE_SIZE*i), [self.visible], self.obstacles)
                elif t==3:
                    TestEnemy((TILE_SIZE*j, TILE_SIZE*i), [self.visible, self.enemies], self.obstacles, player=self.player)

    def update(self) -> None:
        self.player.update()
        self.enemies.update()
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
        self.view.x, self.view.y = self.pos.x, self.pos.y
        for sprite in [s for s in sorted(self.sprites(), key = lambda s: s.rect.centery) if s.rect.colliderect(self.view)]:
            self.screen.blit(sprite.image, sprite.rect.topleft - self.pos)