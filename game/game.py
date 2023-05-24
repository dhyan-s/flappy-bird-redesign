import pygame
import os, sys

from sprites.bird import Bird
from sprites.pipe import PipeManager
from sprites.ground import Ground

from .interactions import BirdPipeInteractionManager, BirdCollisionManager
from .display_handler import DisplayHandler
from .score import Score

class Game:
    """
    A class that brings together all the sprites and objects to create a fun and engaging Flappy Bird game.
    """
    
    def __init__(self, display: pygame.Surface, display_handler: DisplayHandler, score_handler: Score) -> None:
        self.display = display
        self.display_handler = display_handler
        self.display_handler.add_state('game', self)
        self.score_handler = score_handler
        
    def game_over(self) -> None:
        """The method that is called when the game is over"""
        self.pipe_manager.stop()
        self.display_handler.set_current_state('home_screen')
        
    def load(self) -> None:
        """
        Loads the game dependencies and initializes the game objects.
        """
        self.crash_sound = pygame.mixer.Sound("assets/sounds/crash.mp3")
        self.point_sound = pygame.mixer.Sound("assets/sounds/point.ogg")
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.ogg")
        
        self.background = pygame.image.load(f"{os.path.dirname(__file__)}/background.png").convert()
        self.background = pygame.transform.scale(self.background, (self.display.get_width(), self.display.get_height()))
        
        self.bird = Bird(self.display)
        self.bird.start()
        self.bird.add_jump_sound(self.jump_sound)

        self.pipe_manager = PipeManager(self.display)

        self.bird_pipe_interaction_manager = BirdPipeInteractionManager(self.bird, self.pipe_manager)
        self.bird_pipe_interaction_manager.add_collision_callback(self.game_over)
        self.bird_pipe_interaction_manager.add_collision_sound(self.crash_sound)
        self.bird_pipe_interaction_manager.add_pass_through_callback(self.score_handler.increment_score)
        self.bird_pipe_interaction_manager.add_pass_through_sound(self.point_sound)
        
        self.ground = Ground(self.display)
        
        self.bird_collision_manager = BirdCollisionManager(self.bird, self.ground)
        self.bird_collision_manager.add_collision_callback(self.game_over)
        self.bird_collision_manager.add_collision_sound(self.crash_sound)

        self.BIRD_FLAP = pygame.USEREVENT
        pygame.time.set_timer(self.BIRD_FLAP, 100)

        self.START_PIPES = pygame.USEREVENT + 1
        
    def on_set_active(self) -> None:
        """The function that is called when this screen is set active by the DisplayHandler object."""
        self.score_handler.reset_score()
        self.bird.reset()
        self.pipe_manager.reset()
        self.bird.jump()
        pygame.time.set_timer(self.START_PIPES, 400)
        
    def render(self) -> None:
        """Renders the game objects and handles game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type  == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.jump()
            if event.type == self.BIRD_FLAP:
                self.bird.flap()
            if event.type == self.START_PIPES:
                self.pipe_manager.start()
                pygame.event.clear(self.START_PIPES)
        self.display.blit(self.background, (0, 0))
        self.pipe_manager.render()
        self.bird.render()
        self.bird_pipe_interaction_manager.handle_interactions()
        self.bird_collision_manager.handle_collision()
        self.ground.render()
        self.score_handler.render_score(y=100)
