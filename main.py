import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Initialize colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 60
PLAYER_SPEED = 10
GRAVITY = 0.5
JUMP_STRENGTH = -15

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

# Initialize window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run")
clock = pygame.time.Clock()

# Initialize character variables/image
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
player_velocity_x = 0
player_velocity_y = 0
is_jumping = False
player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_image.fill(RED)

# Initialize power-up variables
power_up_active = False
power_up_duration = 10 * 1000
power_up_remaining = 0
power_up_cooldown = 15 * 1000
power_up_next_use = 15000

# Initialize platforms
platforms = []
run_plat = True
counter = 0

# Initialize obstacles
obstacles = []
for _ in range(5):
    rand_x = random.randint(100, 1500)
    rand_y = random.randint(100, 1100)
    obstacle = Obstacle(rand_x, rand_y, 40, 40)
    obstacles.append(obstacle)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_velocity_x = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        player_velocity_x = PLAYER_SPEED
    else:
        player_velocity_x = 0

    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = JUMP_STRENGTH
        is_jumping = True

    player_velocity_y += GRAVITY
    player_x += player_velocity_x
    player_y += player_velocity_y

    for obstacle in obstacles:
        if (player_x + PLAYER_WIDTH > obstacle.rect.left and player_x < obstacle.rect.right and
            player_y + PLAYER_HEIGHT > obstacle.rect.top and player_y < obstacle.rect.bottom):
            print("Collision with obstacle!")



    if player_y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
        is_jumping = False
        player_velocity_y = 0

    if player_y <= 0:
        player_y = 0
        is_jumping = True
        player_velocity_y = 0

    if player_x <= 0:
        player_x = 0
        is_jumping = False
        player_velocity_x = 0

    if player_x >= SCREEN_WIDTH - PLAYER_WIDTH:
        player_x = SCREEN_WIDTH - PLAYER_WIDTH
        is_jumping = False
        player_velocity_x = 0

    # Collision detection (platforms)
    for obstacle in obstacles:
        for platform in platforms:
            if (player_x + PLAYER_WIDTH > platform[0] and player_x < platform[0] + platform[2] and
                player_y + PLAYER_HEIGHT > platform[1] and player_y < platform[1] + platform[3]):
                if player_velocity_y > 0:
                    # Player landed on the platform
                    player_y = platform[1] - PLAYER_HEIGHT
                    player_velocity_y = 0
                    is_jumping = False
                elif player_velocity_y < 0:
                    # Player hit the platform from underneath
                    player_y = platform[1] + platform[3]
                    player_velocity_y = 0

        # Collision detection (obstacles)
        if (player_x + PLAYER_WIDTH > obstacle.rect.left and player_x < obstacle.rect.right and
            player_y + PLAYER_HEIGHT > obstacle.rect.top and player_y < obstacle.rect.bottom):
            # Handle obstacle collision (customize as needed)
            # In this section, you can add code to define what happens
            # when the player collides with an obstacle, such as game over,
            # deducting health, etc. Modify this section according to your game's logic.
            pass

    # Update obstacle positions
    for obstacle in obstacles:
        obstacle.rect.x -= PLAYER_SPEED  # Adjust this value based on your game's mechanics
        if obstacle.rect.right < 0:
            obstacle.rect.x = SCREEN_WIDTH  # Reset obstacle position when it goes off-screen



    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle.rect)

    # Power-up usage
    if keys[pygame.K_p] and keys[pygame.K_SPACE] and power_up_next_use <= 0:
        power_up_active = True
        power_up_remaining = power_up_duration
        power_up_next_use = pygame.time.get_ticks() + power_up_cooldown
        GRAVITY = 0.2

    # Decrement power-up next use timer
    if power_up_next_use > 0:
        power_up_next_use -= 20

    # Update power-up
    if power_up_active:
        power_up_remaining -= 20
        if power_up_remaining <= 0:
            power_up_active = False
            power_up_remaining = 0
            power_up_next_use = 15000
            GRAVITY = 0.5

    # Draw power-up and cooldown
    font = pygame.font.Font(None, 36)
    timer_text = font.render("Power-Up Timer: " + str(power_up_remaining // 1000) + " seconds", True, RED)
    screen.blit(timer_text, (10, 20))

    if not power_up_active:
        timer_text_cooldown = font.render("Cooldown: " + str(power_up_next_use // 1000) + " seconds", True, RED)
        ready = font.render("Powerup Ready", True, RED)

        if power_up_next_use <= 0:
            screen.blit(ready, (player_x - 90, player_y - 50))
        else:
            screen.blit(timer_text_cooldown, (player_x - 120, player_y - 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
