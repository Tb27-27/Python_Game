# src/player.py
import pygame
from src.colors import BLUE, LIGHT_BLUE

class Player:
    """Speler met beweging, collision, health en interactie"""
    
    def __init__(self, start_x, start_y):
        # start pos en hoogte
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        self.size_width = 48
        self.size_height = 92
        
        # regels
        self.move_speed = 2
        self.health = 100
        self.max_health = 100
        self.inventory = []
    
    def move(self, delta_x, delta_y, walls):
        """Beweeg speler met aparte X- en Y-collision (geen 'tunneling')"""
        
        # Probeer eerst horizontaal te bewegen
        if delta_x != 0:
            self.pos_x += delta_x
            if self._collides_with_walls(walls):
                self.pos_x -= delta_x
        
        # Dan verticaal
        if delta_y != 0:
            self.pos_y += delta_y
            if self._collides_with_walls(walls):
                self.pos_y -= delta_y
    
    def _collides_with_walls(self, walls):
        """Interne helper: check of player rect een muur raakt"""
        player_rect = pygame.Rect(
            self.pos_x, 
            self.pos_y, 
            self.size_width, 
            self.size_height
        )
        for wall in walls:
            if player_rect.colliderect(wall):
                return True
        return False
    
    def take_damage(self, amount):
        """Neem schade en zorg dat health nooit onder 0 komt"""
        self.health = max(0, self.health - amount)
    
    def heal(self, amount):
        """Herstel health, maar nooit boven maximum"""
        self.health = min(self.max_health, self.health + amount)
    
    def interact(self):
        """Interactie met objecten/deur/NPC (uit te breiden)"""
        print("[Interact] Player probeert iets te doen!")
    
    def draw(self, screen):
        """Teken de speler als blauwe rechthoek (zonder camera offset)"""
        player_rect = pygame.Rect(
            int(self.pos_x),
            int(self.pos_y),
            self.size_width,
            self.size_height
        )
        pygame.draw.rect(screen, LIGHT_BLUE, player_rect)
        pygame.draw.rect(screen, BLUE, player_rect, width=2)
    
    def draw_at_position(self, screen, x, y):
        """Teken de speler op een specifieke scherm positie (voor camera)"""
        player_rect = pygame.Rect(
            int(x),
            int(y),
            self.size_width,
            self.size_height
        )
        pygame.draw.rect(screen, LIGHT_BLUE, player_rect)
        pygame.draw.rect(screen, BLUE, player_rect, width=2)