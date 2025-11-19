# src/tilemap.py
import pygame
import json
from src.colors import *

class Tilemap:
    """
    Tilemap systeem met meerdere layers voor diepte effect.
    Standaard 32*32 pixel tiles.
    Ondersteunt zowel kleuren als tile images.
    """
    
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        
        # Meerdere layers
        self.layers = {   
            'background': [],
            'collision': [],
            'foreground': [],
        }
        
        self.map_width = 0
        self.map_height = 0
        self.walls = []
        
        # Dictionary voor tile images
        self.tile_images = {}
        
        # Kleuren per tile type (fallback als image niet laadt)
        self.tile_colors = {
            0: None,
            1: (100, 100, 100),
            2: (139, 69, 19),
            3: (0, 100, 200),
            4: (34, 139, 34),
            5: (139, 90, 43),
            6: (150, 75, 0),
        }
        
        # Laad tile images
        self._load_tile_images()
    
    def _load_tile_images(self):
        """Laad alle tile images"""
        tile_image_paths = {
            2: "assets/tiles/ground_stone1.png",
        }
        
        for tile_type, image_path in tile_image_paths.items():
            try:
                image = pygame.image.load(image_path)
                scaled_image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                self.tile_images[tile_type] = scaled_image
                print(f"Tile image geladen: {image_path}")
            except pygame.error as e:
                print(f"Kon tile image niet laden: {image_path} - {e}")
                print(f"  Gebruikt fallback kleur voor tile type {tile_type}")
    
    def load_from_file(self, filepath):
        """
        Laad een level vanuit een JSON bestand.
        """
        try:
            with open(filepath, 'r') as file:
                level_data = json.load(file)
                
            if 'grid' in level_data:
                self.layers['collision'] = level_data['grid']
                self.layers['background'] = [[2 for _ in row] for row in level_data['grid']]
                self.layers['foreground'] = [[0 for _ in row] for row in level_data['grid']]
            else:
                self.layers = level_data
            
            first_layer = list(self.layers.values())[0]
            self.map_height = len(first_layer)
            self.map_width = len(first_layer[0]) if first_layer else 0
            
            self._generate_walls()
            print(f"Map geladen: {filepath} ({self.map_width}*{self.map_height} tiles)")
            
        except:
            print(f"Map bestand niet gevonden: {filepath}")

    
    def _generate_walls(self):
        """
        Genereer pygame Rect objecten voor alle tiles.
        """
        self.walls = []
        collision_grid = self.layers.get('collision', [])
        
        for row_index, row in enumerate(collision_grid):
            for col_index, tile_type in enumerate(row):
                if tile_type == 1:
                    wall_rect = pygame.Rect(
                        col_index * self.tile_size,
                        row_index * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    self.walls.append(wall_rect)
    
    def load_from_dict(self, level_data):
        """
        Laad een level met meerdere layers vanuit dict.
        """
        self.layers = level_data
        
        first_layer = list(level_data.values())[0]
        self.map_height = len(first_layer)
        self.map_width = len(first_layer[0]) if first_layer else 0
        
        self._generate_walls()
    
    def draw_layer(self, screen, layer_name, camera_x=0, camera_y=0):
        """Teken een specifieke layer."""
        if layer_name not in self.layers:
            return
        
        grid = self.layers[layer_name]
        
        for row_index, row in enumerate(grid):
            for col_index, tile_type in enumerate(row):
                if tile_type == 0:
                    continue
                
                x = col_index * self.tile_size - camera_x
                y = row_index * self.tile_size - camera_y
                
                # Skip tiles buiten scherm
                if x < -self.tile_size or x > screen.get_width():
                    continue
                if y < -self.tile_size or y > screen.get_height():
                    continue
                
                # Probeer eerst image te tekenen
                if tile_type in self.tile_images:
                    screen.blit(self.tile_images[tile_type], (x, y))
                else:
                    # Fallback naar kleur
                    color = self.tile_colors.get(tile_type, (255, 0, 255))
                    if color:
                        pygame.draw.rect(screen, color, 
                                       (x, y, self.tile_size, self.tile_size))
                        pygame.draw.rect(screen, (0, 0, 0), 
                                       (x, y, self.tile_size, self.tile_size), 1)
    
    def draw_background(self, screen, camera_x=0, camera_y=0):
        """Teken de achtergrond layer."""
        self.draw_layer(screen, 'background', camera_x, camera_y)
    
    def draw_foreground(self, screen, camera_x=0, camera_y=0):
        """Teken de voorgrond layer."""
        self.draw_layer(screen, 'foreground', camera_x, camera_y)
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """
        Backwards compatibility: teken alleen collision layer.
        """
        self.draw_layer(screen, 'collision', camera_x, camera_y)
    
    def get_tile(self, layer_name, x, y):
        """Krijg tile type op een positie."""
        if layer_name not in self.layers:
            return None
        
        grid = self.layers[layer_name]
        grid_x = int(x // self.tile_size)
        grid_y = int(y // self.tile_size)
        
        if 0 <= grid_y < self.map_height and 0 <= grid_x < self.map_width:
            return grid[grid_y][grid_x]
        return None
    
    def is_solid(self, x, y):
        """Check of een positie solid is."""
        tile = self.get_tile('collision', x, y)
        return tile == 1
