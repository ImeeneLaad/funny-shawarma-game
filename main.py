import pygame
from start_screen import start_screen
from level1 import Game

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1100, 700))
    pygame.display.set_caption("The Shawarma Quest")

    start_screen(screen)


    game = Game()
    game.run()
