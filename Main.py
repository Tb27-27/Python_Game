import pygame
import sys
from src.player import Player
from src.enemy import Enemy
from src.map import Map
from src.light_system import LightSystem
from src.ui import UI
from src.colors import * 

pygame.init()

GAME_CONFIG = {
    "screen_width": 1600,
    "screen_height": 800,
    "target_fps": 60,
    "game_title": "Pythy - Survival Horror"
}

class Game:
    def __init__(self):
        self.game_window = pygame.display.set_mode((GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"]))
        pygame.display.set_caption(GAME_CONFIG["game_title"])
        self.game_clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = False
        
        self.player_character = Player(350, 250)
        self.enemy_list = [Enemy(100, 100), Enemy(800, 400)]
        self.game_map = Map("assets/maps/cathedral_1.json")
        self.lighting_system = LightSystem(GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"])
        self.user_interface = UI(GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = not self.is_paused
                if event.key in (pygame.K_e, pygame.K_SPACE):
                    self.player_character.interact()

    def update(self):
        if self.is_paused:
            return
        
        keys = pygame.key.get_pressed()
        movement_delta_x = movement_delta_y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement_delta_x -= self.player_character.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movement_delta_x += self.player_character.move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movement_delta_y -= self.player_character.move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movement_delta_y += self.player_character.move_speed
        
        self.player_character.move(movement_delta_x, movement_delta_y, self.game_map.walls)
        
        player_world_position = (self.player_character.pos_x, self.player_character.pos_y)
        for current_enemy in self.enemy_list:
            current_enemy.update(player_world_position, self.game_map.walls)
            if self.detect_collision(self.player_character, current_enemy):
                self.player_character.take_damage(1)
        
        if self.player_character.health <= 0:
            self.game_over()

    def detect_collision(self, obj1, obj2):
        return (
            obj1.pos_x < obj2.pos_x + obj2.size_width and
            obj1.pos_x + obj1.size_width > obj2.pos_x and
            obj1.pos_y < obj2.pos_y + obj2.size_height and
            obj1.pos_y + obj1.size_height > obj2.pos_y
        )

    def draw(self):
        self.game_window.fill(DARK_GRAY)
        self.game_map.draw(self.game_window)
        for enemy in self.enemy_list:
            enemy.draw(self.game_window)
        self.player_character.draw(self.game_window)
        self.lighting_system.apply_lighting(self.game_window, (self.player_character.pos_x, self.player_character.pos_y))
        self.user_interface.draw(self.game_window, self.player_character)
        if self.is_paused:
            self.draw_pause_screen()
        pygame.display.flip()

    def draw_pause_screen(self):
        overlay = pygame.Surface((GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"]))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.game_window.blit(overlay, (0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(GAME_CONFIG["screen_width"] // 2, GAME_CONFIG["screen_height"] // 2))
        self.game_window.blit(text, text_rect)

    def game_over(self):
        self.game_window.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(GAME_CONFIG["screen_width"] // 2, GAME_CONFIG["screen_height"] // 2))
        self.game_window.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        self.is_running = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.game_clock.tick(GAME_CONFIG["target_fps"])
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()