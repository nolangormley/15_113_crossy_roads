
import pygame
from config import *
from entity import Entity

class Vehicle(Entity):
    def __init__(self, x, y, width, speed, image_key='car'):
        super().__init__(x, y, width, TILE_SIZE - 10)
        self.speed = speed # Pixels per second. Can be negative for leftward movement.
        self.image_key = image_key
        # Adjust color/variant if needed

    def update(self, dt):
        self.x += self.speed * dt
        
        # We don't wrap. The Lane manager handles destroying off-screen entities.

class Train(Vehicle):
    def __init__(self, x, y, speed):
        super().__init__(x, y, TILE_SIZE * 10, speed * 2.5, 'train')
        # Train is much faster
