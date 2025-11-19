import pygame
import math
from src.colors import *

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
    
    def draw(self, screen):
        """
        Teken de vijand op het scherm. Kleur hangt af van de staat.
        """

        # Replace with Images
        color = RED if self.current_state == "chase" else GRAY
        pygame.draw.rect(
            screen, 
            color, 
            (self.pos_x, self.pos_y, self.size_width, self.size_height)
        )
    
    def draw_at_position(self, screen, x, y):
        """Teken de vijand op een specifieke scherm positie (voor camera)"""
        color = RED if self.current_state == "chase" else GRAY
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
    
    def move(self, dx, dy, speed):
        """
        Beweeg de vijand in een bepaalde richting.
        dx, dy = richting vector (wordt genormaliseerd)
        speed = snelheid in pixels per frame
        """

        # Bereken lengte van de richting vector
        distance = math.hypot(dx, dy)
        
        # Voorkom delen door 0
        if distance > 0:

            # richting  vermenigvuldig met snelheid
            self.pos_x += (dx / distance) * speed
            self.pos_y += (dy / distance) * speed
    
    def update(self, player_position, walls):
        """
        Update de vijand elke frame.
        Deze methode moet worden overschreven door subs.
        """
        pass


class Dog(Enemy):
    """
    Dog vijand: Achtervolgt de speler en valt aan met een lunge aanval.
    """
    
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        
        # Afmetingen van de hond (aangepast voor 32*32 tiles)
        self.size_width = 24
        self.size_height = 16
        
        # Bewegingssnelheid
        self.move_speed = 1.0
        
        # Afstanden voor detectie en aanval
        self.player_detection_range = 150 
        self.attack_range = 40
        
        # Aanval systeem
        self.attack_cooldown = 0
        # HOE LANG de aanval duurt
        self.attack_duration = 0  
        self.attacking = False
    
    def update(self, player_position, walls):
        """
        Update de hond elke frame:
        - Bepaal afstand tot speler
        - Kies juiste staat (idle/chase/attack)
        - Voer beweging uit
        """
        # Gebruik de findPlayer methode om afstand en richting te krijgen
        distance, dx, dy = self.findPlayer(player_position)
        
        # === STAAT BEPALEN ===
        self._determine_state(distance)
        
        # === GEDRAG PER STAAT ===
        if self.current_state == "idle":
            self._handle_idle_state()
        elif self.current_state == "chase":
            self._handle_chase_state(dx, dy)
        elif self.current_state == "attack":
            self._handle_attack_state(dx, dy)
    
    def _determine_state(self, distance):
        """Bepaal de staat op basis van afstand tot speler."""
        # Als de hond nog aan het aanvallen is (attack_duration > 0), blijf in attack state
        if self.attack_duration > 0:
            self.current_state = "attack"
        # Check of de hond dichtbij genoeg is EN niet in cooldown
        elif distance < self.attack_range and self.attack_cooldown <= 0:
            self.current_state = "attack"
        elif distance < self.player_detection_range and not self.attacking:
            self.current_state = "chase"
        else:
            self.current_state = "idle"
    
    def _handle_idle_state(self):
        """Gedrag tijdens idle staat: cooldown verlagen."""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Reset attacking flag als cooldown voorbij is
        if self.attack_cooldown <= 0:
            self.attacking = False
    
    def _handle_chase_state(self, dx, dy):
        """Gedrag tijdens chase staat: beweeg richting speler."""
        # Gebruik de move methode om richting speler te bewegen
        self.move(dx, dy, self.move_speed)
    
    def _handle_attack_state(self, dx, dy):
        """Gedrag tijdens attack staat: lunge aanval richting speler."""
        # Start de aanval (alleen de eerste keer)
        if self.attack_duration == 0:
            self.attack_duration = 15
            self.attacking = True
        
        # Lunge: 3x snellere beweging
        lunge_speed = self.move_speed * 3
        self.move(dx, dy, lunge_speed)
        
        # Verlaag attack duration
        self.attack_duration -= 1
        
        # Als de aanval klaar is, start de cooldown
        if self.attack_duration <= 0:
            self.attack_cooldown = 120
            self.attacking = True