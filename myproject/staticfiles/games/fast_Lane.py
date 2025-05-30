import pygame
from pygame.locals import *
import os
import random

pygame.init()

# Set up screen size
info = pygame.display.Info()  
width, height = info.current_w, info.current_h  # Get full screen size
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)  # Full-screen mode
pygame.display.set_caption('Fast Lane - Car Game')

# Colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Road and marker sizes
road_width = width * 0.5  # Road occupies 50% of the screen width
marker_width = 10
marker_height = 50

# Lane coordinates (3 lanes dynamically adjusted)
left_lane = (width // 2) - (road_width // 3)
center_lane = width // 2
right_lane = (width // 2) + (road_width // 3)
lanes = [left_lane, center_lane, right_lane]

# Road and edge markers
road = ((width // 2) - (road_width // 2), 0, road_width, height)
left_edge_marker = ((width // 2) - (road_width // 2) - 5, 0, marker_width, height)
right_edge_marker = ((width // 2) + (road_width // 2) - 5, 0, marker_width, height)

# Lane marker animation
lane_marker_move_y = 0

# Player starting position
player_x = center_lane
player_y = height - 150  # 150 pixels above the bottom of the screen

# Frame settings
clock = pygame.time.Clock()
fps = 60  # Adjusted FPS for smooth gameplay

# Game variables
gameover = False
speed = 3
score = 0
fullscreen = True  # Start in full-screen mode


def load_image(filename):
    """ Load an image from the images folder. """
    base_path = os.path.dirname(os.path.abspath(_file_))  
    image_path = os.path.join(base_path, 'images', filename)

    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else:
        print(f"Error: Image {filename} not found!")
        return pygame.Surface((50, 50))  # Return a blank surface


class Vehicle(pygame.sprite.Sprite):
    """ Vehicle class for both player and traffic. """
    def _init_(self, image, x, y):
        pygame.sprite.Sprite._init_(self)
        image_scale = (road_width // 6) / image.get_rect().width  # Scale to fit lanes
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    """ Player-controlled car. """
    def _init_(self, x, y):
        image = load_image('car.png')
        super()._init_(image, x, y)


# Sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Create player car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load vehicle images
vehicle_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [load_image(img) for img in vehicle_filenames]

# Load crash image
crash_image = load_image('crash.png')
crash_rect = crash_image.get_rect()

# Game loop
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Move the player's car using arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= road_width // 3
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += road_width // 3

            # Toggle fullscreen mode
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width, height))

            # Check for side collision
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
                    crash_rect.center = [player.rect.center[0], (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    # Draw background
    screen.fill(green)

    # Draw road
    pygame.draw.rect(screen, gray, road)

    # Draw edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # Draw lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # Draw player's car
    player_group.draw(screen)

    # Add vehicles
    if len(vehicle_group) < 3:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, -100)
            vehicle_group.add(vehicle)

    # Move vehicles
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1

    # Draw vehicles
    vehicle_group.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, white)
    screen.blit(text, (50, 50))

    # Check for collisions
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # Display Game Over
    if gameover:
        screen.blit(crash_image, crash_rect)
        pygame.draw.rect(screen, red, (0, height // 3, width, 100))

        text = font.render('Game Over! Play again? (Y/N)', True, white)
        text_rect = text.get_rect(center=(width / 2, height / 3 + 50))
        screen.blit(text, text_rect)

    pygame.display.update()

    # Handle Game Over input
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 3
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()