
import pygame
from config import *

class CollisionManager:
    def __init__(self, player):
        self.player = player

    def can_move(self, target_x, target_y, lanes):
        """
        Check if the target position is blocked by a static obstacle (Tree, Rock).
        Dynamic obstacles (activatable) might also block.
        """
        player_rect = pygame.Rect(target_x + 5, target_y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
        
        # Optimize: Only check lanes near target_y
        for lane in lanes:
            if abs(lane.y - target_y) < TILE_SIZE:
                for entity in lane.entities:
                    # Static obstacles typically have 'tree' in image key or are distinct class
                    # Ideally we check type. 
                    if hasattr(entity, 'image_key') and 'tree' in str(entity.image_key): 
                        if player_rect.colliderect(entity.get_rect()):
                            return False
        return True

    def check_collisions(self, lanes, dt):
        """
        Run every frame. Checks for death conditions or riding logic.
        Returns: 'alive', 'dead', 'drowned', 'hit'
        """
        if self.player.is_moving:
            # While hopping, usually invulnerable to "falling" but vulnerable to "hits"?
            # Crossy Road: You can jump INTO a car and die.
            # You can jump ONTO a log.
            pass

        player_rect = self.player.get_rect()
        # Shrink hitbox slightly for fairness, but not too much preventing log detection
        player_hitbox = player_rect.inflate(-4, -4)
        
        center_y = self.player.y + self.player.height / 2
        
        # Find current lane
        current_lane = None
        for lane in lanes:
            if lane.y <= center_y < lane.y + TILE_SIZE: # strictly, lane.y is top
                current_lane = lane
                break
                
        if not current_lane:
            return 'alive' # Should not happen unless out of bounds logic
            
        # 1. Check Vehicle/Train Collisions (Instant Death)
        if current_lane.type in ['road', 'rail']:
            for entity in current_lane.entities:
                if entity.get_rect().colliderect(player_hitbox):
                    return 'hit'

        # 2. Check River Logic
        if current_lane.type == 'river':
            on_log = False
            log_speed = 0
            
            # Use full player rect for safety checks (easier to land on logs)
            # And slightly inflate log hitbox to be generous
            for entity in current_lane.entities:
                if entity.get_rect().inflate(4, 4).colliderect(player_rect):
                    on_log = True
                    log_speed = entity.speed
                    break
            
            if on_log:
                # Move player with log
                self.player.x += log_speed * dt
                # Ensure player stays in bounds (optional, usually player dies if log goes off screen?)
                # We won't clamp here, but let the player drift off screen (death condition logic elsewhere or camera catchup)
                return 'riding'
            else:
                # If not moving (hopping through air) and not on log -> Drown
                # If we are strictly "in the air" (z > 0), we don't drown yet
                if self.player.z <= 0:
                    return 'drowned'
                    
        return 'alive'
