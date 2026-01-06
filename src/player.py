import pygame
from src.colors import BLUE, LIGHT_BLUE

class Player:
    def __init__(self, start_coordinate_x, start_coordinate_y):
        # de logische hitbox voor interacties en muren
        self.size_width = 48
        self.size_height = 96

        # de visuele grootte van de sprite voor de animaties
        self.sprite_render_size_pixels = 120 
        self.base_frame_size_pixels = 48

        self.position_coordinate_x = float(start_coordinate_x)
        self.position_coordinate_y = float(start_coordinate_y)

        # statistieken die ook door de ui worden gelezen
        self.health = 100
        self.max_health = 100
        self.move_speed = 4.0
        
        self.keys_collected_count = 0
        self.completed_minigame_locations = set()

        # i, i, baby, frame all
        self.is_invincible_boolean = False
        self.invincibility_timer_frames = 0
        self.invincibility_duration_limit = 150

        # animatie variabelen
        self.current_animation_frame_index = 0
        self.animation_timer_value = 0.0
        self.animation_speed_rate = 0.15
        self.is_moving_boolean = False
        self.is_facing_right_boolean = True

        # inladen van de animaties
        self.idle_animation_sprites = self.load_animation_spritesheet("assets/player/Player_Idle.png", 4)
        self.walking_animation_sprites = self.load_animation_spritesheet("assets/player/Player_Walking.png", 6)
        
        self.current_active_sprite_surface = self.idle_animation_sprites[0]

    def load_animation_spritesheet(self, file_path_string, total_frames_number):
        extracted_frames_list = []
        try:
            full_sheet_surface = pygame.image.load(file_path_string).convert_alpha()
            for index in range(total_frames_number):
                source_rectangle = pygame.Rect(index * self.base_frame_size_pixels, 0, self.base_frame_size_pixels, self.base_frame_size_pixels)
                temp_surface = pygame.Surface((self.base_frame_size_pixels, self.base_frame_size_pixels), pygame.SRCALPHA)
                temp_surface.blit(full_sheet_surface, (0, 0), source_rectangle)
                
                # schaal de sprite naar de grote visuele maat
                scaled_surface = pygame.transform.scale(temp_surface, (self.sprite_render_size_pixels, self.sprite_render_size_pixels))
                extracted_frames_list.append(scaled_surface)
        except pygame.error:
            fallback_surface = pygame.Surface((self.size_width, self.size_height))
            fallback_surface.fill(LIGHT_BLUE)
            extracted_frames_list.append(fallback_surface)
        return extracted_frames_list

    def move(self, horizontal_input, vertical_input, walls_list):
        self.is_moving_boolean = horizontal_input != 0 or vertical_input != 0
        if horizontal_input > 0:
            self.is_facing_right_boolean = True
        elif horizontal_input < 0:
            self.is_facing_right_boolean = False

        if horizontal_input != 0:
            self.position_coordinate_x += horizontal_input
            if self._collides_with_walls(walls_list):
                self.position_coordinate_x -= horizontal_input
        
        if vertical_input != 0:
            self.position_coordinate_y += vertical_input
            if self._collides_with_walls(walls_list):
                self.position_coordinate_y -= vertical_input
    
    def _collides_with_walls(self, walls_list):
        player_hitbox_rectangle = pygame.Rect(self.position_coordinate_x, self.position_coordinate_y, self.size_width, self.size_height)
        for wall in walls_list:
            if player_hitbox_rectangle.colliderect(wall):
                return True
        return False

    def perform_interaction(self, current_tilemap):
        # bereken het midden van de hitbox voor interactie
        player_center_x = self.position_coordinate_x + (self.size_width // 2)
        player_center_y = self.position_coordinate_y + (self.size_height // 2)
        return current_tilemap.get_interaction_tile_id(player_center_x, player_center_y, 40)
    
    def update(self):
        if self.invincibility_timer_frames > 0:
            self.invincibility_timer_frames -= 1
            self.is_invincible_boolean = True
        else:
            self.is_invincible_boolean = False

        self.animation_timer_value += self.animation_speed_rate
        active_list = self.walking_animation_sprites if self.is_moving_boolean else self.idle_animation_sprites
        
        if self.animation_timer_value >= len(active_list):
            self.animation_timer_value = 0
            
        self.current_animation_frame_index = int(self.animation_timer_value)
        self.current_active_sprite_surface = active_list[self.current_animation_frame_index]

    def draw_at_position(self, screen_surface, screen_coordinate_x, screen_coordinate_y):
        if self.is_invincible_boolean and (self.invincibility_timer_frames // 5) % 2 == 0:
            return 

        if not self.is_facing_right_boolean:
            final_sprite_surface = pygame.transform.flip(self.current_active_sprite_surface, True, False)
        else:
            final_sprite_surface = self.current_active_sprite_surface

        # centreer de grote sprite boven de hitbox
        offset_x = (self.sprite_render_size_pixels - self.size_width) // 2
        offset_y = self.sprite_render_size_pixels - self.size_height
        screen_surface.blit(final_sprite_surface, (int(screen_coordinate_x - offset_x), int(screen_coordinate_y - offset_y)))

    def take_damage(self, damage_amount):
        if not self.is_invincible_boolean:
            self.health = max(0, self.health - damage_amount)
            self.invincibility_timer_frames = self.invincibility_duration_limit