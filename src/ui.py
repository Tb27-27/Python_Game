import pygame
from src.colors import *

class UI:
    # UI class voor health bar en inventory
    
    HEALTH_BAR_WIDTH = 200
    HEALTH_BAR_HEIGHT = 30
    HEALTH_BAR_X = 20
    HEALTH_BAR_Y = 20
    TEXT_OFFSET_X = 10
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen, player):
        # Teken alle UI elementen
        self.draw_health_bar(screen, player)
        self.draw_inventory(screen, player)
    
    def draw_health_bar(self, screen, player):
        # Teken de health bar linksboven
        # Achtergrond van health bar (rood)
        # TODO: Watch tutorial on Resident Evil Heartbeat Health system
        bar_width = self.HEALTH_BAR_WIDTH
        bar_height = self.HEALTH_BAR_HEIGHT
        x = self.HEALTH_BAR_X
        y = self.HEALTH_BAR_Y
        
        pygame.draw.rect(screen, DARK_RED, (x, y, bar_width, bar_height))
        
        # Health (groen)
        health_percentage = player.health / player.max_health
        current_bar_width = int(bar_width * health_percentage)
        pygame.draw.rect(screen, GREEN, (x, y, current_bar_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # Health tekst
        # TODO: Heel lelijk
        health_text = self.font.render(f"HP: {player.health}/{player.max_health}", True, (255, 255, 255))
        screen.blit(health_text, (x + bar_width + self.TEXT_OFFSET_X, y))
    
    def draw_inventory(self, screen, player):
        # Teken inventory
        # TODO: Inventory komt in het pauze scherm later
        # TODO: Inventory counter redundant
        inv_text = self.font.render(f"Items: {len(player.inventory)}", True, (255, 255, 255))
        screen.blit(inv_text, (20, 60))