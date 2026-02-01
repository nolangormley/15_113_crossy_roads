
import pygame
import sys
from config import *
from asset_manager import AssetManager
from input_manager import InputManager
from camera import Camera
from player import Player
from world_generator import WorldGenerator
from collision_manager import CollisionManager
from ui import UIManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.asset_manager = AssetManager.get_instance()
        self.asset_manager.load_assets()
        
        self.input_manager = InputManager()
        self.ui_manager = UIManager(self.asset_manager)
        
        self.state = 'MENU' # MENU, PLAYING, GAMEOVER
        self.score = 0
        self.high_score = 0
        
        self.reset_game()
        
    def reset_game(self):
        # Initialize Game World
        self.player = Player(SCREEN_WIDTH // 2, 0)
        self.camera = Camera()
        self.world_generator = WorldGenerator()
        self.collision_manager = CollisionManager(self.player)
        self.score = 0
        self.max_y = 0 # To track forward progress

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0 # Delta time in seconds
            self.input_manager.update()
            
            if self.input_manager.get_action('quit'):
                pygame.quit()
                sys.exit()
                
            if self.state == 'MENU':
                self.update_menu()
                self.render_menu()
            elif self.state == 'PLAYING':
                self.update_playing(dt)
                self.render_playing()
            elif self.state == 'GAMEOVER':
                self.update_game_over()
                self.render_game_over()
                
            pygame.display.flip()
            
    def update_menu(self):
        if self.input_manager.get_action('confirm'):
            self.reset_game()
            self.state = 'PLAYING'
            
    def render_menu(self):
        self.screen.fill(COLOR_BG)
        # Reuse Game Over style or simple start text
        title_surf = self.asset_manager.fonts['gameover'].render(TITLE, True, (255, 255, 255))
        rect = title_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        self.screen.blit(title_surf, rect)
        
        sub_surf = self.asset_manager.fonts['main'].render("Press ENTER to Start", True, (255, 255, 255))
        rect2 = sub_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(sub_surf, rect2)

    def update_playing(self, dt):
        # 1. Update Player Input
        # Note: Player checks inputs internally but we need to validate "Can I move there?"
        # The Player class `handle_input` handles "intent". 
        # We need to inject collision logic *before* move starts or *during* move?
        # My Player class starts moving immediately on input. 
        # I should probably modify Player to ask Game/CollisionManager "Can I move?" 
        # Or better: Player sets target, Game checks target valid. 
        # BUT, to keep it modular, let's let Player choose target, but we revert/block if invalid?
        # Re-reading Player: It calculates `dest_x`. It does not check obstacles.
        # Let's override player input handling here or pass collision manager to player.
        pass
        
        # Let's handle input explicitly here for blocking logic OR pass manager.
        # Ideally Player shouldn't know about World, but input needs to know.
        
        # HACK: Modifying Player to accept external validation is cleaner.
        # For now, let's just let Player move and if he hits a tree, he bounces back? 
        # No, "Clipping" -> blocked.
        
        # Let's peek at input 
        dx, dy = 0, 0
        if not self.player.is_moving and not self.player.dead:
            if self.input_manager.get_action('up'): dy = -TILE_SIZE
            elif self.input_manager.get_action('down'): dy = TILE_SIZE
            elif self.input_manager.get_action('left'): dx = -TILE_SIZE
            elif self.input_manager.get_action('right'): dx = TILE_SIZE
            
            if dx != 0 or dy != 0:
                tx = self.player.x + dx
                ty = self.player.y + dy
                # 1. Check Bounds
                if 0 <= tx <= SCREEN_WIDTH - self.player.width:
                    # 2. Check Static Obstacles
                    if self.collision_manager.can_move(tx, ty, self.world_generator.get_lanes()):
                        self.player.start_move(tx, ty)
                        if dy < 0: self.score += 1 # Only score on forward move? 
                        # Actually score is max distance.
                        
        # Update World (Lane spawning)
        self.player.update(dt)
        if abs(self.player.y) > self.max_y:
            self.max_y = abs(self.player.y)
            self.score = int(self.max_y / TILE_SIZE)

        self.camera.update(self.player.y, dt)
        self.world_generator.update(self.camera.scroll_y, dt)
        
        # Update Collisions
        status = self.collision_manager.check_collisions(self.world_generator.get_lanes(), dt)
        if status in ['hit', 'drowned']:
            self.player.die()
            self.state = 'GAMEOVER'
            if self.score > self.high_score:
                self.high_score = self.score
                
        # Update Camera bounds check (if player falls off screen)
        # Player Y is negative. Camera scroll_y is negative.
        # Bottom of screen is scroll_y + SCREEN_HEIGHT.
        # If player.y > scroll_y + SCREEN_HEIGHT -> Death
        if self.player.y > self.camera.scroll_y + SCREEN_HEIGHT + TILE_SIZE: # Buffer
             self.player.die()
             self.state = 'GAMEOVER'
             if self.score > self.high_score:
                self.high_score = self.score

    def render_playing(self):
        self.screen.fill(COLOR_BG)
        
        # Render Order:
        # 1. Backgrounds of all lanes
        lanes = self.world_generator.get_lanes()
        for lane in lanes:
            lane.render_background(self.screen, self.camera)
            
        # 2. Gather All Entities
        render_list = []
        
        # Add Player
        render_list.append(self.player)
        
        # Add Lane Entities
        for lane in lanes:
            render_list.extend(lane.entities)
            
        # Sort by Y position (Painter's Algorithm) regarding the bottom of the sprite
        # For 2D top down, usually higher Y (lower on screen) draws LAST (on top).
        # We need to sort by `y + height`.
        # Note: Player Z affects draw position but not sort order (usually).
        # Actually in Crossy Road, a jumping player is "above" the car locally but still behind the tree in front.
        # Standard Y-sorting works well.
        # Add slight bias to Player to ensure they draw ON TOP of logs/ground at same Y
        render_list.sort(key=lambda e: e.y + e.height + (5 if e == self.player else 0))
        
        for entity in render_list:
            entity.render(self.screen, self.camera, self.asset_manager)
            
        # UI
        self.ui_manager.render_game_ui(self.screen, self.score, self.high_score)

    def update_game_over(self):
        if self.input_manager.get_action('confirm'):
            self.reset_game()
            self.state = 'PLAYING'
            
    def render_game_over(self):
        self.render_playing() # Draw the game frozen
        self.ui_manager.render_game_over(self.screen, self.score, self.high_score)
