import pygame
import math
import random
from src.colors import *
from .pathfinding import a_star

# src/enemy.py

class Enemy:
    """
    Basis klasse voor alle vijanden in het spel.
    Elke vijand heeft een positie en een staat (idle, chase, attack).
    In plaats van een simpel blok, tekent deze klasse nu 'glitchy' code.
    """
    
    def __init__(self, start_coordinate_x, start_coordinate_y):
        # Startpositie van de vijand (float voor vloeiende beweging)
        self.position_coordinate_x = float(start_coordinate_x)
        self.position_coordinate_y = float(start_coordinate_y)

        # Huidige staat: "idle", "chase", of "attack"
        self.current_state = "idle"

        # Deze moeten door subklassen worden ingesteld
        self.size_width = 0
        self.size_height = 0

        # Initialisatie van font voor het glitch effect
        self.glitch_font = pygame.font.SysFont("Courier", 20, bold=True)
        self.glitch_characters = ["0", "1", "{", "}", ";", "==", "!=", "&&", "||", "=>", "NULL", "ptr"]
        
    def separate_from_other_enemies(self, all_enemies, separation_distance=80):
        """
        Zorgt ervoor dat vijanden elkaar niet overlappen door een afstotende kracht.
        """
        steer_coordinate_x = 0
        steer_coordinate_y = 0
        for other_enemy in all_enemies:
            if other_enemy is self:
                continue
            difference_x = self.position_coordinate_x - other_enemy.position_coordinate_x
            difference_y = self.position_coordinate_y - other_enemy.position_coordinate_y
            distance = math.hypot(difference_x, difference_y)

            if 0 < distance < separation_distance:
                # Hoe dichterbij, hoe sterker de duw weg
                strength = (separation_distance - distance) / separation_distance
                steer_coordinate_x += difference_x * strength * 2.0
                steer_coordinate_y += difference_y * strength * 2.0

        # Pas de sturing toe (met een lege lijst muren voor eenvoud)
        if steer_coordinate_x or steer_coordinate_y:
            self.move(steer_coordinate_x, steer_coordinate_y, 1.0, walls=[])

    def draw_at_position(self, screen, screen_x, screen_y):
        """
        Tekent de vijand als een verzameling glitchy programmeercodes.
        De kleur verandert op basis van de huidige staat van de vijand.
        """
        base_color = {
            "attack": ORANGE,
            "chase": RED,
            "recover": PURPLE,
        }.get(self.current_state, GRAY)

        # Teken een subtiele achtergrond gloed
        glitch_rect = pygame.Rect(screen_x, screen_y, self.size_width, self.size_height)
        subtle_surface = pygame.Surface((self.size_width, self.size_height), pygame.SRCALPHA)
        subtle_surface.fill((*base_color, 40)) # 40 is de transparantie
        screen.blit(subtle_surface, glitch_rect)

        # Teken willekeurige karakters binnen het gebied van de vijand
        for _ in range(random.randint(5, 8)):
            character = random.choice(self.glitch_characters)
            
            # Willekeurige positie binnen de bounding box
            random_offset_x = random.randint(0, self.size_width - 15)
            random_offset_y = random.randint(0, self.size_height - 15)
            
            # Rendert de tekst
            text_surface = self.glitch_font.render(character, True, base_color)
            screen.blit(text_surface, (screen_x + random_offset_x, screen_y + random_offset_y))

        # Voeg af en toe een horizontale glitch-lijn toe
        if random.random() < 0.3:
            line_y = random.randint(0, self.size_height)
            pygame.draw.line(
                screen, 
                WHITE, 
                (screen_x, screen_y + line_y), 
                (screen_x + self.size_width, screen_y + line_y), 
                1
            )
    
    def find_player(self, player_position):
        """
        Bereken de afstand tot de speler en de richting.
        Returns: (distance, difference_x, difference_y).
        """
        player_x, player_y = player_position
        
        difference_x = player_x - self.position_coordinate_x
        difference_y = player_y - self.position_coordinate_y
        
        distance = math.hypot(difference_x, difference_y)
        
        return distance, difference_x, difference_y
    
    def move(self, direction_x, direction_y, speed, walls):
        """
        Beweeg de vijand in een bepaalde richting met muur-detectie.
        """
        distance = math.hypot(direction_x, direction_y)

        if distance > 0:
            move_x = (direction_x / distance) * speed
            move_y = (direction_y / distance) * speed

            if move_x != 0:
                self.position_coordinate_x += move_x
                if self._collides_with_walls(walls):
                    self.position_coordinate_x -= move_x

            if move_y != 0:
                self.position_coordinate_y += move_y
                if self._collides_with_walls(walls):
                    self.position_coordinate_y -= move_y

    def _collides_with_walls(self, walls):
        """Interne check of de vijand een muur raakt."""
        enemy_rectangle = pygame.Rect(
            self.position_coordinate_x,
            self.position_coordinate_y,
            self.size_width,
            self.size_height
        )
        for wall in walls:
            if enemy_rectangle.colliderect(wall):
                return True
        return False


class Dog(Enemy):
    """
    Specifieke vijand 'Dog' die pathfinding gebruikt om de speler te achtervolgen.
    """
    def __init__(self, start_coordinate_x, start_coordinate_y):
        super().__init__(start_coordinate_x, start_coordinate_y)
        
        self.size_width = 80
        self.size_height = 40
        
        self.movement_speed = 2.5
        
        self.player_detection_range = 600
        self.attack_range = 200
        
        # Pathfinding instellingen
        self.current_path = []
        self.current_target_node = None
        self.path_recalculation_timer = 0
        self.path_recalculation_interval = 30  

        # Aanval instellingen
        self.attack_duration_timer = 0
        self.maximum_attack_duration = 20
        self.recovery_timer = 0
        self.maximum_recovery_time = 90

    def update(self, player_position, walls, tile_size=48):
        """
        Hoofd-update van de vijand-logica per frame.
        """
        distance_to_player, difference_x, difference_y = self.find_player(player_position)
        
        self.path_recalculation_timer -= 1
        
        self._update_state_logic(distance_to_player)
        
        # Bereken pad indien nodig
        if self.current_state in ("chase", "attack"):
            if (self.path_recalculation_timer <= 0 or 
                not self.current_path or 
                self._has_reached_target()):
                
                new_path = a_star(
                    start_pos=(self.position_coordinate_x + self.size_width // 2, 
                               self.position_coordinate_y + self.size_height // 2),
                    goal_pos=(player_position[0] + 24, player_position[1] + 46),
                    walls=walls,
                    tile_size=tile_size
                )
                self.current_path = new_path or []
                self.path_recalculation_timer = self.path_recalculation_interval
                self.current_target_node = self.current_path[0] if self.current_path else None

        # Gedrag per staat
        if self.current_state == "idle":
            pass
        elif self.current_state == "recover":
            self._handle_recovery_logic()
        elif self.current_state == "attack":
            self._handle_attack_logic(difference_x, difference_y, walls)
        else: # chase
            self._follow_calculated_path(walls)

    def _update_state_logic(self, distance):
        """Bepaalt de huidige staat op basis van de afstand tot de speler."""
        if self.attack_duration_timer > 0:
            self.current_state = "attack"
            return
        if self.recovery_timer > 0:
            self.current_state = "recover"
            return

        if distance < self.attack_range:
            self.current_state = "attack"
            self.attack_duration_timer = self.maximum_attack_duration
        elif distance < self.player_detection_range:
            self.current_state = "chase"
        else:
            self.current_state = "idle"

    def _follow_calculated_path(self, walls):
        """Beweegt de vijand langs de knooppunten van het A* pad."""
        if not self.current_target_node:
            return

        target_x, target_y = self.current_target_node
        direction_x = target_x - (self.position_coordinate_x + self.size_width // 2)
        direction_y = target_y - (self.position_coordinate_y + self.size_height // 2)
        distance = math.hypot(direction_x, direction_y)

        if distance < 25:
            if self.current_path:
                self.current_path.pop(0)
                self.current_target_node = self.current_path[0] if self.current_path else None
            return

        self.move(direction_x, direction_y, self.movement_speed, walls)

    def _has_reached_target(self):
        """Controleert of de vijand dicht genoeg bij het huidige doel-knooppunt is."""
        if not self.current_target_node:
            return True
        direction_x = self.current_target_node[0] - (self.position_coordinate_x + self.size_width // 2)
        direction_y = self.current_target_node[1] - (self.position_coordinate_y + self.size_height // 2)
        return math.hypot(direction_x, direction_y) < 30

    def _handle_attack_logic(self, difference_x, difference_y, walls):
        """Voert een lunge uit richting de speler tijdens een aanval."""
        lunge_velocity = self.movement_speed * 3
        self.move(difference_x, difference_y, lunge_velocity, walls)
        
        self.attack_duration_timer -= 1
        if self.attack_duration_timer <= 0:
            self.recovery_timer = self.maximum_recovery_time

    def _handle_recovery_logic(self):
        """Telt af tot de vijand weer hersteld is van een aanval."""
        self.recovery_timer -= 1