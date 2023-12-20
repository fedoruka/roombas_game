import pygame


bullet_image = pygame.image.load('images/bullet.png')


class Bullet:
    def __init__(self, position, facing):
        self.position = position
        self.facing = facing
        self.speed = 5
        self.active = True

    def move(self):
        if not self.active:
            return

        if self.facing == 'b': 
            self.position[1] += self.speed
        if self.facing == 't':
            self.position[1] -= self.speed
        if self.facing == 'l':
            self.position[0] -= self.speed
        if self.facing == 'r':
            self.position[0] += self.speed

    def draw(self, window):
        if self.active:
            window.blit(bullet_image, self.position)
