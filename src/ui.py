import pygame
from src.colors import *

class UI:
    """
    De UI klasse is verantwoordelijk voor het tekenen van alle interface-elementen,
    zoals de gezondheidsbalk, de verzamelde sleutels en informatievensters.
    """
    
    # Constanten voor de  de gezondheidsbalk
    HEALTH_BAR_WIDTH = 96
    HEALTH_BAR_HEIGHT = 32
    HEALTH_BAR_X_POSITION = 8
    HEALTH_BAR_Y_POSITION = 8
    TEXT_OFFSET_X_COORDINATE = 4
    
    def __init__(self, screen_width_pixels, screen_height_pixels):
        """
        Initialiseert de gebruikersinterface met de juiste schermresolutie en fonts.
        """
        self.screen_width_pixels = screen_width_pixels
        self.screen_height_pixels = screen_height_pixels
        
        # Initialiseer het lettertype voor de interface
        self.user_interface_font = pygame.font.Font(None, 36)

        # Probeer de afbeelding voor de sleutels te laden
        try:
            self.key_icon_surface = pygame.image.load("assets/key.png").convert_alpha()
            self.key_icon_surface = pygame.transform.scale(self.key_icon_surface, (32, 32))
        except pygame.error:
            # Als het bestand niet bestaat, gebruiken we geen afbeelding
            self.key_icon_surface = None

    def draw(self, screen_surface, player_instance):
        """
        Hoofdmethode die alle afzonderlijke UI-elementen op het scherm tekent.
        """
        self.draw_health_bar(screen_surface, player_instance)
        self.draw_keys_inventory(screen_surface, player_instance)
    
    def draw_health_bar(self, screen_surface, player_instance):
        """
        Tekent de gezondheidsbalk van de speler aan de linkerkant van het scherm.
        """
        bar_width = self.HEALTH_BAR_WIDTH
        bar_height = self.HEALTH_BAR_HEIGHT
        coordinate_x = self.HEALTH_BAR_X_POSITION
        coordinate_y = self.HEALTH_BAR_Y_POSITION
        
        # Teken de achtergrond van de balk (donkerrood)
        pygame.draw.rect(screen_surface, DARK_RED, (coordinate_x, coordinate_y, bar_width, bar_height))
        
        # Bereken de breedte van de huidige gezondheid en teken de groene balk
        health_percentage = player_instance.health / player_instance.max_health
        current_health_bar_width = int(bar_width * health_percentage)
        pygame.draw.rect(screen_surface, GREEN, (coordinate_x, coordinate_y, current_health_bar_width, bar_height))
        
        # Teken een witte rand om de balk
        pygame.draw.rect(screen_surface, WHITE, (coordinate_x, coordinate_y, bar_width, bar_height), 1)
        
        # Teken de HP-tekst naast de balk
        health_text_surface = self.user_interface_font.render(
            f"HP: {int(player_instance.health)}/{player_instance.max_health}", 
            True, 
            WHITE
        )
        screen_surface.blit(
            health_text_surface, 
            (coordinate_x + bar_width + self.TEXT_OFFSET_X_COORDINATE, coordinate_y)
        )
    
    def draw_info_message(self, screen_surface, message_text):
        """
        Tekent een tekstvak in het midden onderaan het scherm met automatische tekstafbreking.
        """
        box_width_pixels = 640
        box_height_pixels = 140
        
        # Gebruik de correcte variabelenamen voor de schermresolutie
        box_coordinate_x = (self.screen_width_pixels - box_width_pixels) // 2
        box_coordinate_y = self.screen_height_pixels - box_height_pixels - 60

        # Maak een transparant oppervlak voor de container
        message_container_surface = pygame.Surface((box_width_pixels, box_height_pixels))
        message_container_surface.set_alpha(230)
        message_container_surface.fill(BLACK)
        screen_surface.blit(message_container_surface, (box_coordinate_x, box_coordinate_y))
        
        # Teken de witte rand van de container
        pygame.draw.rect(screen_surface, WHITE, (box_coordinate_x, box_coordinate_y, box_width_pixels, box_height_pixels), 2)

        # Logica om de tekst op te splitsen in meerdere regels (word wrap)
        info_font = pygame.font.Font(None, 30)
        words_list = message_text.split(' ')
        lines_list = []
        current_line_text = ""

        for word in words_list:
            test_line_text = current_line_text + word + " "
            if info_font.size(test_line_text)[0] < box_width_pixels - 40:
                current_line_text = test_line_text
            else:
                lines_list.append(current_line_text)
                current_line_text = word + " "
        lines_list.append(current_line_text)

        # Teken elke regel tekst in het venster
        for line_index, line_text in enumerate(lines_list):
            text_line_surface = info_font.render(line_text, True, WHITE)
            screen_surface.blit(
                text_line_surface, 
                (box_coordinate_x + 20, box_coordinate_y + 25 + (line_index * 32))
            )

    def draw_keys_inventory(self, screen_surface, player_instance):
        """
        Tekent de verzamelde sleutels rechtsboven in het scherm.
        """
        # Startpunt aan de rechterkant van het scherm
        inventory_coordinate_x = self.screen_width_pixels - 50
        inventory_coordinate_y = 30
        spacing_pixels = 40

        # Teken een icoon voor elke verzamelde sleutel
        for key_index in range(player_instance.keys_collected_count):
            render_location_x = inventory_coordinate_x - (key_index * spacing_pixels)
            
            if self.key_icon_surface:
                screen_surface.blit(self.key_icon_surface, (render_location_x, inventory_coordinate_y))
            else:
                # Fallback: geel vierkantje als de afbeelding ontbreekt
                pygame.draw.rect(screen_surface, (255, 215, 0), (render_location_x, inventory_coordinate_y, 25, 25))
                pygame.draw.rect(screen_surface, (255, 255, 255), (render_location_x, inventory_coordinate_y, 25, 25), 2)

        # Teken de tekst-teller
        keys_status_text = f"Keys: {player_instance.keys_collected_count} / 3"
        text_surface = self.user_interface_font.render(keys_status_text, True, (255, 255, 255))
        text_x = self.screen_width_pixels - text_surface.get_width() - 20
        text_y = inventory_coordinate_y + 45
        screen_surface.blit(text_surface, (text_x, text_y))