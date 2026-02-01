
import pygame
from config import *
from entity import Entity

class Player(Entity):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, TILE_SIZE - 10, TILE_SIZE - 10)
        self.image_key = 'player'
        
        # Movement State
        self.is_moving = False
        self.target_x = self.x
        self.target_y = self.y
        self.move_speed = PLAYER_SPEED # Seconds to complete a hop
        self.move_timer = 0.0
        
        # Logic State
        self.start_x = self.x
        self.start_y = self.y
        self.dead = False
        
        # Visuals
        self.z = 0 # Height for hop
        self.scale_x = 1.0 # Squashing
        self.scale_y = 1.0

    def handle_input(self, input_manager):
        if self.dead or self.is_moving:
            return

        dx = 0
        dy = 0
        
        if input_manager.get_action('up'):
            dy = -TILE_SIZE
        elif input_manager.get_action('down'):
            dy = TILE_SIZE
        elif input_manager.get_action('left'):
            dx = -TILE_SIZE
        elif input_manager.get_action('right'):
            dx = TILE_SIZE
            
        if dx != 0 or dy != 0:
            dest_x = self.target_x + dx
            # Boundary checks
            if 0 <= dest_x <= SCREEN_WIDTH - TILE_SIZE: # Basic screen bounds
                 self.start_move(dest_x, self.target_y + dy)

    def start_move(self, tx, ty):
        self.is_moving = True
        self.move_timer = 0.0
        self.start_x = self.x
        self.start_y = self.y
        self.target_x = tx
        self.target_y = ty
        
        # Audio trigger could go here

    def update(self, dt):
        if self.is_moving:
            self.move_timer += dt
            t = min(1.0, self.move_timer / self.move_speed)
            
            # Linear interpolation for position
            self.x = self.start_x + (self.target_x - self.start_x) * t
            self.y = self.start_y + (self.target_y - self.start_y) * t
            
            # Parabolic arc for hop height (Z)
            # 4 * h * x * (1-x) for parabola 0->1->0
            self.z = 4 * 15 * t * (1 - t) 
            
            if t >= 1.0:
                self.is_moving = False
                self.x = self.target_x
                self.y = self.target_y
                self.z = 0
        
        # Update bounding box
        self.rect = pygame.Rect(self.x + 5, self.y + 5, self.width, self.height)

    def render(self, surface, camera, asset_manager):
        screen_y = camera.apply(self.y)
        
        # Shadow
        shadow_rect = pygame.Rect(self.x + 5, screen_y + self.height - 5, self.width, 10)
        pygame.draw.ellipse(surface, (0,0,0, 100), shadow_rect)
        
        # Player Sprite with Z offset
        draw_y = screen_y - self.z
        
        img = asset_manager.get_image(self.image_key)
        if img:
            # Center horizontally
            draw_x = self.x + (self.width - img.get_width()) // 2
            # Align bottom
            draw_y = screen_y + self.height - img.get_height() - self.z
            surface.blit(img, (draw_x, draw_y))
        else:
            rect = pygame.Rect(self.x, screen_y - self.z, self.width, self.height)
            pygame.draw.rect(surface, (255, 255, 255), rect)

    def die(self):
        self.dead = True
        # Squish animation or particle effect setup
