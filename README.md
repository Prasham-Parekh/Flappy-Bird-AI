**Flappy Bird AI (NEAT-based)**
This project implements a Flappy Bird-like game using Python and Pygame, where an AI controlled by a NEAT (NeuroEvolution of Augmenting Topologies) algorithm learns to play the game. The AI evolves through generations, improving its performance in avoiding pipes and surviving longer.

**Features**
AI Control: Uses NEAT to evolve a neural network for each bird, allowing it to learn from each generation.
Game Environment: Custom-built game environment with obstacles (pipes) that the AI must avoid.
Fitness Evaluation: Fitness function evaluates each bird's performance based on survival time and score.
Real-time AI Training: The AI learns and evolves by playing multiple generations of the game.

**Requirements**
1. To run the project, you need Python and the following dependencies:
    Python 3.x
    Pygame
    NEAT-Python
2. You can install the dependencies with:
    pip install pygame
    pip install neat-python

**How to Run**
1. Clone this repository to your local machine:
    git clone https://github.com/Prasham-Parekh/Flappy-Bird-AI.git
2. Navigate to the project directory:
    cd Flappy-Bird-AI
3. Run the game using the following command:
    python main.py
This will start the game, and you will see the AI agents evolve as they attempt to play the game.

**How It Works**
The NEAT algorithm evolves neural networks that control the bird in the game.
The fitness of each bird is calculated based on how long it survives and how many pipes it successfully navigates.
The best-performing birds are selected to produce offspring, and the cycle repeats for multiple generations.
Over time, the AI improves, learning how to avoid pipes more effectively.
