
import pygame
from config import *

class UIManager:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        
    def render_game_ui(self, surface, score, high_score, xp=0, next_xp=100, level=1):
        # Top Left: Score
        score_surf = self.asset_manager.fonts['score'].render(str(score), True, (255, 255, 255))
        # Add shadow
        shadow_surf = self.asset_manager.fonts['score'].render(str(score), True, (0, 0, 0))
        surface.blit(shadow_surf, (22, 22))
        surface.blit(score_surf, (20, 20))
        
        # High Score
        hs_text = f"HI {high_score}"
        hs_surf = self.asset_manager.fonts['main'].render(hs_text, True, (255, 255, 0))
        surface.blit(hs_surf, (20, 70))
        
        # Experience Bar (Top Center)
        bar_width = 300
        bar_height = 30
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 20
        
        # Border
        border_rect = pygame.Rect(bar_x - 4, bar_y - 4, bar_width + 8, bar_height + 8)
        pygame.draw.rect(surface, (0, 0, 0), border_rect, border_radius=5)
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (50, 50, 50), bg_rect, border_radius=5)
        
        # Fill
        if next_xp > 0:
            fill_pct = min(1.0, xp / next_xp)
            fill_width = int(bar_width * fill_pct)
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            pygame.draw.rect(surface, (255, 50, 50), fill_rect, border_radius=5)
            
        # Label "EXP" (Right of bar)
        exp_surf = self.asset_manager.fonts['main'].render("EXP", True, (255, 200, 0))
        surface.blit(exp_surf, (bar_x + bar_width + 10, bar_y))
        
        # Level (Left of bar)
        lvl_surf = self.asset_manager.fonts['main'].render(f"LVL {level}", True, (255, 255, 255))
        surface.blit(lvl_surf, (bar_x - lvl_surf.get_width() - 10, bar_y))
        
    def render_game_over(self, surface, score, high_score):
        # Darken screen
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Game Over Text
        go_surf = self.asset_manager.fonts['gameover'].render("GAME OVER", True, (255, 255, 255))
        go_rect = go_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        surface.blit(go_surf, go_rect)
        
        # Score
        score_surf = self.asset_manager.fonts['score'].render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        surface.blit(score_surf, score_rect)
        
        # Restart Prompt
        prompt_surf = self.asset_manager.fonts['main'].render("Press ENTER to Restart", True, (200, 200, 200))
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80))
        surface.blit(prompt_surf, prompt_rect)
