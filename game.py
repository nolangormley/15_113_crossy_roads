
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
        self.xp = 0
        self.level = 1
        self.next_level_xp = 50
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
                        if dy < 0: 
                             self.score += 1 
                             # Gain XP for moving forward (simulating collecting points)
                             self.xp += 10
                             if self.xp >= self.next_level_xp:
                                 self.xp = 0
                                 self.level += 1
                                 self.next_level_xp = int(self.next_level_xp * 1.5)
                        
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
        # 3D TILT EFFECT
        # We render the entire game world onto a temporary surface first.
        # Then we rotate/scale that surface and blit it to the main screen.
        
        # Buffer size needs to be larger to accommodate rotation without clipping corners
        buffer_width = SCREEN_WIDTH + 400
        buffer_height = SCREEN_HEIGHT + 400
        world_surf = pygame.Surface((buffer_width, buffer_height))
        world_surf.fill(COLOR_BG)
        
        # We need to offset rendering by (buffer_width - SCREEN_WIDTH)/2 to center it on the buffer
        offset_x = 200
        offset_y = 200
        
        # Render Order:
        # 1. Backgrounds of all lanes
        lanes = self.world_generator.get_lanes()
        for lane in lanes:
            # Modified render_background to accept offset? No, we can just shift the context.
            # But the 'camera' applies Y shift. We need X shift manually or modify camera?
            # Easiest: Just modify where we blit.
            # Actually, `lane.render_background` uses `surface.blit`.
            # We can't easily inject offset_x into `render_background` without changing the method signature.
            # Let's create a temporary wrapper or just manually draw here?
            # Re-implementing background drawing here is safer than refactoring everything.
            
            screen_y = self.camera.apply(lane.y) + offset_y
            # Note: We draw WIDER than screen width on the buffer to fill corners after rotation
            # Draw -200 to +200 range
            if -TILE_SIZE < screen_y < buffer_height:
                color = COLOR_GRASS
                if lane.type == 'road': color = COLOR_ROAD
                elif lane.type == 'river': color = COLOR_RIVER
                elif lane.type == 'rail': color = COLOR_RAIL
                if lane.type == 'grass' and lane.index % 2 == 0: color = COLOR_GRASS_LIGHT
                
                rect = pygame.Rect(0, screen_y, buffer_width, TILE_SIZE)
                pygame.draw.rect(world_surf, color, rect)
                
                # Details
                if lane.type == 'road':
                    pygame.draw.line(world_surf, COLOR_ROAD_MARKING, (0, screen_y + TILE_SIZE - 2), (buffer_width, screen_y + TILE_SIZE - 2), 2)
                elif lane.type == 'rail':
                   for i in range(0, buffer_width, 20):
                        pygame.draw.rect(world_surf, COLOR_RAIL_METAL, (i, screen_y + 2, 4, TILE_SIZE - 4))
                   pygame.draw.line(world_surf, COLOR_RAIL_METAL, (0, screen_y + 10), (buffer_width, screen_y + 10), 4)
                   pygame.draw.line(world_surf, COLOR_RAIL_METAL, (0, screen_y + TILE_SIZE - 10), (buffer_width, screen_y + TILE_SIZE - 10), 4)
                   # Warning lights? We'd need to copy logic. Simplified here for now.
                   if getattr(lane, 'train_active', False):
                       c = (255,0,0) if int(pygame.time.get_ticks()/200)%2==0 else (100,0,0)
                       pygame.draw.circle(world_surf, c, (50 + offset_x, screen_y + 5), 5)

        # 2. Gather All Entities
        render_list = []
        render_list.append(self.player)
        for lane in lanes:
            render_list.extend(lane.entities)
            
        render_list.sort(key=lambda e: e.y + e.height + (20 if e == self.player else 0))
        
        for entity in render_list:
            # entity.render uses camera.apply(y). We need to ADD offset_x to x and offset_y to y
            # But render takes (surface, camera, asset_manager).
            # We can temporarily patch the camera? No.
            # We can manually implement render here? Or patching Entity.render is better.
            # Let's adjust entity.x temporarily? No, side effects.
            # Best way: Use a Dummy Camera or just pass absolute position?
            
            # Let's hack it: Just modify the `render` call to support offset?
            # Or manually blit here. Most entities use `asset_manager.get_image`.
            
            screen_y = self.camera.apply(entity.y) + offset_y
            screen_x = entity.x + offset_x
            
             # Draw only if on buffer screen
            if -entity.height < screen_y < buffer_height:
                drawn = False
                if entity.image_key:
                    img = self.asset_manager.get_image(entity.image_key)
                    if img:
                        # Flip if moving left (negative speed)
                        # We assume sprites face RIGHT by default
                        if hasattr(entity, 'speed') and entity.speed < 0:
                            img = pygame.transform.flip(img, True, False)
                        draw_x = screen_x + (entity.width - img.get_width()) // 2
                        draw_y = screen_y + entity.height - img.get_height()
                        
                        # Shadow (Cast on ground)
                        # Shadow logic: Simple black rect/ellipse offset
                        shadow_width = img.get_width()
                        shadow_height = img.get_height() // 4 # Flattened
                        if shadow_height < 5: shadow_height = 5
                        
                        # Create shadow surface
                        s_surf = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
                        pygame.draw.ellipse(s_surf, (0, 0, 0, 80), (0, 0, shadow_width, shadow_height))
                        
                        if hasattr(entity, 'speed') and entity.speed < 0:
                             # Shadow flip might not be needed for ellipse, but for complex shapes yes.
                             # For uniformity, let's leave it unless we use shaped shadows.
                             pass
                        
                        # Position: Bottom of entity + Offset
                        # We want it to look like light is from Top-Left, so shadow falls Bottom-Right
                        # Base Y is screen_y + entity.height
                        
                        sh_x = draw_x + 10 # Offset X
                        sh_y = (screen_y + entity.height) - (shadow_height // 2) + 5 # Offset Y (Ground level)
                        
                        world_surf.blit(s_surf, (sh_x, sh_y))


                        # Player Z
                        if entity == self.player: draw_y -= entity.z
                        
                        world_surf.blit(img, (draw_x, draw_y))
                        drawn = True
                
                if not drawn:
                    rect = pygame.Rect(screen_x, screen_y, entity.width, entity.height)
                    if entity == self.player: rect.y -= entity.z
                    pygame.draw.rect(world_surf, entity.color, rect)


        # TRANSFORM: Rotate 15 degrees and Scale?
        # A simple rotation is enough to give the "isometric" feel if sprites are 2.5D.
        # But Crossy Road is barely rotated, it's mostly orthographic 3D.
        # Pygame can't do real 3D. 
        # But we can rotate the whole screen Z-axis slightly (-5 deg?) no that tilts it sideways.
        # We need X-axis tilt? Pygame handles 2D surfaces.
        # We can't tilt 'into' the screen easily.
        
        # Wait, user asked: "camera is rotated at an angle". 
        # Usually implies Isometric (45 deg Y turn) or just Perspective.
        # Crossy road is ISOMETRIC-like. 
        # To fake Isometric in 2D: Rotate surface 45 degrees.
        
        rotated_surf = pygame.transform.rotate(world_surf, 345) # 15 degrees counter-clockwise
        
        # Center the rotated surface on the main screen
        r_rect = rotated_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
        self.screen.fill(COLOR_BG) # Clear margins
        self.screen.blit(rotated_surf, r_rect)

        # UI (Render normally on top, untransformed)
        self.ui_manager.render_game_ui(self.screen, self.score, self.high_score, self.xp, self.next_level_xp, self.level)

    def update_game_over(self):
        if self.input_manager.get_action('confirm'):
            self.reset_game()
            self.state = 'PLAYING'
            
    def render_game_over(self):
        self.render_playing() # Draw the game frozen
        self.ui_manager.render_game_over(self.screen, self.score, self.high_score)
