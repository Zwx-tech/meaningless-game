import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, grups):
        super().__init__(grups)
        self.image = pygame.image.load("graphic/test/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0) # change hitbox based on texture
        print("tile size", self.hitbox)