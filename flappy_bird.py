import pygame
import ctypes
import sys

from game import Game, HomeScreen, DisplayHandler, Score

ctypes.windll.shcore.SetProcessDpiAwareness(1)
pygame.init()

FPS = 120
SCREENWIDTH = 700
SCREENHEIGHT = 1024

display = pygame.display.set_mode((SCREENWIDTH , SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird By Dhyanesh")

icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

display_handler = DisplayHandler()

font = pygame.font.Font("assets/fonts/score_font.TTF", 50)
score = Score(display=display, font=font)

game = Game(display, display_handler, score)
home_screen = HomeScreen(display, display_handler, score)

display_handler.set_current_state('home_screen')

while True:
    display.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        display_handler.handle_event(event)
    
    display_handler.render()
    
    pygame.display.update()
    clock.tick(FPS)
    