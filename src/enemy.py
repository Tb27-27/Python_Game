import pygame
import math
from src.colors import *
from .pathfinding import a_star

# src/enemy.py

class Enemy:
    """
    Basis klasse voor alle vijanden in het spel.
    Elke vijand heeft een positie en een staat (idle, chase, attack).
    """
    
    def __init__(self, start_x, start_y):
        # Startpositie van de vijand (float voor vloeiende beweging)
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)

        # Huidige staat: "idle", "chase", of "attack"
        self.current_state = "idle"

        # Deze moeten door subklassen worden ingesteld
        self.size_width = 0
        self.size_height = 0
        
    def separate_from_other_enemies(self, all_enemies, separation_distance=80):
        """
        Simple separation steering: push away from nearby enemies
        """
        steer_x = 0
        steer_y = 0
        for other in all_enemies:
            if other is self:
                continue
            dx = self.pos_x - other.pos_x
            dy = self.pos_y - other.pos_y
            distance = math.hypot(dx, dy)

            if 0 < distance < separation_distance:
                # Closer = stronger push
                strength = (separation_distance - distance) / separation_distance
                steer_x += dx * strength * 2.0
                steer_y += dy * strength * 2.0

        # Apply the steering (with wall collision check)
        if steer_x or steer_y:
            self.move(steer_x, steer_y, 1.0, walls=[])

    def draw(self, screen):
        """Kleur afhankelijk van state o"""
        if self.current_state == "attack":
            color = ORANGE
        elif self.current_state == "chase":
            color = RED
        elif self.current_state == "recover":
            color = PURPLE
        else:  # idle
            color = GRAY
        pygame.draw.rect(
            screen,
            color,
            (self.pos_x, self.pos_y, self.size_width, self.size_height)
        )

    def draw_at_position(self, screen, x, y):
        color = {
            "attack": ORANGE,
            "chase": RED,
            "recover": PURPLE,
        }.get(self.current_state, GRAY)
        pygame.draw.rect(
            screen,
            color,
            (x, y, self.size_width, self.size_height)
        )
    
    def findPlayer(self, player_position):
        """
        Bereken de afstand tot de speler en de richting.
        Returns: (distance, dx, dy). afstand en richting vectoren
        """
        player_x, player_y = player_position
        
        # Bereken verschil in X en Y richting
        dx = player_x - self.pos_x
        dy = player_y - self.pos_y
        
        # Bereken totale afstand met Pythagoras
        distance = math.hypot(dx, dy)
        
        return distance, dx, dy
    
    def move(self, dx, dy, speed, walls):
        """
        Beweeg de vijand in een bepaalde richting met wall collision.
        dx, dy = richting vector (wordt genormaliseerd)
        speed = snelheid in pixels per frame
        walls = lijst van pygame.Rect objecten voor collision
        """

        # Bereken lengte van de richting vector
        distance = math.hypot(dx, dy)

        # Voorkom delen door 0
        if distance > 0:
            # Normaliseer richting en vermenigvuldig met snelheid
            move_x = (dx / distance) * speed
            move_y = (dy / distance) * speed

            # Probeer eerst horizontaal te bewegen
            if move_x != 0:
                self.pos_x += move_x
                if self._collides_with_walls(walls):
                    self.pos_x -= move_x

            # Dan verticaal
            if move_y != 0:
                self.pos_y += move_y
                if self._collides_with_walls(walls):
                    self.pos_y -= move_y

    def _collides_with_walls(self, walls):
        """Check of enemy rect een muur raakt"""
        enemy_rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.size_width,
            self.size_height
        )
        for wall in walls:
            if enemy_rect.colliderect(wall):
                return True
        return False
    
    def update(self, player_position, walls):
        """
        Update de vijand elke frame.
        Deze methode moet worden overschreven door subs.
        """
        pass


class Dog(Enemy):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        
        self.size_width = 100
        self.size_height = 50
        
        self.move_speed = 2.5
        
        self.player_detection_range = 600
        self.attack_range = 200
        
        # Pathfinding
        self.path = []
        self.current_target = None
        self.path_recalc_timer = 0
        # 30 frames = 0.5 seconden
        self.path_recalc_interval = 30  

        # Attack timers
        self.attack_duration = 0
        self.max_attack_duration = 20
        self.recovery_time = 0
        self.max_recovery_time = 90

    def update(self, player_position, walls, tile_size=48):
        distance, dx, dy = self.findPlayer(player_position)
        
        self.path_recalc_timer -= 1
        
        # attack / sleep / etc. gebasseerd op asfstand van spelen
        self._update_state(distance)
        
        # path calculatiosn
        if self.current_state in ("chase", "attack"):
            if (self.path_recalc_timer <= 0 or 
                not self.path or 
                self._reached_current_target()):
                
                # HIER ZAT DE FOUT:
                path = a_star(
                    start_pos=(self.pos_x + self.size_width//2, self.pos_y + self.size_height//2),
                    goal_pos=(player_position[0] + 24, player_position[1] + 46),
                    walls=walls,
                    tile_size=tile_size
                )
                self.path = path or []
                self.path_recalc_timer = self.path_recalc_interval
                self.current_target = self.path[0] if self.path else None

        # behaviour state
        if self.current_state == "idle":
            pass
        elif self.current_state == "recover":
            self._handle_recovery()
        elif self.current_state == "attack":
            self._handle_attack(dx, dy, walls)
        else:  # chase
            self._follow_path(walls)

    def _update_state(self, distance):
        # attacking na cooldown
        if self.attack_duration > 0:
            self.current_state = "attack"
            return
        if self.recovery_time > 0:
            self.current_state = "recover"
            return

        # als je dichtbij bent chace of attack
        if distance < self.attack_range:
            self.current_state = "attack"
            self.attack_duration = self.max_attack_duration
        elif distance < self.player_detection_range:
            self.current_state = "chase"
        else:
            self.current_state = "idle"

    def _follow_path(self, walls):
        if not self.current_target:
            return

        tx, ty = self.current_target
        dx = tx - (self.pos_x + self.size_width // 2)
        dy = ty - (self.pos_y + self.size_height // 2)
        dist = math.hypot(dx, dy)

        if dist < 25:
            if self.path:
                self.path.pop(0)
                self.current_target = self.path[0] if self.path else None
            return

        self.move(dx, dy, self.move_speed, walls)

    def _reached_current_target(self):
        if not self.current_target:
            return True
        dx = self.current_target[0] - (self.pos_x + self.size_width // 2)
        dy = self.current_target[1] - (self.pos_y + self.size_height // 2)
        return math.hypot(dx, dy) < 30

    def _handle_attack(self, dx, dy, walls):
        # lunge naar player zonder pathfinding, moet een rechte attack zijn
        lunge_speed = self.move_speed * 3
        self.move(dx, dy, lunge_speed, walls)
        
        self.attack_duration -= 1
        if self.attack_duration <= 0:
            self.recovery_time = self.max_recovery_time

    def _handle_recovery(self):
        self.recovery_time -= 1