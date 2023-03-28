import time

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.rows * cell_size
        self.height = life.cols * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        matrix = self.life.curr_generation
        y = 0
        for i in range(0, len(matrix)):
            x = 0
            for j in range(0, len(matrix[i])):
                if matrix[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("green"), (x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        self.draw_grid()
        self.draw_lines()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        pause = False
        start = False
        pygame.display.flip()
        while (not self.life.is_max_generations_exceeded and self.life.is_changing) or start == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = x // self.cell_size
                    coll = y // self.cell_size
                    self.life.curr_generation[coll][row] = 1
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
            if pause:
                continue
            if start:
                self.life.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
                time.sleep(1)
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((15, 15), randomize=True, max_generations=15)
    gui = GUI(game, 30, 30)
    gui.run()
