import pygame
from src.robot_vision import RobotVision
from src.tiles import BLOCKING_TILES
from . import bullet

SPEED = 1


class Robot:
    def __init__(self, index: int, position) -> None:
        self._bottom_tile = pygame.image.load(f'images/{index}_b.png')
        self._top_tile = pygame.image.load(f'images/{index}_t.png')
        self._left_tile = pygame.image.load(f'images/{index}_l.png')
        self._right_tile = pygame.image.load(f'images/{index}_r.png')
        self._dead_tile = pygame.image.load('images/bomb_after.png')

        self.facing = 'r'  # t, b, l, r
        self.position = position
        self.can_move_forward = True
        self.health = 1000
        self.state = {}

    def get_tile(self):
        if self.health <= 0:
            return self._dead_tile
        
        return {
            'b': self._bottom_tile,
            'r': self._right_tile,
            't': self._top_tile,
            'l': self._left_tile,
        }[self.facing]

    def move_forward(self):
        if not self.can_move_forward or self.health <= 0:
            return

        if self.facing == 'b': 
            self.position[1] += 1
        if self.facing == 't':
            self.position[1] -= 1
        if self.facing == 'l':
            self.position[0] -= 1
        if self.facing == 'r':
            self.position[0] += 1

    def turn_left(self):
        self.facing = {
            't': 'l',
            'l': 'b',
            'b': 'r',
            'r': 't',
        }[self.facing]

    def turn_right(self):
        self.facing = {
            't': 'r',
            'r': 'b',
            'b': 'l',
            'l': 't',
        }[self.facing]

    def get_facing(self):
        return self.facing
    
    def move_on(self):
        return None
    
    def shoot(self):
        starting_position = [self.position[0], self.position[1]]
        if self.facing == 'b': 
            starting_position[1] += 32
        if self.facing == 't':
            starting_position[1] -= 32
        if self.facing == 'l':
            starting_position[0] -= 32
        if self.facing == 'r':
            starting_position[0] += 32
        return bullet.Bullet(starting_position, self.facing)

    def think(self, surrounding_tiles):
        if self.get_facing() == 'r' and surrounding_tiles[1][2] == 1:
            return self.turn_right
    
        return self.move_forward

    def get_surrounding_tiles(self, TILES_X, TILES_Y, tilemap):
        surrounding_tiles = []
        directions = [(-1, -1), (0, -1), (1, -1),   # (0, 0) (1, 0) (2, 0)
                      (-1, 0), (0, 0), (1, 0),      # (0, 1) (1, 1) (2, 1)
                      (-1, 1), (0, 1), (1, 1)]      # (0, 2) (1, 2) (2, 2)

        x_tile = self.position[0] // 32
        y_tile = self.position[1] // 32
        for dx, dy in directions:
            x, y = int((self.position[0]) // 32) + dx, int((self.position[1]) // 32) + dy

            if 0 <= x < TILES_X and 0 <= y < TILES_Y:
                surrounding_tiles.append(tilemap[y][x])
            else:
                surrounding_tiles.append(1)
    
        surrounding_tiles = [surrounding_tiles[0:3], surrounding_tiles[3:6], surrounding_tiles[6:9]]
        
        vision = RobotVision()
        vision.top_left = surrounding_tiles[0][0]
        vision.top = surrounding_tiles[0][1]
        vision.top_right = surrounding_tiles[0][2]
        vision.left = surrounding_tiles[1][0]
        vision.current_tile = surrounding_tiles[1][1]
        vision.right = surrounding_tiles[1][2]
        vision.bottom_left = surrounding_tiles[2][0]
        vision.bottom = surrounding_tiles[2][1]
        vision.bottom_right = surrounding_tiles[2][2]

        vision.current_tiles_x_y = (int(self.position[0] // 32), int(self.position[1] // 32))
            
        return vision
