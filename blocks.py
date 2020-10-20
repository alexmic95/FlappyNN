import pygame
import random


class UpperBlock:
    def __init__(self, winsize):
        self.x = winsize
        maxy = winsize - 200
        miny = 50
        self.y = random.randint(miny, maxy)

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, 0, 50, self.y))

    def move(self):
        self.x = self.x - 3


class LowerBlock:
    def __init__(self, winsize, ublock):
        self.x = winsize
        self.y = ublock.y + 150
        self.winsize = winsize

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 50, self.winsize - self.y))

    def move(self):
        self.x = self.x - 3
