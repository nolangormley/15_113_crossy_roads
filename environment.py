
import pygame
from config import *
from entity import Entity

class Obstacle(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.image_key = 'tree'
        # Hitbox might be smaller than visual
        
class Log(Entity):
    def __init__(self, x, y, width, speed):
        super().__init__(x, y, width, TILE_SIZE)
        self.image_key = 'log_medium'
        if width < TILE_SIZE * 2.5: self.image_key = 'log_small'
        elif width > TILE_SIZE * 3.5: self.image_key = 'log_large'
        
        self.speed = speed

    def update(self, dt):
        self.x += self.speed * dt
