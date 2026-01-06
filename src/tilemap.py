"""src/tilemap.py"""
import json
from typing import Dict, List, Optional, Tuple

import pygame

# Importeer de kleurconstanten voor gebruik als fallback
from src.colors import *


class Tilemap:
    """
    Klasse voor het beheren van de spelwereld, inclusief muren, 
    interactieve objecten en de achtergrondafbeelding.
    Standaard tilegrootte is 48 x 48 pixels.
    """

    def __init__(self, tile_size: int = 48) -> None:
        self.tile_size = tile_size

        # Initialiseer de lagen voor de map
        self.layers: Dict[str, List[List[int]]] = {
            "background": [],
            "collision": [],
        }

        self.map_width: int = 0
        self.map_height: int = 0
        self.walls: List[pygame.Rect] = []

        # Variabele voor de grote achtergrondafbeelding
        self.background_image: Optional[pygame.Surface] = None

        # Kleuren die worden gebruikt als er geen afbeelding beschikbaar is
        self.tile_colors: Dict[int, Optional[Tuple[int, int, int]]] = {
            0: None,             # Lege tegel
            1: (100, 100, 100),  # Standaard muur
            2: (139, 69, 19),    # Minigame interactie punt
            3: (200, 200, 0),    # Informatiebord (geel)
        }

    def load_background_image(self, path: str) -> None:
        """
        Laadt een grote afbeelding die als achtergrond voor het level dient.
        """
        try:
            image = pygame.image.load(path).convert()
            self.background_image = image
            print(f"Grote achtergrond succesvol geladen: {path}")
        except pygame.error as error_message:
            print(f"Kon achtergrond niet laden: {path} -> {error_message}")

    def load_from_file(self, file_path: str) -> None:
        """
        Laadt de levelgegevens (het grid) vanuit een JSON-bestand.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file_handle:
                data = json.load(file_handle)

            if "grid" in data:
                grid_data = data["grid"]
                self.layers["collision"] = grid_data
                self.layers["background"] = [] 
            else:
                self.layers = data

            # Bepaal de afmetingen van de map op basis van de collision-laag
            collision_layer = self.layers.get("collision", [])
            self.map_height = len(collision_layer)
            self.map_width = len(collision_layer[0]) if collision_layer else 0

            # Genereer de muren voor collision detectie
            self._generate_walls()
            print(f"Map data succesvol geladen: {file_path}")

        except Exception as error_message:
            print(f"Fout opgetreden bij het laden van de map: {error_message}")

    def _generate_walls(self) -> None:
        """
        Genereert een lijst met pygame.Rect objecten voor alle tegels 
        waar de speler niet doorheen mag lopen (muren, interactiepunten en borden).
        """
        self.walls = []
        grid = self.layers.get("collision", [])

        for y_index, row in enumerate(grid):
            for x_index, tile_type in enumerate(row):
                # Tegel 1: Muur
                # Tegel 2: Minigame Operators (blokkeert ook beweging)
                # Tegel 3: Informatiebord (blokkeert ook beweging)
                # Tegel 4: Minigame Jumper (blokkeert ook beweging)
                # Tegel 5: Minigame Quiz
                # Tegel 9: deur voor de kerk
                if tile_type in (1, 2, 3, 4): 
                    wall_rectangle = pygame.Rect(
                        x_index * self.tile_size,
                        y_index * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                    self.walls.append(wall_rectangle)

    def draw_background(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0) -> None:
        """
        Tekent de achtergrondafbeelding op het scherm, rekening houdend met de camera-positie.
        """
        if self.background_image:
            screen.blit(self.background_image, (-camera_x, -camera_y))
        else:
            # Fallback: teken de muren als gekleurde blokken als de afbeelding ontbreekt
            self.draw_layer(screen, "collision", camera_x, camera_y)

    def draw_layer(self, screen, layer_name, camera_x, camera_y):
        """
        Tekent een specifieke laag tegels. Wordt voornamelijk als fallback gebruikt.
        """
        if layer_name not in self.layers:
            return
        
        grid = self.layers[layer_name]
        for y_index, row in enumerate(grid):
            for x_index, tile_type in enumerate(row):
                if tile_type == 0: 
                    continue
                
                screen_position_x = x_index * self.tile_size - camera_x
                screen_position_y = y_index * self.tile_size - camera_y

                # Teken de tegel alleen als deze binnen het zichtveld van het scherm valt
                if -self.tile_size < screen_position_x < screen.get_width() and \
                   -self.tile_size < screen_position_y < screen.get_height():
                    color = self.tile_colors.get(tile_type, (255, 0, 255))
                    if color:
                        pygame.draw.rect(screen, color, (screen_position_x, screen_position_y, self.tile_size, self.tile_size))

    def get_interaction_tile_info(self, world_coordinate_x, world_coordinate_y, search_radius):
        """
        Zoekt naar interactieve tegels (2, 3, 4 of 9) binnen een straal rondom de speler.
        Geeft het ID en de exacte locatie in het grid terug.
        """
        grid_column_start = int((world_coordinate_x - search_radius) // self.tile_size)
        grid_column_end = int((world_coordinate_x + search_radius) // self.tile_size)
        grid_row_start = int((world_coordinate_y - search_radius) // self.tile_size)
        grid_row_end = int((world_coordinate_y + search_radius) // self.tile_size)

        collision_grid = self.layers.get("collision", [])
        
        for row_index in range(grid_row_start, grid_row_end + 1):
            for column_index in range(grid_column_start, grid_column_end + 1):
                if 0 <= row_index < self.map_height and 0 <= column_index < self.map_width:
                    tile_value = collision_grid[row_index][column_index]
                    
                    if tile_value in (2, 3, 4, 5, 9):
                        return tile_value, row_index, column_index
                        
        return None, None, None

    def get_tile(self, layer_name, world_coordinate_x, world_coordinate_y):
        """
        Geeft de tegelwaarde terug op een specifieke pixelpositie in de wereld.
        """
        if layer_name not in self.layers: 
            return None
        grid = self.layers[layer_name]
        grid_coordinate_x = int(world_coordinate_x // self.tile_size)
        grid_coordinate_y = int(world_coordinate_y // self.tile_size)
        
        if 0 <= grid_coordinate_y < self.map_height and 0 <= grid_coordinate_x < self.map_width:
            return grid[grid_coordinate_y][grid_coordinate_x]
        return None