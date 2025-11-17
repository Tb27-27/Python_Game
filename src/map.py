import pygame
from src.colors import *

class Map:
    # Map class met walls en tiles
    
    def __init__(self, map_file=None):
        self.tiles = []
        self.walls = []
        
        # Laad de ground texture
        try:
            self.ground_texture = pygame.image.load("assets/tiles/ground_stone1.png")
        except:
            print("Waarschuwing: ground_stone1.png niet gevonden, gebruik fallback kleur")
            self.ground_texture = None
        
        # Maak een simpele test map met muren
        self.create_test_map()
    
    def create_test_map(self):
        # maak een simpele test map met muren rondom

        # Buitenmuren (bovenkant, onderkant, links, rechts)
        self.walls = [
            pygame.Rect(0, 0, 1600, 50),      # Bovenkant
            pygame.Rect(0, 750, 1600, 50),    # Onderkant
            pygame.Rect(0, 0, 50, 800),       # Links
            pygame.Rect(1550, 0, 50, 800),    # Rechts
            
            # Wat binnenste muren voor obstakels
            pygame.Rect(400, 200, 200, 50),
            pygame.Rect(800, 400, 50, 200),
        ]
    
    def load_map(self, map_file):
        # Laad map vanuit JSON (later implementeren)
        pass
    
    def draw(self, screen):
        # Teken de ground texture en alle muren
        # Teken de ground texture als achtergrond
        if self.ground_texture:
            # Tile de texture over het hele scherm
            texture_width = self.ground_texture.get_width()
            texture_height = self.ground_texture.get_height()
            
            for x in range(0, 1600, texture_width):
                for y in range(0, 800, texture_height):
                    screen.blit(self.ground_texture, (x, y))
        else:
            # Fallback: grijze achtergrond als texture niet gevonden is
            screen.fill((60, 60, 60))
        
        # Teken alle muren
        for wall in self.walls:
            pygame.draw.rect(screen, GRAY, wall)
