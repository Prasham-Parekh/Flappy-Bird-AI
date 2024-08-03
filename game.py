import pygame
import random

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Bird Constants 
JUMP = -10
GRAVITY = 0.5
BIRD_SIZE = 20

# Pipe Constants


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Bird Class
class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH / 5
        self.y = SCREEN_HEIGHT / 2
        self.velocity = 0
    
    def jump(self):
        self.velocity = JUMP

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        if (self.y - BIRD_SIZE) < 0:
            self.y = BIRD_SIZE
            self.velocity = 0
        
        if (self.y + BIRD_SIZE) > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - BIRD_SIZE
            self.velocity = 0

# Pipe Class


# Main Game
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        pygame.draw.circle(screen, BLACK, player_pos, SIZE)

        pygame.display.flip()


    pygame.quit()