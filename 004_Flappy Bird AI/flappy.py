'''
Flappy Bird AI using Python, pygame and NEAT
CodeSpace
'''
# Importing modules
import pygame
import neat
import os
import random

# Adding display caption and font initialization
pygame.display.set_caption('Flappy Bird AI')
pygame.font.init()

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FLOOR = 730
DRAW_TRAJECTORY = True
GAME_FONT = pygame.font.SysFont('montserratsemibold', 30)
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Loading images
bird_img = [pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird_' + str(x) + '.png'))) for x in range(1, 4)]
bg_img = pygame.transform.scale(pygame.image.load(os.path.join('img','bg.png')).convert_alpha(), (600, 900))
floor_img = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'floor.png')))
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'pipe.png')))

generation = 0

# Flappy Bird class
class Bird:
    IMG = bird_img
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    # Initialization of bird
    def __init__(self, x, y):
        self.img = self.IMG[0]
        self.img_count = 0
        self.x = x
        self.y = y
        self.height = self.y
        self.velocity = 0
        self.tilt = 0
        self.tick_count = 0

    # Bird's jump function
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    # Bird's movement
    def move(self):
        self.tick_count += 1
        displacement = self.velocity * self.tick_count + 1.5 * pow(self.tick_count, 2)
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2
        self.y = self.y + displacement
        if (displacement < 0) or (self.y < self.height + 50):
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    # Drawing bird in game
    def draw(self, window):
        self.img_count += 1
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMG[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMG[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMG[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMG[1]
        elif self.img_count <= self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMG[0]
            self.img_count = 0
        if self.tilt <= -80:
            self.img = self.IMG[1]
            self.img_count = self.ANIMATION_TIME * 2
        rotateObject(window, self.img, (self.x, self.y), self.tilt)

    # Get the bird's current mask
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# Pipe class
class Pipe():
    GAP = 200
    VELOCITY = 5

    # Initialization of pipe
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.TOP_PIPE = pygame.transform.flip(pipe_img, False, True)
        self.BOTTOM_PIPE = pipe_img
        self.passed = False
        self.set_height()

    # Sets the pipe's height
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bottom = self.height + self.GAP

    # Pipe's movement
    def move(self):
        self.x -= self.VELOCITY

    # Drawing pipes in game
    def draw(self, window):
        window.blit(self.TOP_PIPE, (self.x, self.top))
        window.blit(self.BOTTOM_PIPE, (self.x, self.bottom))

    # Detecting colliding of bird with pipe
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        bottom_mask = pygame.mask.from_surface(self.BOTTOM_PIPE)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        if top_point or bottom_point:
            return True
        return False

# Floor class
class Floor:
    IMG = floor_img
    VELOCITY = 5
    WIDTH = floor_img.get_width()

    # Initialization of floor
    def __init__(self, y):
        self.y = y
        self.tile_1 = 0
        self.tile_2 = self.WIDTH

    # Floor's movement
    def move(self):
        self.tile_1 -= self.VELOCITY
        self.tile_2 -= self.VELOCITY
        if self.tile_1 + self.WIDTH < 0:
            self.tile_1 = self.tile_2 + self.WIDTH
        if self.tile_2 + self.WIDTH < 0:
            self.tile_2 = self.tile_1 + self.WIDTH

    # Drawing pipes in game
    def draw(self, window):
        window.blit(self.IMG, (self.tile_1, self.y))
        window.blit(self.IMG, (self.tile_2, self.y))

# Rotating objects and bliting
def rotateObject(surface, img, topleft, angle):
    img_rotated = pygame.transform.rotate(img, angle)
    new_rectangle = img_rotated.get_rect(center = img.get_rect(topleft = topleft).center)
    surface.blit(img_rotated, new_rectangle.topleft)

# Drawinf game window
def draw_window(window, birds, pipes, floor, score, generation, pipe_index):
    window.blit(bg_img, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    floor.draw(window)
    for bird in birds:
        if DRAW_TRAJECTORY:
            try:
                pygame.draw.line(window, (153, 255, 51), (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (pipes[pipe_index].x + pipes[pipe_index].TOP_PIPE.get_width() / 2, pipes[pipe_index].height), 2)
                pygame.draw.line(window, (153, 255, 51), (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (pipes[pipe_index].x + pipes[pipe_index].BOTTOM_PIPE.get_width() / 2, pipes[pipe_index].bottom), 2)
            except:
                pass
        bird.draw(window)
    text_score = GAME_FONT.render('Score: ' + str(score), 1, (255, 69, 0))
    window.blit(text_score, (WINDOW_WIDTH - text_score.get_width() - 15, 10))
    text_score = GAME_FONT.render('Generation: ' + str(generation - 1), 1, (255, 69, 0))
    window.blit(text_score, (10, 10))
    text_score = GAME_FONT.render('Alive birds: ' + str(len(birds)), 1, (255, 69, 0))
    window.blit(text_score, (10, 50))
    pygame.display.update()

# Simulation of the current generation
def evolution(genomes, config):
    global WINDOW, generation
    window = WINDOW
    generation += 1
    networks = []
    birds = []
    gen = []
    for _, genome in genomes:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        birds.append(Bird(300, 365))
        gen.append(genome)
    floor = Floor(FLOOR)
    pipes = [Pipe(700)]
    score = 0
    clock = pygame.time.Clock()
    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        pipe_index = 0
        if len(birds) > 0:
            if (len(pipes) > 1) and (birds[0].x > pipes[0].x + pipes[0].TOP_PIPE.get_width()):
                pipe_index = 1
        for i, bird in enumerate(birds):
            gen[i].fitness += 0.1
            bird.move()
            output = networks[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))
            if output[0] > 0.5:
                bird.jump()
        floor.move()
        remove_pipe = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.collide(bird):
                    gen[birds.index(bird)].fitness -=1
                    networks.pop(birds.index(bird))
                    gen.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipe.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            score += 1
            for genome in gen:
                genome.fitness += 5
            pipes.append(Pipe(WINDOW_WIDTH))
        for pipe in remove_pipe:
            pipes.remove(pipe)
        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                networks.pop(birds.index(bird))
                gen.pop(birds.index(bird))
                birds.pop(birds.index(bird))
        draw_window(WINDOW, birds, pipes, floor, score, generation, pipe_index)

# Running the NEAT algorithm
def NEATrun(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(evolution, 20)

# Searching path to configuration file
if __name__ == '__main__':
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'config.txt')
    NEATrun(config_path)
