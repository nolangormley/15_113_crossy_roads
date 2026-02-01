
import pygame
from config import *

class Entity:
    def __init__(self, x, y, width, height, color=(255,0,255)):
        self.x = x # World coordinate X
        self.y = y # World coordinate Y (row * TILE_SIZE usually)
        self.width = width
        self.height = height
        self.color = color
        self.active = True
        self.image_key = None # For AssetManager
        
        # Grid coordinates (optional, for logic)
        self.grid_x = int(x / TILE_SIZE)
        self.grid_y = int(y / TILE_SIZE)

    def update(self, dt):
        pass

    def render(self, surface, camera, asset_manager):
        # Calculate screen position
        screen_y = camera.apply(self.y)
        
        # Draw only if on screen (culling)
        if -self.height < screen_y < SCREEN_HEIGHT:
            drawn = False
            if self.image_key:
                img = asset_manager.get_image(self.image_key)
                if img:
                    # Align bottom of sprite with bottom of entity collision box
                    # screen_y is top of entity. screen_y + self.height is bottom.
                    draw_y = screen_y + self.height - img.get_height()
                    draw_x = self.x + (self.width - img.get_width()) // 2
                    surface.blit(img, (draw_x, draw_y))
                    drawn = True
            
            if not drawn:
                rect = pygame.Rect(self.x, screen_y, self.width, self.height)
                pygame.draw.rect(surface, self.color, rect)
                
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
