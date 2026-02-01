
from config import *

class Camera:
    def __init__(self):
        self.scroll_y = 0
        self.target_scroll_y = 0
        self.speed_min = 20 # Minimum creep speed pixels/sec
        
    def update(self, player_y, dt):
        # In Crossy Road, the camera moves up (decreasing Y in screen coords if 0 is top)
        # But let's assume world coordinates: 
        # Y=0 is start, Y increases as we go "forward" (up the screen visually).
        # Standard 2D: Y decreases going up.
        # Let's say Player Start is (TileX, 0).
        # Moving "Forward" means Y decreases (negative).
        # So we want camera to track negative Y.
        
        # We want the player to be roughly at 2/3rds down the screen.
        target = player_y - (SCREEN_HEIGHT * 0.6)
        
        # Smooth follow
        if target < self.scroll_y:
            self.scroll_y += (target - self.scroll_y) * 5 * dt
            
        # Optional: Auto-scroll enforcement (death if off screen)
        # self.scroll_y -= self.speed_min * dt

    def apply(self, y):
        return y - self.scroll_y
