import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pythy")
clock = pygame.time.Clock()

# Player settings
player_x = 350
player_y = 250
player_width = 50
player_height = 90
player_speed = 5


# Enemy settings
enemy_x = 350
enemy_y = 250
enemy_width = 60
enemy_height = 100
enemy_speed = 5

# move input bool
def moveInput(direction, keys):
    if direction == "left" and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        return True
    elif direction == "right" and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        return True
    elif direction == "up" and (keys[pygame.K_UP] or keys[pygame.K_w]):
        return True
    elif direction == "down" and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        return True
    else:
        return False
    

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keys pressed
    keys = pygame.key.get_pressed()

        
    
    # Move player
    if moveInput("left") and player_x > 0:
        player_x -= player_speed
    if moveInput("right") and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if moveInput("up") and player_y > 0:
        player_y -= player_speed
    if moveInput("down") and player_y < SCREEN_HEIGHT - player_height:
        player_y += player_speed
    
    # Draw everything
    screen.fill(WHITE)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Draw player
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit
pygame.quit()
sys.exit()