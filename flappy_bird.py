import pygame
from pygame.locals import  *
import sys

from sprites.bird import Bird
from sprites.pipe import Pipe, PipeManager
from sprites.interactions import BirdPipeInteractionManager
from sprites.ground import Ground

pygame.init()

FPS = 120
SCREENWIDTH = 700
SCREENHEIGHT = 1024

display = pygame.display.set_mode((SCREENWIDTH , SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird By Dhyanesh")

crash_sound = pygame.mixer.Sound("assets/sounds/crash.mp3")
point_sound = pygame.mixer.Sound("assets/sounds/point.ogg")
jump_sound = pygame.mixer.Sound("assets/sounds/jump.ogg")

bird = Bird(display)
bird.start()
bird.add_jump_sound(jump_sound)

pipe_manager = PipeManager(display)
pipe_manager.start()

bird_pipe_interaction_manager = BirdPipeInteractionManager(bird, pipe_manager)

ground = Ground(display)
ground.start()

BIRD_FLAP = pygame.USEREVENT
pygame.time.set_timer(BIRD_FLAP, 100)

ADDPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPIPE, 900)

def collision():
    pipe_manager.stop()
    bird.stop()
    ground.stop()
    pass
    
bird_pipe_interaction_manager.add_collision_callback(collision)
bird_pipe_interaction_manager.add_collision_sound(crash_sound)
bird_pipe_interaction_manager.add_pass_through_sound(point_sound)

game_started = True
while True:
    display.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_started:
            if (event.type  == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
            if event.type == BIRD_FLAP:
                bird.flap()
            if event.type == ADDPIPE:
                pipe_manager.add_pipe()
    if game_started:
        pipe_manager.render()
        bird.render()
        bird_pipe_interaction_manager.handle_interactions()
    else:
        ground.stop()
    ground.render()
    pygame.display.update()
    clock.tick(FPS)