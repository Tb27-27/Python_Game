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
    "game_width": 512,
    "game_height": 288,
    "screen_width": 1280,
    "screen_height": 720,
    "target_fps": 60,
    "game_title": "Pythy",
    "tile_size": 32,
    "scale_factor": 2.5
}

class Camera:
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.camera_x = 0
        self.camera_y = 0
    
    def follow_player(self, player):
        """Camera volgt de speler, gecentreerd op het scherm"""
        self.camera_x = player.pos_x + player.size_width // 2 - self.game_width // 2
        self.camera_y = player.pos_y + player.size_height // 2 - self.game_height // 2
    
    def apply_to_position(self, x, y):
        """Converteer wereld positie naar scherm positie"""
        return x - self.camera_x, y - self.camera_y
    
    def apply_to_rect(self, rect):
        """Pas camera offset toe op een pygame Rect"""
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
        
        # Game surface is klein (16*9 tiles = 512*288)
        self.game_surface = pygame.Surface(
            (GAME_CONFIG["game_width"], GAME_CONFIG["game_height"])
        )
        
        self.game_clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = False
        
        self.player_character = Player(256, 144)
        self.enemy_list = [Dog(200, 100), Dog(350, 200)]
        
        # Laad de map met 32*32 tiles
        self.game_map = Tilemap(tile_size=GAME_CONFIG["tile_size"])
        self.game_map.load_from_file("assets/maps/cathedral_1.json")
        
        # Camera systeem (werkt op game surface grootte)
        self.camera = Camera(
            GAME_CONFIG["game_width"],
            GAME_CONFIG["game_height"]
        )
        
        self.lighting_system = LightSystem(
            GAME_CONFIG["game_width"], 
            GAME_CONFIG["game_height"],
            light_radius=120
        )
        self.user_interface = UI(
            GAME_CONFIG["game_width"], 
            GAME_CONFIG["game_height"]
        )
        
        # Lijst voor objecten die depth sorting nodig hebben
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
        movement_delta_x = movement_delta_y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement_delta_x -= self.player_character.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movement_delta_x += self.player_character.move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movement_delta_y -= self.player_character.move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movement_delta_y += self.player_character.move_speed
        
        self.player_character.move(
            movement_delta_x, 
            movement_delta_y, 
            self.game_map.walls
        )
        
        # Update camera om speler te volgen
        self.camera.follow_player(self.player_character)
        
        player_world_position = (
            self.player_character.pos_x, 
            self.player_character.pos_y
        )
        
        for current_enemy in self.enemy_list:
            current_enemy.update(player_world_position, self.game_map.walls)
            if self.detect_collision(self.player_character, current_enemy):
                self.player_character.take_damage(1)
        
        if self.player_character.health <= 0:
            self.game_over()
        
        # Update depth sorted objects lijst
        self.depth_sorted_objects = [self.player_character] + self.enemy_list
        # Sorteer op Y positie (objecten lager op scherm worden later getekend)
        self.depth_sorted_objects.sort(key=lambda obj: obj.pos_y)

    def detect_collision(self, obj1, obj2):
        return (
            obj1.pos_x < obj2.pos_x + obj2.size_width and
            obj1.pos_x + obj1.size_width > obj2.pos_x and
            obj1.pos_y < obj2.pos_y + obj2.size_height and
            obj1.pos_y + obj1.size_height > obj2.pos_y
        )

    def draw(self):
        # Teken alles op de kleine game surface
        self.game_surface.fill(DARK_GRAY)
        
        # === LAAG 1: ACHTERGROND ===
        self.game_map.draw_background(
            self.game_surface, 
            self.camera.camera_x, 
            self.camera.camera_y
        )
        
        # === LAAG 2: COLLISION LAYER (optioneel, voor zichtbaarheid) ===
        # self.game_map.draw(self.game_surface, self.camera.camera_x, self.camera.camera_y)
        
        # === LAAG 3: SPELER EN ENEMIES (met depth sorting en camera offset) ===
        for obj in self.depth_sorted_objects:
            screen_x, screen_y = self.camera.apply_to_position(obj.pos_x, obj.pos_y)
            obj.draw_at_position(self.game_surface, screen_x, screen_y)
        
        # === LAAG 4: VOORGROND ===
        self.game_map.draw_foreground(
            self.game_surface, 
            self.camera.camera_x, 
            self.camera.camera_y
        )
        
        # === LAAG 5: LIGHTING (met camera offset) ===
        screen_player_x, screen_player_y = self.camera.apply_to_position(
            self.player_character.pos_x, 
            self.player_character.pos_y
        )
        self.lighting_system.apply_lighting(
            self.game_surface, 
            (screen_player_x, screen_player_y)
        )
        
        # === LAAG 6: UI (altijd bovenop, geen camera offset) ===
        self.user_interface.draw(self.game_surface, self.player_character)
        
        if self.is_paused:
            self.draw_pause_screen()
        
        # === UPSCALE: Schaal game surface naar display window ===
        scaled_surface = pygame.transform.scale(
            self.game_surface,
            (GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"])
        )
        self.display_window.blit(scaled_surface, (0, 0))
        
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
        text_rect = text.get_rect(
            center=(
                GAME_CONFIG["game_width"] // 2, 
                GAME_CONFIG["game_height"] // 2
            )
        )
        self.game_surface.blit(text, text_rect)

    def game_over(self):
        self.game_surface.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(
            center=(
                GAME_CONFIG["game_width"] // 2, 
                GAME_CONFIG["game_height"] // 2
            )
        )
        self.game_surface.blit(text, text_rect)
        
        # Upscale voor display
        scaled_surface = pygame.transform.scale(
            self.game_surface,
            (GAME_CONFIG["screen_width"], GAME_CONFIG["screen_height"])
        )
        self.display_window.blit(scaled_surface, (0, 0))
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