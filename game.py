import pygame
import random
import sys
import neat
import os

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
PIPE_FREQUENCY = 1200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Bird Class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.fitness = 0
    
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
        self.passed = False
    
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

def draw_window(birds, pipes, score):
    for pipe in pipes:
        pipe.draw()

    for bird in birds:
        bird.draw()

    pygame.display.update()

# Main Game
def main(genomes, config):
    # Game variables
    birds = []
    nets = []
    ge = []

    # Create birds for each genome
    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2))
        ge.append(genome)

    pipes = [Pipe()]
    running = True
    last_pipe_time = pygame.time.get_ticks()
    score = 0

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + PIPE_WIDTH:
                pipe_ind = 1
        else:
            running = False
            break

        for i, bird in enumerate(birds):
            bird.update()
            ge[i].fitness += 0.1

            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].height + PIPE_GAP)))

            if output[0] > 0.5:
                bird.jump()

        # Gets last pipe time
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > PIPE_FREQUENCY:
            pipes.append(Pipe())
            last_pipe_time = current_time
        
        add_pipe = False
        remove_pipes = []
        # Updates and draws new pipe
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if check_collision(bird, pipes):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + PIPE_WIDTH < 0:
                remove_pipes.append(pipe)

            pipe.update()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe())

        for r in remove_pipes:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        # Removes pipes that are out of screen
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        draw_window(birds, pipes, score)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config-feedforward.txt")
    run(config_path)