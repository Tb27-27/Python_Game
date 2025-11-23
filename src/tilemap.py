"""src/tilemap.py"""
import json
from typing import Dict, List, Optional, Tuple

import pygame

from src.colors import *  # Zorg dat dit bestand bestaat of vervang door expliciete kleuren


class Tilemap:
    """
    Standaard tilegrootte: 48 x 48 pixels.
    Ondersteunt zowel afbeeldingen als fallback-kleuren per tile-type.
    """

    def __init__(self, tile_size: int = 48) -> None:
        self.tile_size = tile_size

        # Meerdere lagen
        self.layers: Dict[str, List[List[int]]] = {
            "background": [],
            "collision": [],
            "foreground": [],
        }

        self.map_width: int = 0
        self.map_height: int = 0
        self.walls: List[pygame.Rect] = []

        # Cache voor geladen tile-afbeeldingen
        self.tile_images: Dict[int, pygame.Surface] = {}

        # Fallback-kleuren als een afbeelding niet geladen kan worden
        self.tile_colors: Dict[int, Optional[Tuple[int, int, int]]] = {
            0: None,           # Lege tile
            1: (100, 100, 100),  # Muur
            2: (139, 69, 19),   # Bruine grond
            3: (0, 100, 200),   # Water
            4: (34, 139, 34),   # Gras
            5: (139, 90, 43),   # Zand
            6: (150, 75, 0),    # Hout
        }

        self._load_tile_images()

    # Afbeeldingen laden
    def _load_tile_images(self) -> None:
        """Laad tile-afbeeldingen van schijf (met fallback naar kleur)."""
        tile_image_paths = {
            2: "assets/tiles/ground_stone1.png",
            # Voeg hier later meer tiles toe
        }

        for tile_type, path in tile_image_paths.items():
            try:
                image = pygame.image.load(path).convert_alpha()
                scaled = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                self.tile_images[tile_type] = scaled
                print(f"Tile-afbeelding geladen: {path}")
            except pygame.error as e:
                print(f"Kon tile niet laden: {path} → {e}")
                print(f"  → Gebruik fallback-kleur voor tile type {tile_type}")

    # Level inladen
    def load_from_file(self, filepath: str) -> None:
        """Laad een level vanuit een JSON-bestand."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Oude single-layer structuur ondersteunen
            if "grid" in data:
                grid = data["grid"]
                h, w = len(grid), len(grid[0]) if grid else 0
                self.layers["collision"] = grid
                self.layers["background"] = [[2 for _ in row] for row in grid]
                self.layers["foreground"] = [[0 for _ in row] for row in grid]
            else:
                self.layers = data

            # Afmetingen bepalen
            first_layer = next(iter(self.layers.values()))
            self.map_height = len(first_layer)
            self.map_width = len(first_layer[0]) if first_layer else 0

            self._generate_walls()
            print(f"Map geladen: {filepath} → {self.map_width}×{self.map_height} tiles")

        except FileNotFoundError:
            print(f"Map-bestand niet gevonden: {filepath}")
        except json.JSONDecodeError as e:
            print(f"JSON-fout in {filepath}: {e}")
        except Exception as e:
            print(f"Onverwachte fout bij laden van {filepath}: {e}")

    def load_from_dict(self, level_data: Dict[str, List[List[int]]]) -> None:
        """Laad een level direct vanuit een dictionary (meerdere layers)."""
        self.layers = level_data

        first_layer = next(iter(level_data.values()))
        self.map_height = len(first_layer)
        self.map_width = len(first_layer[0]) if first_layer else 0

        self._generate_walls()

    # Collision handling
    def _generate_walls(self) -> None:
        """Genereer een lijst van pygame.Rect objecten voor alle solide tiles."""
        self.walls = []
        grid = self.layers.get("collision", [])

        for y, row in enumerate(grid):
            for x, tile_type in enumerate(row):
                if tile_type == 1:  # 1 = solide muur
                    rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                    self.walls.append(rect)

    # Rendering
    def draw_layer(
        self,
        screen: pygame.Surface,
        layer_name: str,
        camera_x: float = 0,
        camera_y: float = 0,
    ) -> None:
        """Teken een specifieke layer met camera-offset."""
        if layer_name not in self.layers:
            return

        grid = self.layers[layer_name]

        for y, row in enumerate(grid):
            for x, tile_type in enumerate(row):
                if tile_type == 0:
                    continue

                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y

                # Culling: tiles buiten beeld overslaan
                if (
                    screen_x < -self.tile_size
                    or screen_x > screen.get_width()
                    or screen_y < -self.tile_size
                    or screen_y > screen.get_height()
                ):
                    continue

                # Eerst proberen afbeelding te tekenen
                if tile_type in self.tile_images:
                    screen.blit(self.tile_images[tile_type], (screen_x, screen_y))
                else:

                    # Fallback: gekleurde rechthoek
                    color = self.tile_colors.get(tile_type, (255, 0, 255))  # magenta = missing
                    if color:
                        pygame.draw.rect(screen, color, (screen_x, screen_y, self.tile_size, self.tile_size))
                        pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, self.tile_size, self.tile_size), 1)

    def draw_background(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0) -> None:
        self.draw_layer(screen, "background", camera_x, camera_y)

    def draw_foreground(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0) -> None:
        self.draw_layer(screen, "foreground", camera_x, camera_y)

    # Backwards compatibility
    def draw(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0) -> None:
        """Oude methode – tekent alleen de collision layer (voor bestaande code)."""
        self.draw_layer(screen, "collision", camera_x, camera_y)

    # Query functies
    def get_tile(self, layer_name: str, world_x: float, world_y: float) -> Optional[int]:
        """Retourneer het tile-type op een wereldpositie."""
        if layer_name not in self.layers:
            return None

        grid = self.layers[layer_name]
        grid_x = int(world_x // self.tile_size)
        grid_y = int(world_y // self.tile_size)

        if 0 <= grid_y < self.map_height and 0 <= grid_x < self.map_width:
            return grid[grid_y][grid_x]
        return None

    def is_solid(self, world_x: float, world_y: float) -> bool:
        """Controleer of een wereldpositie solide is (gebaseerd op collision layer)."""
        tile = self.get_tile("collision", world_x, world_y)
        return tile == 1