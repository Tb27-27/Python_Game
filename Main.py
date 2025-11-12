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

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Pygame")
clock = pygame.time.Clock()

# Player settings
player_x = 350
player_y = 250
player_width = 50
player_height = 90
player_speed = 5

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
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
        player_x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
        player_y -= player_speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < SCREEN_HEIGHT - player_height:
        player_y += player_speed
    
    # Draw everything
    screen.fill(WHITE)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit
pygame.quit()
sys.exit()