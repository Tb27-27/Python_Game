# Main.py
import pygame
import sys
from src.player import Player
from src.enemy import Dog
from src.tilemap import Tilemap
from src.light_system import LightSystem
from src.ui import UI
from src.colors import *

pygame.init()

GAME_CONFIG = {
    "game_width": 1440,
    "game_height": 960,
    "screen_width": 1440,
    "screen_height": 960,
    "target_fps": 60,
    "game_title": "Pythy",
    "tile_size": 48,
    "scale_factor": 1
}

class Camera:
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.camera_x = 0
        self.camera_y = 0

        # Camera deadzone box (player can move within this area without camera moving)
        self.deadzone_width = 400
        self.deadzone_height = 300

        # Calculate deadzone boundaries (relative to screen edges)
        self.deadzone_left = (game_width - self.deadzone_width) // 2
        self.deadzone_right = (game_width + self.deadzone_width) // 2
        self.deadzone_top = (game_height - self.deadzone_height) // 2
        self.deadzone_bottom = (game_height + self.deadzone_height) // 2

    def follow_player(self, player, map_width_px, map_height_px):
        """Follow player with deadzone box, confined to map boundaries"""
        # Calculate player center in world coordinates
        player_center_x = player.pos_x + player.size_width // 2
        player_center_y = player.pos_y + player.size_height // 2

        # Calculate player position on screen
        player_screen_x = player_center_x - self.camera_x
        player_screen_y = player_center_y - self.camera_y

        # Horizontal deadzone logic
        if player_screen_x < self.deadzone_left:
            self.camera_x = player_center_x - self.deadzone_left
        elif player_screen_x > self.deadzone_right:
            self.camera_x = player_center_x - self.deadzone_right

        # Vertical deadzone logic
        if player_screen_y < self.deadzone_top:
            self.camera_y = player_center_y - self.deadzone_top
        elif player_screen_y > self.deadzone_bottom:
            self.camera_y = player_center_y - self.deadzone_bottom

        # Clamp camera to map boundaries
        self.camera_x = max(0, min(self.camera_x, map_width_px - self.game_width))
        self.camera_y = max(0, min(self.camera_y, map_height_px - self.game_height))
    
    def apply_to_position(self, x, y):
        return x - self.camera_x, y - self.camera_y
    
    def apply_to_rect(self, rect):
        return pygame.Rect(
            rect.x - self.camera_x,
            rect.y - self.camera_y,
            rect.width,
            rect.height
        )

class Game:
    def __init__(self):
        self.display_window = pygame.display.set_mode(
            (GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"])
        )
        pygame.display.set_caption(GAME_CONFIG["game_title"])
        
        self.game_surface = pygame.Surface(
            (GAME_CONFIG["game_width"], GAME_CONFIG["game_height"])
        )
        
        self.game_clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = False
        
        self.player_character = Player(256, 144)
        self.enemy_list = [Dog(200, 100), Dog(350, 200)]
        
        # Load map with 48x48 tiles
        self.game_map = Tilemap(tile_size=GAME_CONFIG["tile_size"])
        self.game_map.load_from_file("assets/maps/cathedral_1.json")
        
        self.camera = Camera(
            GAME_CONFIG["game_width"],
            GAME_CONFIG["game_height"]
        )
        
        self.lighting_system = LightSystem(
            GAME_CONFIG["game_width"],
            GAME_CONFIG["game_height"],
            light_radius=250
        )
        self.user_interface = UI(
            GAME_CONFIG["game_width"], 
            GAME_CONFIG["game_height"]
        )
        
        self.depth_sorted_objects = []

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
        dx = dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.player_character.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.player_character.move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.player_character.move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.player_character.move_speed
        
        self.player_character.move(dx, dy, self.game_map.walls)
        self.player_character.update()

        # Calculate map dimensions in pixels
        map_width_px = self.game_map.map_width * self.game_map.tile_size
        map_height_px = self.game_map.map_height * self.game_map.tile_size

        self.camera.follow_player(self.player_character, map_width_px, map_height_px)

        player_pos = (self.player_character.pos_x, self.player_character.pos_y)

        for enemy in self.enemy_list:
            enemy.update(
                player_pos, 
                self.game_map.walls,
                tile_size=self.game_map.tile_size
            )

            enemy.separate_from_other_enemies(
                self.enemy_list, 
                separation_distance=90
            )
            
            if self.detect_collision(self.player_character, enemy):
                self.player_character.take_damage(10)
        
        if self.player_character.health <= 0:
            self.game_over()
        
        self.depth_sorted_objects = [self.player_character] + self.enemy_list
        self.depth_sorted_objects.sort(key=lambda obj: obj.pos_y)

    def detect_collision(self, obj1, obj2):
        return (
            obj1.pos_x < obj2.pos_x + obj2.size_width and
            obj1.pos_x + obj1.size_width > obj2.pos_x and
            obj1.pos_y < obj2.pos_y + obj2.size_height and
            obj1.pos_y + obj1.size_height > obj2.pos_y
        )

    def draw(self):
        self.game_surface.fill(DARK_GRAY)
        
        # --- LAYERS ---
        self.game_map.draw_background(
            self.game_surface, 
            self.camera.camera_x, 
            self.camera.camera_y
        )

        self.game_map.draw(
            self.game_surface, 
            self.camera.camera_x, 
            self.camera.camera_y
        )
        
        for obj in self.depth_sorted_objects:
            sx, sy = self.camera.apply_to_position(obj.pos_x, obj.pos_y)
            obj.draw_at_position(self.game_surface, sx, sy)
        
        self.game_map.draw_foreground(
            self.game_surface, 
            self.camera.camera_x,
            self.camera.camera_y
        )
        
        px, py = self.camera.apply_to_position(
            self.player_character.pos_x,
            self.player_character.pos_y
        )
        
        self.lighting_system.apply_lighting(
            self.game_surface,
            (px, py),
            (self.player_character.size_width, self.player_character.size_height)
        )
        
        self.user_interface.draw(self.game_surface, self.player_character)
        
        if self.is_paused:
            self.draw_pause_screen()
        
        # --- IMPORTANT: NO UPSCALING ANYMORE ---
        self.display_window.blit(self.game_surface, (0, 0))
        pygame.display.flip()

    def draw_pause_screen(self):
        overlay = pygame.Surface(
            (GAME_CONFIG["game_width"], GAME_CONFIG["game_height"])
        )
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.game_surface.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 36)
        text = font.render("PAUSED", True, WHITE)
        rect = text.get_rect(center=(GAME_CONFIG["game_width"] // 2, GAME_CONFIG["game_height"] // 2))
        self.game_surface.blit(text, rect)

    def game_over(self):
        self.game_surface.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", True, RED)
        rect = text.get_rect(center=(GAME_CONFIG["game_width"] // 2, GAME_CONFIG["game_height"] // 2))
        self.game_surface.blit(text, rect)

        self.display_window.blit(self.game_surface, (0, 0))
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
