import pygame
import math
from src.colors import *

# src/enemy.py
class Enemy:
    def __init__(self, start_x, start_y):
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        self.current_state = "idle"

    # All enemies need to be drawn 
    def draw(self, screen):
        color = RED if self.current_state == "chase" else GRAY
        pygame.draw.rect(screen, color, 
                         (self.pos_x, self.pos_y, self.size_width, self.size_height))
        
    # All enemies need to know where the player is compared to them
    # TODO: Implement
    def findPlayer(self):
        print("find player")

    # All enemies have the ability to move (but don't always) 
    # TODO: Implement
    def move (self, speed):
        print("move")
        
    # All enemies need to update themselves to see what they do
    def update(self):
        print("Every enemy needs to update themselves")

class Dog(Enemy):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.size_width = 100
        self.size_height = 40
        self.move_speed = 2
        self.player_detection_range = 300
        self.attack_range = 10
        self.attack_cooldown = 0
        self.attacking = False

    def update(self, player_position, walls):
        player_x, player_y = player_position
        distance = math.hypot(self.pos_x - player_x, self.pos_y - player_y)
        
        if distance < self.attack_range and self.attack_cooldown <= 0:
            self.current_state = "attack"
        elif distance < self.player_detection_range and self.attack_cooldown <= 0 and self.attacking == False:
            self.current_state = "chase"
        else:
            self.current_state = "idle"
        # TODO: Don't repeat yourself

        if self.current_state == "idle":
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            if self.attack_cooldown  <= 0:
                self.attacking = False

        if self.current_state == "chase":
            dx = player_x - self.pos_x
            dy = player_y - self.pos_y
            length = math.hypot(dx, dy)
            if length > 0:
                self.pos_x += (dx / length) * self.move_speed
                self.pos_y += (dy / length) * self.move_speed
                self.attack_cooldown -= 1

        # TODO: Fix Lunge
        if self.current_state == "attack":
            dx = player_x - self.pos_x
            dy = player_y - self.pos_y
            length = math.hypot(dx, dy)
            if length < 0:
                self.pos_x += (dx / length) * self.move_speed * 5
                self.pos_y += (dy / length) * self.move_speed * 5
                self.attack_cooldown = 10
                self.attacking = True

