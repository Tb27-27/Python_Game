import pytest
import pygame
from src.player import Player

def test_player_initialization():
    # controleer of de speler start met de juiste waarden
    player_instance = Player(100, 200)
    
    # de x en y coordinaten moeten overeenkomen met de startpositie
    assert player_instance.position_coordinate_x == 100
    assert player_instance.position_coordinate_y == 200
    # de gezondheid moet bij de start honderd zijn
    assert player_instance.health == 100

def test_player_movement():
    # controleer of de speler kan bewegen zonder muren
    player_instance = Player(100, 100)
    
    # we bewegen de speler tien pixels naar rechts
    player_instance.move(10, 0, [])
    
    # de x coordinaat moet nu honderdtien zijn
    assert player_instance.position_coordinate_x == 110

def test_player_collision_wall():
    # controleer of de speler stopt als hij tegen een muur loopt
    player_instance = Player(100, 100)
    
    # we plaatsen een muur op positie honderdtwintig
    wall_rectangle = pygame.Rect(120, 100, 50, 150)
    wall_rectangles_list = [wall_rectangle]
    
    # probeer tien pixels naar rechts te bewegen
    player_instance.move(10, 0, wall_rectangles_list)
    
    # de speler mag niet bewogen zijn omdat de muur in de weg staat
    assert player_instance.position_coordinate_x == 100

def test_player_take_damage():
    # controleer of de gezondheid van de speler afneemt na schade
    player_instance = Player(100, 100)
    
    # de speler krijgt twintig schade punten
    player_instance.take_damage(20)
    
    # de gezondheid moet nu tachtig zijn
    assert player_instance.health == 80