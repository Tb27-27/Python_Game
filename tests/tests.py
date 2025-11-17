import pytest
from src.player import Player

def test_player_movement():
    # Test of player kan bewegen
    player = Player(100, 100)
    player.move(10, 0, [])
    assert player.x == 110
    
def test_player_collision_wall():
    # Test of player stopt bij muur
    # TODO: implementeren na collision system
    pass