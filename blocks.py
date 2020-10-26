import pygame
import random


class UpperBlock:
    def __init__(self, winsize):
        self.x = winsize
        maxy = winsize - 200
        miny = 50
        self.y = random.randint(miny, maxy)
        self.scored = False

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, 0, 50, self.y))

    def move(self):
        self.x = self.x - 3

    def hitplayer(self, player):
        if player.x + player.halfsize < self.x:
            return False
        elif player.x - player.halfsize > self.x + 50:
            return False
        elif player.y - player.halfsize > self.y:
            return False
        else:
            return True


class LowerBlock:
    def __init__(self, winsize, ublock):
        self.x = winsize
        self.y = ublock.y + 150
        self.winsize = winsize

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 50, self.winsize - self.y))

    def move(self):
        self.x = self.x - 3

    def hitplayer(self, player):
        if player.x + player.halfsize < self.x:
            return False
        elif player.x - player.halfsize > self.x + 50:
            return False
        elif player.y + player.halfsize < self.y:
            return False
        else:
            return True
