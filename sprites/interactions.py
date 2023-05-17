import pygame

from .bird import Bird
from .pipe import Pipe, PipeManager

class BirdPipeInteractionManager:
    def __init__(self, bird: Bird, pipe_manager: PipeManager):
        self.bird = bird
        self.pipe_manager = pipe_manager
        
        self.passing_pipe: Pipe = None
        self.colliding_pipe: Pipe = None
        
        self._on_pass_through = lambda: None
        self._on_collision = lambda: None
        
        self._pass_through_sound: pygame.mixer.Sound = None
        self._collision_sound: pygame.mixer.Sound = None
    
    def add_pass_through_callback(self, func) -> None:
        self._on_pass_through = func
        
    def remove_pass_through_callback(self) -> None:
        self._on_pass_through = lambda: None
        
    def add_collision_callback(self, func) -> None:
        self._on_collision = func
        
    def remove_collision_callback(self) -> None:
        self._on_collision = lambda: None
        
    def add_pass_through_sound(self, sound: pygame.mixer.Sound) -> None:
        self._pass_through_sound = sound
    
    def remove_pass_through_sound(self) -> None:
        self._pass_through_sound = None
    
    def add_collision_sound(self, sound: pygame.mixer.Sound) -> None:
        self._collision_sound = sound
    
    def remove_collision_sound(self) -> None:
        self._collision_sound = None
        
    def check_pass_through(self) -> tuple[bool, Pipe | None]:
        for pipe in self.pipe_manager:
            valid_x = (
                self.bird.centerx >= pipe.top_pipe.centerx
                and self.bird.centerx <= pipe.top_pipe.midright[0]
            )
            valid_y = (
                self.bird.top > pipe.top_pipe.midbottom[1]
                and self.bird.bottom < pipe.bottom_pipe.midtop[1]
            )
            if valid_x and valid_y:
                return (True, pipe)
        return (False, None)
        
    def handle_pass_through(self) -> None:
        passing_through, passing_pipe = self.check_pass_through()
        if passing_through and self.passing_pipe != passing_pipe:
            print('pass through')
            self._on_pass_through()
            if self._pass_through_sound is not None: 
                self._pass_through_sound.play()
        self.passing_pipe = passing_pipe
        
    def check_collision(self) -> tuple[bool, Pipe]:  # sourcery skip: use-next
        bird_mask = pygame.mask.from_surface(self.bird.bird)
        for pipe in self.pipe_manager:
            pipe_mask = pygame.mask.from_surface(pipe.pipe)
            top_pipe_offset = (pipe.top_pipe.x - self.bird.bird_rect.x, pipe.top_pipe.y - self.bird.bird_rect.y)
            bottom_pipe_offset = (pipe.bottom_pipe.x - self.bird.bird_rect.x, pipe.bottom_pipe.y - self.bird.bird_rect.y)
            if bird_mask.overlap(pipe_mask, top_pipe_offset) or bird_mask.overlap(pipe_mask, bottom_pipe_offset):
                return (True, pipe)
        return (False, None)
    
    def handle_collision(self) -> None:
        colliding, colliding_pipe = self.check_collision()
        if colliding and self.colliding_pipe != colliding_pipe:
            print('collision')
            self._on_collision()
            if self._collision_sound is not None:
                self._collision_sound.play()
        self.colliding_pipe = colliding_pipe
    
    def handle_interactions(self):      
        self.handle_collision()
        self.handle_pass_through()