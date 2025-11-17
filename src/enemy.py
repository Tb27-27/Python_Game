import pygame
import math
from src.colors import *

# src/enemy.py
class Enemy:
    def __init__(self, start_x, start_y):
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        self.size_width = 60
        self.size_height = 100
        self.move_speed = 2
        self.current_state = "idle"
        self.player_detection_range = 300

    def update(self, player_position, walls):
        player_x, player_y = player_position
        distance = math.hypot(self.pos_x - player_x, self.pos_y - player_y)
        
        self.current_state = "chase" if distance < self.player_detection_range else "idle"
        
        if self.current_state == "chase":
            dx = player_x - self.pos_x
            dy = player_y - self.pos_y
            length = math.hypot(dx, dy)
            if length > 0:
                self.pos_x += (dx / length) * self.move_speed
                self.pos_y += (dy / length) * self.move_speed

    def draw(self, screen):
        color = RED if self.current_state == "chase" else GRAY
        pygame.draw.rect(screen, color, 
                         (self.pos_x, self.pos_y, self.size_width, self.size_height))