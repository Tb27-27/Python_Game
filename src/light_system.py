import pygame
import math

class LightSystem:
    """Fog-of-war lighting: alleen binnen lichtcirkel zichtbaar, rest zwart"""
    
    def __init__(self, screen_width, screen_height, light_radius=2040):
        self.screen_width_pixels = screen_width
        self.screen_height_pixels = screen_height
        self.light_radius_pixels = light_radius
        
        # rond masker voor player
        self.radial_light_mask = self._generate_radial_light_mask()
    
    def _generate_radial_light_mask(self):
        """Genereer perfect cirkel gradient mask voor zacht licht"""
        mask_size = self.light_radius_pixels * 2
        light_mask = pygame.Surface((mask_size, mask_size), pygame.SRCALPHA)
        
        mask_center_x = self.light_radius_pixels
        mask_center_y = self.light_radius_pixels
        
        # bouw zachte gradient op elke pixel
        for pixel_y in range(mask_size):
            for pixel_x in range(mask_size):
                # afstand van center
                delta_x = pixel_x - mask_center_x
                delta_y = pixel_y - mask_center_y
                distance_from_center = math.hypot(delta_x, delta_y)
                
                if distance_from_center < self.light_radius_pixels:
                    # fade out
                    fade_factor = distance_from_center / self.light_radius_pixels
                    darkness_alpha = int(255 * fade_factor * fade_factor)
                else:
                    # alles wat er buiten valt moet donker zijn
                    darkness_alpha = 255
                
                light_mask.set_at((pixel_x, pixel_y), (0, 0, 0, darkness_alpha))
        
        return light_mask
    
    def apply_lighting(self, screen, player_position, player_size=(48, 92)):
        """Pas fog-of-war toe: zwarte overlay met lichtcirkel bij speler"""

        # zwarte overlay
        darkness_overlay = pygame.Surface(
            (self.screen_width_pixels, self.screen_height_pixels),
            pygame.SRCALPHA
        )
        darkness_overlay.fill((0, 0, 0, 255))

        # waar het licht is
        player_center_x = int(player_position[0] + player_size[0] // 2)
        player_center_y = int(player_position[1] + player_size[1] // 2)
        light_mask_offset_x = player_center_x - self.light_radius_pixels
        light_mask_offset_y = player_center_y - self.light_radius_pixels

        # blit er het licht overheen
        darkness_overlay.blit(
            self.radial_light_mask,
            (light_mask_offset_x, light_mask_offset_y),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        # laatste stap is helemaal donker maken van de rest
        screen.blit(darkness_overlay, (0, 0))