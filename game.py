import pygame
import random
import sys
import neat
import os

# Screen Dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Bird Constants 
JUMP = -10.5
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
        self.height = self.y
        self.velocity = 0
        self.fitness = 0
        self.tick_count = 0
    
    def jump(self):
        self.velocity = JUMP
        self.tick_count = 0
        self.height = self.y

    def update(self):
        self.tick_count += 1

        displace = self.velocity*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        
        if displace >= 16:
            displace = (displace/abs(displace)) * 16

        if displace < 0:
            displace -= 2

        self.y = self.y + displace

    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), BIRD_SIZE)

    def get_rect(self):
        return pygame.Rect(self.x - BIRD_SIZE, self.y - BIRD_SIZE, BIRD_SIZE * 2, BIRD_SIZE * 2)

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.passed = False
        
        self.set_height()
    
    def update(self):
        self.x -= PIPE_SPEED

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP
    
    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top))
        pygame.draw.rect(screen, BLACK, (self.x, self.bottom, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom))

# Checks for Collision
def check_collision(bird, pipes):
    bird_rect = bird.get_rect()
    
    # Check collision with pipes
    for pipe in pipes:
        top_pipe_rect = pygame.Rect(pipe.x, 0, PIPE_WIDTH, pipe.top)
        bottom_pipe_rect = pygame.Rect(pipe.x, pipe.bottom, PIPE_WIDTH, SCREEN_HEIGHT - pipe.bottom)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
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

    score_text = font.render(f"Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

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
        birds.append(Bird(230, 350))
        ge.append(genome)

    pipes = [Pipe(700)]
    running = True
    score = 0

    clock = pygame.time.Clock()

    while running and len(birds) > 0:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + PIPE_WIDTH:
                pipe_ind = 1
        else:
            running = False
            break

        for i, bird in enumerate(birds):
            ge[i].fitness += 0.1
            bird.update()

            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()
        
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
            pipes.append(Pipe(SCREEN_WIDTH))

        for r in remove_pipes:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

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