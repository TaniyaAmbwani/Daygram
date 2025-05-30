import pygame
import sys
import random
from math import *

pygame.init()

# Declaring variables
width = 1540
height = 790

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sky Chaser")
clock = pygame.time.Clock()

margin = 100
lowerBound = 100

score = 0

# Declaring variables that store the color codes:
white = (230, 230, 230)
Black = (0, 0, 0)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (64, 178, 239)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)

font = pygame.font.SysFont("TimesNewRoman", 25)
button_font = pygame.font.SysFont("Arial", 30)

# Defining balloon class
class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, blue, yellow, orange])

    # Function that moves the balloon:
    def move(self):
        direct = random.choice(self.proPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    # Logic to show balloon on screen:
    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b), (self.x + self.a / 2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))

    # To check if the balloon is burst or not
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if isonBalloon(self.x, self.y, self.a, self.b, pos):
            score += 1
            self.reset()

    # Reset function:
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, blue, yellow, orange])

balloons = []
no_of_Balloon = 10

for i in range(no_of_Balloon):
    obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
    balloons.append(obj)

def isonBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False

def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = lightGreen
    for i in range(no_of_Balloon):
        if isonBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r / 2, pos[1] - r / 2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l / 2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l / 2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l / 2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l / 2, pos[1]), (pos[0] - l, pos[1]), 4)

def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))

# Display the score:
def showScore():
    scoreText = font.render("Goal Achieved: " + str(score), True, white)
    display.blit(scoreText, (710, height - lowerBound + 50))

# Draw button:
def draw_button(x, y, w, h, text, color):
    pygame.draw.rect(display, color, (x, y, w, h))
    text_surface = button_font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    display.blit(text_surface, text_rect)

def handle_buttons():
    global score
    pos = pygame.mouse.get_pos()
    if 50 < pos[0] < 150 and height - lowerBound + 10 < pos[1] < height - lowerBound + 50:
        score = 0
        game()
    if 1350 < pos[0] < 1450 and height - lowerBound + 10 < pos[1] < height - lowerBound + 50:
        close()

# Close the game:
def close():
    pygame.quit()
    sys.exit()

# To keep track of events:
def game():
    global score
    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_buttons()
                for i in range(no_of_Balloon):
                    balloons[i].burst()

        display.fill(Black)

        for i in range(no_of_Balloon):
            balloons[i].show()

        pointer()

        for i in range(no_of_Balloon):
            balloons[i].move()

        lowerPlatform()
        showScore()

        draw_button(50, height - lowerBound + 10, 100, 40, "RESET", green)
        draw_button(1350, height - lowerBound + 10, 100, 40, "QUIT", red)

        pygame.display.update()
        clock.tick(60)

game()
