from settings import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from tile import Tile
from random import randint


class MovementAI:

    def __init__(self, entity):

        self.entity = entity
        self.target = (self.entity.hitbox.x, self.entity.hitbox.y)
        self.temp_target = None
        self.last_pos = (self.entity.hitbox.x, self.entity.hitbox.y)
        self.finder = AStarFinder()
        self.map_matrix = [[int(not cell) for cell in row] for row in MAP]
        self.target_disctance = 1

    def set_target(self, x, y) -> None:
        if self.temp_target is None:
            self.target = (x, y)

    def get_angle(self, x1, y1, x2, y2) -> float:
        dx, dy = x2 - x1, y2 - y1
        angle = math.atan2(dy, dx)
        angle = math.degrees(angle)

        return angle

    def target_condition(self) -> bool:
        return not (math.sqrt(abs(self.entity.hitbox.x - self.target[0])**2 + abs(self.entity.hitbox.y - self.target[1])**2) <= self.target_disctance)

    def avoid_wall(self, x, y) -> None:

        path = self.find_path(x, y)

        if len(path) > 1:
            self.temp_target = (path[1][0] * TILE_SIZE + 1, path[1][1] * TILE_SIZE + 1)
        else:
            self.temp_target = None

    def find_path(self, x, y) -> list[tuple[int, int]]:
        grid = Grid(matrix=self.map_matrix)

        x1, y1, x2, y2 = x // TILE_SIZE, y // TILE_SIZE, self.target[0] // TILE_SIZE, self.target[1] // TILE_SIZE
        start = grid.node(x1, y1)
        end = grid.node(x2, y2)

        path, _ = self.finder.find_path(start, end, grid)

        return path

    def move(self) -> None:

        x, y = self.entity.hitbox.x, self.entity.hitbox.y
        tx, ty = self.target

        if self.target_condition():
            if abs(x - self.last_pos[0]) < 2 and abs(y - self.last_pos[1]) < 2:
                angle = randint(0, 360)
                self.entity.rotate(angle)

            else:

                if self.entity.check_collsions() or self.temp_target is not None:
                    self.avoid_wall(x, y)

                    if self.temp_target is not None:
                        tx, ty = self.temp_target

                        angle = self.get_angle(x, y, tx, ty)
                        self.entity.rotate(angle)

                else:

                    angle = self.get_angle(x, y, tx, ty)

                    self.entity.rotate(angle)

            self.last_pos = (x, y)

        else:
            self.temp_target = None
            self.entity.direction.x, self.entity.direction.y = False, False

    def update(self, *args, **kwargs) -> None:
        self.move()


def create_ai(
    entity,
    ai_list: list[type] = [],
):

    class AI(*ai_list):

        def __init__(self):
            self.entity = entity
            super(AI, self).__init__(self.entity)

        def update(self, *args, **kwargs) -> None:
            super(AI, self).update(*args, **kwargs)

    return AI()