import pygame
import random
import math
import os
from pygame import mixer

# Initialize pygame
pygame.init()

# Get the directory where this script is located
game_dir = os.path.dirname(__file__)
image_dir = os.path.join(game_dir, "images")  # Path to images folder

# Create a full-screen window with the default close (X) button
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()  # Get the screen size

# Load images using absolute paths
background = pygame.image.load(os.path.join(image_dir, "background1.png"))
background = pygame.transform.scale(background, (width, height))  # Scale background

icon = pygame.image.load(os.path.join(image_dir, "spaceship.png"))
playerimg = pygame.image.load(os.path.join(image_dir, "arcade-game.png"))
bulletimg = pygame.image.load(os.path.join(image_dir, "bullet.png"))

# Enemy images
num_of_enemy = 5
enemyimg = [pygame.image.load(os.path.join(image_dir, "alien.png")) for _ in range(num_of_enemy)]

# Sounds
bulletSound = mixer.Sound(os.path.join(image_dir, "laser.wav"))
explosionSound = mixer.Sound(os.path.join(image_dir, "explosion.wav"))

# Set game icon
pygame.display.set_caption("Attack Aliens")
pygame.display.set_icon(icon)

# Player settings
playerx, playery = width // 2 - 32, height - 100  # Center player horizontally
playerx_change = 0

# Enemy settings (Increased Speed)
enemyx = [random.randint(0, width - 64) for _ in range(num_of_enemy)]
enemyy = [random.randint(50, 150) for _ in range(num_of_enemy)]
enemyx_change = [3 for _ in range(num_of_enemy)]  # Increased from 2 to 3
enemyy_change = [40 for _ in range(num_of_enemy)]

# Bullet settings (Increased Speed)
bulletx, bullety = 0, playery
bulletx_change, bullety_change = 0, 20  # Increased from 16 to 20
bullet_state = "ready"

# Score settings
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Functions
def show_score(x, y):
    score = font.render("Killed: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (width // 2 - 150, height // 2 - 32))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    return distance < 27

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))  # Background covers entire screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Allow (X) button to close the game

        # Move player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound.play()
                bulletx = playerx
                fire_bullet(bulletx, bullety)
            if event.key == pygame.K_ESCAPE:  # Quit game when ESC is pressed
                running = False

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerx_change = 0

    # Update player position
    playerx += playerx_change
    playerx = max(0, min(width - 64, playerx))

    # Enemy movement
    for i in range(num_of_enemy):
        if enemyy[i] > height - 150:
            for j in range(num_of_enemy):
                enemyy[j] = height + 100  # Move enemies off-screen
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0 or enemyx[i] >= width - 64:
            enemyx_change[i] *= -1
            enemyy[i] += enemyy_change[i]

        if iscollision(enemyx[i], enemyy[i], bulletx, bullety):
            explosionSound.play()
            bullety = playery
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, width - 64)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    if bullety < 0:
        bullety = playery
        bullet_state = "ready"

    # Draw player and score
    player(playerx, playery)
    show_score(10, 10)

    pygame.display.update()

pygame.quit()
