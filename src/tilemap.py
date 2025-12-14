"""src/tilemap.py"""
import json
from typing import Dict, List, Optional, Tuple

import pygame

# backup kleuren
from src.colors import *


class Tilemap:
    """
    standaard tilegrootte: 48 x 48 pixels.
    ondersteunt nu ook een grote achtergrond afbeelding.
    """

    def __init__(self, tile_size: int = 48) -> None:
        self.tile_size = tile_size

        # alle lagen (foreground is nu weg)
        self.layers: Dict[str, List[List[int]]] = {
            "background": [],
            "collision": [],
        }

        self.map_width: int = 0
        self.map_height: int = 0
        self.walls: List[pygame.Rect] = []

        # hier komt de grote achtergrond afbeelding in
        self.background_image: Optional[pygame.Surface] = None

        # tile-afbeeldingen
        self.tile_images: Dict[int, pygame.Surface] = {}

        # kleuren als een afbeelding niet geladen kan worden
        self.tile_colors: Dict[int, Optional[Tuple[int, int, int]]] = {
            0: None,           # lege tile
            1: (100, 100, 100),  # muur
            2: (139, 69, 19),   # bruine grond
            3: (0, 100, 200),   # water
        }

        self._load_tile_images()

    # afbeeldingen laden
    def _load_tile_images(self) -> None:
        """laad kleine tile-afbeeldingen van schijf."""
        # dit gebruiken we alleen als fallback
        pass

    def load_background_image(self, path: str) -> None:
        """laad de grote 1056x1920 afbeelding."""
        try:
            image = pygame.image.load(path).convert()
            self.background_image = image
            print(f"grote achtergrond geladen: {path}")
        except pygame.error as e:
            print(f"kon achtergrond niet laden: {path} -> {e}")

    # level inladen
    def load_from_file(self, filepath: str) -> None:
        """laad een level data vanuit een json-bestand."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "grid" in data:
                grid = data["grid"]
                self.layers["collision"] = grid
                # background layer maken we leeg want we gebruiken een plaatje
                self.layers["background"] = [] 
            else:
                self.layers = data

            # afmetingen bepalen
            # we kijken naar de collision layer voor de grootte
            collision_layer = self.layers.get("collision", [])
            self.map_height = len(collision_layer)
            self.map_width = len(collision_layer[0]) if collision_layer else 0

            self._generate_walls()
            print(f"map data geladen: {filepath}")

        except Exception as e:
            print(f"fout bij laden map: {e}")

    # collision
    def _generate_walls(self) -> None:
        """maak lijst van muren waar je tegenaan botst."""
        self.walls = []
        grid = self.layers.get("collision", [])

        for y, row in enumerate(grid):
            for x, tile_type in enumerate(row):
                if tile_type == 1: # 1 is een muur
                    rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                    self.walls.append(rect)

    # rendering
    def draw_layer(self, screen, layer_name, camera_x, camera_y):
        """oude functie voor tiles tekenen (fallback)."""
        if layer_name not in self.layers:
            return
        
        grid = self.layers[layer_name]
        for y, row in enumerate(grid):
            for x, tile_type in enumerate(row):
                if tile_type == 0: continue
                
                sx = x * self.tile_size - camera_x
                sy = y * self.tile_size - camera_y

                # alleen tekenen als het in beeld is
                if -self.tile_size < sx < screen.get_width() and -self.tile_size < sy < screen.get_height():
                    # teken logic hier
                    color = self.tile_colors.get(tile_type, (255,0,255))
                    if color:
                         pygame.draw.rect(screen, color, (sx, sy, self.tile_size, self.tile_size))

    def draw_background(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0) -> None:
        """tekent de grote achtergrond afbeelding."""
        if self.background_image:
            # teken de afbeelding op de juiste plek ten opzichte van de camera
            screen.blit(self.background_image, (-camera_x, -camera_y))
        else:
            # als er geen afbeelding is, tekende collision
            self.draw_layer(screen, "collision", camera_x, camera_y)

    # helpers
    def get_tile(self, layer_name, world_x, world_y):
        if layer_name not in self.layers: return None
        grid = self.layers[layer_name]
        gx = int(world_x // self.tile_size)
        gy = int(world_y // self.tile_size)
        if 0 <= gy < self.map_height and 0 <= gx < self.map_width:
            return grid[gy][gx]
        return None