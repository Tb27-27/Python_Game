import pygame
import math

class LightSystem:
    """Fog-of-war lighting: alleen binnen lichtcirkel zichtbaar, rest pikzwart"""
    
    def __init__(self, screen_width, screen_height, light_radius=300):
        self.screen_width_pixels = screen_width
        self.screen_height_pixels = screen_height
        self.light_radius_pixels = light_radius
        
        # Pre-generate het ronde lichtmasker (centrum transparant, randen zwart)
        self.radial_light_mask = self._generate_radial_light_mask()
    
    def _generate_radial_light_mask(self):
        """Genereer perfect rond gradient mask voor zacht licht"""
        mask_size = self.light_radius_pixels * 2
        light_mask = pygame.Surface((mask_size, mask_size), pygame.SRCALPHA)
        
        mask_center_x = self.light_radius_pixels
        mask_center_y = self.light_radius_pixels
        
        # bouw zachte gradient op elke pixel
        for pixel_y in range(mask_size):
            for pixel_x in range(mask_size):
                # Afstand van centrum
                delta_x = pixel_x - mask_center_x
                delta_y = pixel_y - mask_center_y
                distance_from_center = math.hypot(delta_x, delta_y)
                
                if distance_from_center < self.light_radius_pixels:
                    # Zachte falloff
                    fade_factor = distance_from_center / self.light_radius_pixels
                    darkness_alpha = int(255 * fade_factor * fade_factor)
                else:
                    # Buiten radius = volledig zwart
                    darkness_alpha = 255
                
                # Zet pixel: zwart met alpha (transparant = licht, opaque = donker)
                light_mask.set_at((pixel_x, pixel_y), (0, 0, 0, darkness_alpha))
        
        return light_mask
    
    def apply_lighting(self, screen, player_position):
        """Pas fog-of-war toe: zwarte overlay met lichtgat bij speler"""
        
        # Maak volledig zwarte overlay (alles onzichtbaar)
        darkness_overlay = pygame.Surface(
            (self.screen_width_pixels, self.screen_height_pixels), 
            pygame.SRCALPHA
        )
        darkness_overlay.fill((0, 0, 0, 255))  # 100% zwart
        
        # Bereken waar het licht moet schijnen (midden speler)
        player_torso_x = int(player_position[0] + 25)
        player_torso_y = int(player_position[1] + 45)
        light_mask_offset_x = player_torso_x - self.light_radius_pixels
        light_mask_offset_y = player_torso_y - self.light_radius_pixels
        
        # "Snee" het lichtgat in de duisternis (multiplicatie blend)
        darkness_overlay.blit(
            self.radial_light_mask, 
            (light_mask_offset_x, light_mask_offset_y),
            special_flags=pygame.BLEND_RGBA_MULT
        )
        
        # Overlay over hele scherm (moet LAATSTE render stap zijn)
        screen.blit(darkness_overlay, (0, 0))