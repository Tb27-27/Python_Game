# Main.py
import pygame
import sys
from src.player import Player
from src.enemy import Dog
from src.tilemap import Tilemap
from src.light_system import LightSystem
from src.ui import UI
from src.colors import *
from src.minigame import *


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

        # camera deadzone size
        self.deadzone_width = 400
        self.deadzone_height = 300

        # camera deadzone boundaries
        self.deadzone_left = (game_width - self.deadzone_width) // 2
        self.deadzone_right = (game_width + self.deadzone_width) // 2
        self.deadzone_top = (game_height - self.deadzone_height) // 2
        self.deadzone_bottom = (game_height + self.deadzone_height) // 2

    def follow_player(self, player, map_width_pixels, map_height_pixels):
        """
        Zorgt ervoor dat de camera de speler volgt met een deadzone. 
        Alle variabelen zijn volledig uitgeschreven om verwarring te voorkomen.
        """
        # Bereken het exacte middelpunt van de speler in de spelwereld
        player_center_coordinate_x = player.position_coordinate_x + player.size_width // 2
        player_center_coordinate_y = player.position_coordinate_y + player.size_height // 2

        # Bepaal waar de speler zich bevindt op het scherm (relatief aan de camera)
        player_screen_coordinate_x = player_center_coordinate_x - self.camera_x
        player_screen_coordinate_y = player_center_coordinate_y - self.camera_y

        # Controleer horizontale deadzone grenzen
        if player_screen_coordinate_x < self.deadzone_left:
            # Gebruik hier de volledige naam: player_center_coordinate_x
            self.camera_x = player_center_coordinate_x - self.deadzone_left
        elif player_screen_coordinate_x > self.deadzone_right:
            self.camera_x = player_center_coordinate_x - self.deadzone_right

        # Controleer verticale deadzone grenzen
        if player_screen_coordinate_y < self.deadzone_top:
            self.camera_y = player_center_coordinate_y - self.deadzone_top
        elif player_screen_coordinate_y > self.deadzone_bottom:
            self.camera_y = player_center_coordinate_y - self.deadzone_bottom

        # Beperk de camera zodat deze niet buiten de randen van de map kijkt
        self.camera_x = max(0, min(self.camera_x, map_width_pixels - self.game_width))
        self.camera_y = max(0, min(self.camera_y, map_height_pixels - self.game_height))
    
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
        
        self.player_character = Player(1035, 800)
        self.enemy_list = [Dog(500, 400), Dog(1500, 400)]
        
        # laad map with 48x48 tiles
        self.game_map = Tilemap(tile_size=GAME_CONFIG["tile_size"])
        
        self.game_map.load_from_file("assets/maps/Garden_1.json")
        self.game_map.load_background_image("assets/backgrounds/background_garden.png")

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

        # minigame state
        self.is_minigame_active = False
        self.active_minigame_session = None
        self.last_interaction_location = None

        # messages
        self.active_info_message = ""
        self.message_display_timer = 0

    def handle_events(self):
        """
        Verwerkt alle gebruikersinvoer en controleert op interacties met de spelwereld.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            # Als er een minigame actief is, gaan alle events naar de telefoon
            if self.active_minigame_session:
                self.active_minigame_session.handle_input(event)
                continue

            if event.type == pygame.KEYDOWN:
                # Interactie met de wereld via de spatiebalk
                if event.key == pygame.K_SPACE:
                    # Bereken het exacte middelpunt van de speler
                    player_center_coordinate_x = self.player_character.position_coordinate_x + self.player_character.size_width // 2
                    player_center_coordinate_y = self.player_character.position_coordinate_y + self.player_character.size_height // 2
                    
                    # Haal de informatie van de tegel op (ID en locatie in het grid)
                    tile_type, row_index, column_index = self.game_map.get_interaction_tile_info(
                        player_center_coordinate_x, 
                        player_center_coordinate_y, 
                        40
                    )

                    # Logica voor de Operator Shooter (Tegel 2)
                    if tile_type == 2:
                        if (row_index, column_index) not in self.player_character.completed_minigame_locations:
                            self.last_interaction_location = (row_index, column_index)
                            logic_module = OperatorMinigame(360, 490)
                            self.active_minigame_session = CellphoneInterface(
                                GAME_CONFIG["game_width"], 
                                GAME_CONFIG["game_height"], 
                                logic_module
                            )
                        else:
                            self.active_info_message = "You have already mastered this challenge!"
                            self.message_display_timer = 120
                    
                    # Logica voor het Informatiebord (Tegel 3)
                    elif tile_type == 3:
                        self.active_info_message = "This is the church of Py, search the garden for objects and press spacebar next to them to absorb their keys or something"
                        self.message_display_timer = 270

                    # Logica voor de Python Track Minigame (Tegel 4)
                    elif tile_type == 4:
                        # Start de Python Track minigame op de telefoon
                        if (row_index, column_index) not in self.player_character.completed_minigame_locations:
                            self.last_interaction_location = (row_index, column_index)
                            # Maak de logica module aan voor het track-spel
                            logic_module = PythonTrackMinigame(360, 490) 
                            self.active_minigame_session = CellphoneInterface(
                                GAME_CONFIG["game_width"], 
                                GAME_CONFIG["game_height"],
                                logic_module
                            )
                        else:
                            # Toon een melding als de speler deze track al heeft voltooid
                            self.active_info_message = "This track has already been conquered!"
                            self.message_display_timer = 120
                            
                    elif tile_type == 5:
                        # Start de Python Quiz op de telefoon
                        if (row_index, column_index) not in self.player_character.completed_minigame_locations:
                            self.last_interaction_location = (row_index, column_index)
                            
                            logic_module = PythonQuizMinigame(360, 580) 
                            
                            self.active_minigame_session = CellphoneInterface(
                                GAME_CONFIG["game_width"], 
                                GAME_CONFIG["game_height"],
                                logic_module
                            )
                        else:
                            self.active_info_message = "This quiz has already been completed!"
                            self.message_display_timer = 120

                    # Logica voor de Finale Poort (Tegel 9)
                    elif tile_type == 9:
                        if self.player_character.keys_collected_count >= 3:
                            self.active_info_message = "Well done, you have seen the power of python and mastered it. (end of game currently)"
                        else:
                            self.active_info_message = "You don't respect the power of python yet, even though the door it is judging you to be unworthy of walking through it"
                        self.message_display_timer = 180

                # Pauzeer het spel met de Escape-toets
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = not self.is_paused


    def start_python_minigame(self):
        """
        Zet het spel op pauze en activeert de status voor het Python minispel.
        """
        self.is_paused = True
        self.is_minigame_active = True
        print("Python minigame has started.")

    def update(self):
        # controleer of de telefoon op dit moment open staat
        if self.active_minigame_session:
            self.active_minigame_session.update()
            
            # kijk of de minigame sessie net is afgelopen
            if not self.active_minigame_session.is_active:
                # pak de eindscore van de applicatie die op de telefoon draaide
                final_score_points = self.active_minigame_session.current_application.total_score_points
                
                if final_score_points >= 100:
                    # voeg de locatie toe aan de lijst met voltooide uitdagingen
                    if self.last_interaction_location not in self.player_character.completed_minigame_locations:
                        self.player_character.keys_collected_count += 1
                        self.player_character.completed_minigame_locations.add(self.last_interaction_location)
                        self.active_info_message = "You feel closer to python"
                        self.message_display_timer = 180
                
                # sluit de telefoon sessie af
                self.active_minigame_session = None
            
            return
        
        # controleer of het spel op pauze staat via het menu
        if self.is_paused:
            return
        
        # vanaf hier begint de normale logica van de wereld
        keys = pygame.key.get_pressed()
        horizontal_movement = 0
        vertical_movement = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            horizontal_movement -= self.player_character.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            horizontal_movement += self.player_character.move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vertical_movement -= self.player_character.move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vertical_movement += self.player_character.move_speed
        
        self.player_character.move(horizontal_movement, vertical_movement, self.game_map.walls)
        self.player_character.update()

        # werk de camera en de vijanden bij
        map_width_pixels = self.game_map.map_width * self.game_map.tile_size
        map_height_pixels = self.game_map.map_height * self.game_map.tile_size
        self.camera.follow_player(self.player_character, map_width_pixels, map_height_pixels)

        player_current_position = (self.player_character.position_coordinate_x, self.player_character.position_coordinate_y)

        for enemy in self.enemy_list:
            enemy.update(player_current_position, self.game_map.walls, tile_size=self.game_map.tile_size)
            enemy.separate_from_other_enemies(self.enemy_list, separation_distance=90)
            
            if self.detect_collision(self.player_character, enemy):
                self.player_character.take_damage(10)
        
        # sorteer de objecten voor het diepte effect
        self.depth_sorted_objects = [self.player_character] + self.enemy_list
        self.depth_sorted_objects.sort(key=lambda object_instance: object_instance.position_coordinate_y)

        # werk de timer van de informatieberichten bij
        if self.message_display_timer > 0:
            self.message_display_timer -= 1
        else:
            self.active_info_message = ""

    def detect_collision(self, object_one, object_two):
        """Controleert of twee objecten elkaar overlappen."""
        return (
            object_one.position_coordinate_x < object_two.position_coordinate_x + object_two.size_width and
            object_one.position_coordinate_x + object_one.size_width > object_two.position_coordinate_x and
            object_one.position_coordinate_y < object_two.position_coordinate_y + object_two.size_height and
            object_one.position_coordinate_y + object_one.size_height > object_two.position_coordinate_y
        )

    def draw(self):
        """Tekent de volledige spelwereld en UI elementen."""
        self.game_surface.fill(DARK_GRAY)
        
        # Achtergrond
        self.game_map.draw_background(self.game_surface, self.camera.camera_x, self.camera.camera_y)
        
        # Wereld objecten
        for game_object in self.depth_sorted_objects:
            screen_x, screen_y = self.camera.apply_to_position(
                game_object.position_coordinate_x, 
                game_object.position_coordinate_y
            )
            game_object.draw_at_position(self.game_surface, screen_x, screen_y)
        
        # Verlichting
        player_screen_x, player_screen_y = self.camera.apply_to_position(
            self.player_character.position_coordinate_x,
            self.player_character.position_coordinate_y
        )
        self.lighting_system.apply_lighting(
            self.game_surface,
            (player_screen_x, player_screen_y),
            (self.player_character.size_width, self.player_character.size_height)
        )
        
        # Telefoon/Minigame
        if self.active_minigame_session:
            overlay_surface = pygame.Surface((GAME_CONFIG["game_width"], GAME_CONFIG["game_height"]))
            overlay_surface.set_alpha(128)
            overlay_surface.fill(BLACK)
            self.game_surface.blit(overlay_surface, (0, 0))
            self.active_minigame_session.draw(self.game_surface)
        
        # Health bar en algemene UI
        self.user_interface.draw(self.game_surface, self.player_character)

        # Informatieberichten (Borden)
        if self.active_info_message != "":
            self.user_interface.draw_info_message(self.game_surface, self.active_info_message)
        
        # Pauze scherm
        if self.is_paused:
            self.draw_pause_screen()

        # Update display
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