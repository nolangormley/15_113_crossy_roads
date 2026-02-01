
import pygame
from config import *

class UIManager:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        
    def render_game_ui(self, surface, score, high_score):
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
