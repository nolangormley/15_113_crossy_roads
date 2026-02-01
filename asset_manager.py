
import pygame
from config import *

class AssetManager:
    _instance = None
    
    def __init__(self):
        self.fonts = {}
        self.sounds = {}
        self.images = {}
        
    @staticmethod
    def get_instance():
        if AssetManager._instance is None:
            AssetManager._instance = AssetManager()
        return AssetManager._instance

    def load_assets(self):
        pygame.font.init()
        # Default font
        self.fonts['main'] = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonts['score'] = pygame.font.SysFont("Impact", 40)
        self.fonts['gameover'] = pygame.font.SysFont("Arial Black", 50)
        
        # In a real build with assets, we'd load images here.
        # Since we are creating a clone from code, we will generate procedural sprites.
        self._generate_sprites()
        
        # Audio - placeholders using pygame.mixer specific generation or empty
        # We will assume sound files exist or use simple beep generation if possible,
        # but for now we'll setup the dictionary.
        # Real implementation would load .wav files.
        pass

    def _generate_sprites(self):
        # Helper to draw a "3D" block (Top + Front view)
        def draw_block(surface, x, y, width, height, depth, color):
            # Colors
            c_top = tuple(min(255, c * 1.2) for c in color)
            c_front = color
            c_side = tuple(max(0, c * 0.8) for c in color)
            
            # Layout: Top face sits on top of Front face
            # y is the top-left coordinate of the TOP face
            
            # Top Face
            pygame.draw.rect(surface, c_top, (x, y, width, depth))
            # Front Face
            pygame.draw.rect(surface, c_front, (x, y + depth, width, height))
            # Side (Right) - Optional fake perspective if we wanted
            # pygame.draw.rect(surface, c_side, (x + width, y + depth, 5, height))

        def create_surface(width, height):
             return pygame.Surface((width, height), pygame.SRCALPHA)

        # Player (Chicken)
        # Dimensions: 30w, 30d (top), 30h (front)?
        # Total surface size needed
        s_player = create_surface(40, 50)
        # Legs
        pygame.draw.rect(s_player, (255, 140, 0), (10, 35, 5, 10))
        pygame.draw.rect(s_player, (255, 140, 0), (25, 35, 5, 10))
        # Body (White) - 30x20 front, 15 depth
        draw_block(s_player, 5, 5, 30, 25, 10, (255, 255, 255)) 
        # Wing
        pygame.draw.rect(s_player, (220, 220, 220), (3, 20, 3, 10)) # Left
        pygame.draw.rect(s_player, (220, 220, 220), (34, 20, 3, 10)) # Right
        # Beak
        draw_block(s_player, 16, 20, 8, 4, 4, (255, 180, 0))
        # Comb (Red)
        draw_block(s_player, 16, 0, 4, 4, 5, (255, 0, 0))
        # Eyes
        pygame.draw.rect(s_player, (0,0,0), (32, 20, 2, 4)) # Right Eye (Side view ish)
        pygame.draw.rect(s_player, (0,0,0), (6, 20, 2, 4))  # Left Eye
        
        self.images['player'] = s_player

        # Car
        def make_car(color):
            s = create_surface(70, 50) 
            # Wheels
            pygame.draw.rect(s, (20,20,20), (10, 35, 10, 8))
            pygame.draw.rect(s, (20,20,20), (50, 35, 10, 8))
            # Body
            draw_block(s, 0, 15, 70, 20, 15, color)
            # Cabin
            draw_block(s, 10, 5, 40, 10, 10, (150, 210, 255))
            return s
            
        self.images['car'] = make_car((220, 50, 50))
        self.images['car_blue'] = make_car((50, 50, 220)) # Variant?

        # Log
        def make_log(width):
            s = create_surface(width, 40)
            color = (139, 69, 19)
            # Top/Side
            draw_block(s, 0, 5, width, 25, 10, color)
            # End detail
            pygame.draw.rect(s, (100, 50, 10), (0, 15, 5, 25))
            pygame.draw.rect(s, (100, 50, 10), (width-5, 15, 5, 25))
            return s
            
        self.images['log_small'] = make_log(TILE_SIZE * 2)
        self.images['log_medium'] = make_log(TILE_SIZE * 3)
        self.images['log_large'] = make_log(TILE_SIZE * 4)

        # Tree
        s_tree = create_surface(40, 80)
        # Trunk
        draw_block(s_tree, 12, 50, 16, 20, 5, (101, 67, 33))
        # Leaves layers
        draw_block(s_tree, 0, 35, 40, 15, 10, (34, 139, 34))
        draw_block(s_tree, 5, 20, 30, 15, 10, (40, 160, 40))
        draw_block(s_tree, 10, 5, 20, 15, 10, (50, 180, 50))
        self.images['tree'] = s_tree
        
        # Train
        def make_train():
            s = create_surface(TILE_SIZE * 10, 50)
            color = (60, 60, 60)
            draw_block(s, 0, 10, TILE_SIZE * 10, 35, 10, color)
            # Windows
            for i in range(20, TILE_SIZE * 10, 40):
                pygame.draw.rect(s, (255, 255, 0), (i, 25, 20, 10))
            return s
        self.images['train'] = make_train()

    def get_image(self, name):
        return self.images.get(name, None)
        
    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
