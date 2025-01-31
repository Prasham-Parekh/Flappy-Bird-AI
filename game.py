import pygame
import random
import sys

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Bird Constants 
JUMP = -10
GRAVITY = 0.5
BIRD_SIZE = 20

# Pipe Constants
PIPE_GAP = 200
PIPE_WIDTH = 80
PIPE_SPEED = 5
PIPE_FREQUENCY = 1000

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

    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), BIRD_SIZE)

    def get_rect(self):
        return pygame.Rect(self.x - BIRD_SIZE, self.y - BIRD_SIZE, BIRD_SIZE * 2, BIRD_SIZE * 2)

# Pipe Class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
    
    def update(self):
        self.x -= PIPE_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
        return top_rect, bottom_rect

# Checks for Collision
def check_collision(bird, pipes):
    bird_rect = bird.get_rect()
    
    # Check collision with pipes
    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    
    # Check collision with ground
    if bird.y + BIRD_SIZE >= SCREEN_HEIGHT:
        return True
    
    # Check collision with ceiling
    if bird.y - BIRD_SIZE <= 0:
        return True
    
    return False

pygame.font.init()
font = pygame.font.SysFont(None, 50)

# Main Game
def main():
    bird = Bird()
    pipes = [Pipe()]
    running = True
    last_pipe_time = pygame.time.get_ticks()
    score = 0
    high_score = 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()

        # Gets last pipe time
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > PIPE_FREQUENCY:
            pipes.append(Pipe())
            last_pipe_time = current_time
        
        # Updates and draws new pipe
        for pipe in pipes:
            pipe.update()
            pipe.draw()

        # Removes pipes that are out of screen
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        # Update score if the bird passes a pipe
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH < bird.x and not hasattr(pipe, 'scored'):
                score += 1
                pipe.scored = True

        # Draws bird
        bird.draw()

         # Check for collisions
        if check_collision(bird, pipes):
            # Restart game
            high_score = max(high_score, score)
            score = 0
            bird = Bird()
            pipes = []
            last_pipe_time = pygame.time.get_ticks()

        # Display Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

def run():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config-feedforward.txt")
    run(config_path)