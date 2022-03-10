import pygame
from math import sin, cos, pi
from debug import debug
from settings import *
import ai


class Entity(pygame.sprite.Sprite):

    def __init__(self, pos, grups, collision_sprites: list, img_path="graphic/test/player.png"):
        super().__init__(grups)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # change hitbox based on texture

        self.direction = pygame.math.Vector2()
        self.speed = 6

        self.collision_sprites = collision_sprites

    def collide(self, direction="x"):
        if direction == "x":
            for s in self.collision_sprites:
                if s.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = s.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = s.hitbox.right

        if direction == "y":
            for s in self.collision_sprites:
                if s.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = s.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = s.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:  # wypadkowa wektora
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collide("x")
        self.hitbox.y += self.direction.y * speed
        self.collide("y")

        self.rect.center = self.hitbox.center

    def rotate(self, alpha=False):
        if alpha is False: self.direction = pygame.Vector2(0,0)
        alpha = alpha/360 * (2 * pi)
        x, y = float(cos(alpha)), float(sin(alpha))
        self.direction = pygame.math.Vector2(x, y).normalize()

    def update(self, *args, **kwargs) -> None:
        self.move(self.speed)


class Player(Entity):

    def __init__(self, pos, grups, collision_sprites: list):
        super().__init__(pos, grups, collision_sprites)

        self.speed = 6

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self, *args, **kwargs) -> None:
        self.input()
        self.move(self.speed)
        print("test2:", self.hitbox.x, self.hitbox.y)


class Enemy(Entity):

    def __init__(self, pos, grups, collision_sprites, image_path="graphic/test/player.png"):
        super().__init__(pos, grups, collision_sprites, image_path)

    def mele_atack(self, directions, ):
        pass

    def range_atack(self, directions, count, speed, range):
        pass


class TestEnemy(Enemy):

    def __init__(self, pos, grups, collision_sprites, image_path="graphic/test/rock.png", player=None):
        super().__init__(pos, grups, collision_sprites, image_path)
        self.ai = ai.create_ai(self, [ai.MovementAI])
        self.player = player
        self.speed = 3

    def mele_atack(self, directions, ):
        pass

    def range_atack(self, directions, count, speed, range):
        pass

    def update(self, *args, **kwargs) -> None:

        if self.player is not None:
            self.ai.set_target(self.player.hitbox.x, self.player.hitbox.y)

        self.move(self.speed)
        self.ai.update()