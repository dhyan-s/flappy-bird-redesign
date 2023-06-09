import pygame
import os

class Pipe:
    """Represents a pair of pipes in the game."""
    
    def __init__(self, display: pygame.Surface, x: int | float, y: int | float) -> None:
        self.display = display
        self.moving: bool = False
        
        self.x_pos: int = x
        self.y_pos: int = y
        
        self.pipe: pygame.Surface
        self.top_pipe: pygame.Rect
        self.bottom_pipe: pygame.Rect
        self.mask: pygame.mask.Mask
        
        self.load_pipes()
        
    def start(self) -> None:
        """Starts the movement of the pipes."""
        self.moving = True
        
    def stop(self) -> None:
        """Stops the movement of the pipes."""
        self.moving = False
        
    def load_pipes(self) -> None:
        """
        Loads the pipe image, scales it to the desired size,
        sets the position of the top and bottom pipes, creates a collision mask,
        and updates the pipe positions.
        """
        cur_dir = os.path.dirname(__file__)
        
        self.pipe = pygame.image.load(f"{cur_dir}/pipe.png")
        self.pipe = pygame.transform.scale(self.pipe, (145, 550))
        
        self.bottom_pipe = self.pipe.get_rect(midtop = (self.x_pos, self.y_pos))
        self.top_pipe = self.pipe.get_rect(midbottom = (self.x_pos, self.y_pos - 280))
        
        self.mask = pygame.mask.from_surface(self.pipe)
        
        self.update_pipe_pos()
        
    def update_pipe_pos(self) -> None:
        """Updates the positions of the top and bottom pipes."""
        self.bottom_pipe.midtop = (self.x_pos, self.y_pos)
        self.top_pipe.midbottom = (self.x_pos, self.y_pos - 280)
        
    def render(self) -> None:
        """Renders the pipes on the display surface."""
        self.display.blit(self.pipe, self.top_pipe)
        self.display.blit(self.pipe, self.bottom_pipe)
        if self.moving:
            self.update_pipe_pos()
            self.x_pos -= 6.1
