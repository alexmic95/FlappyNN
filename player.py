import pygame
from blocks import UpperBlock, LowerBlock


class Player:
    def __init__(self, winsize):
        self.x = int(winsize/2)
        self.y = int(winsize/2)
        self.winsize = winsize
        self.x_vel = 0
        self.y_vel = 0
        self.size = 30
        self.halfsize = int(self.size / 2)
        self.score_dist = 0
        self.rect = pygame.Rect((self.x - self.halfsize, self.y - self.halfsize), (self.size, self.size))
        self.img = pygame.image.load("bird.png")
        self.img = pygame.transform.scale(self.img, (30, 30))

    def draw(self, win):
        self.rect.x = self.x - self.halfsize
        self.rect.y = self.y - self.halfsize
        #pygame.draw.rect(win, (255, 145, 0), (self.x - self.halfsize, self.y - self.halfsize, self.size, self.size))
        win.blit(self.img, self.rect)

    def move(self):
        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel
        if self.x + self.halfsize > self.winsize:
            self.x = self.winsize - self.halfsize
        elif self.x - self.halfsize < 0:
            self.x = 0 + self.halfsize
        if self.y + self.halfsize > self.winsize:
            self.y = self.winsize - self.halfsize
            self.y_vel = 0
        elif self.y - self.halfsize < 0:
            self.y = 0 + self.halfsize
            self.y_vel = 0

    def gravity(self):
        self.y_vel = self.y_vel + 0.5
        if self.y_vel > 7:
            self.y_vel = 7

    def jump(self):
        self.y_vel -= 15
        if self.y_vel < -8:
            self.y_vel = -8

    def score_dist_add(self):
        self.score_dist = self.score_dist + 1

    def getdists(self, blocks):
        y_vel = self.y_vel
        y = self.y
        nextblockdist = 1000
        for block in blocks:
            if type(block) is UpperBlock:
                if (block.x + 50) - (self.x - self.halfsize) <= nextblockdist:
                    if (block.x + 50) - (self.x - self.halfsize) > 0:
                        nextblockdist = (block.x + 50) - (self.x - self.halfsize)
                        nextublock = block
            elif type(block) is LowerBlock:
                if (block.x + 50) - (self.x - self.halfsize) <= nextblockdist:
                    if (block.x + 50) - (self.x - self.halfsize) > 0:
                        nextblockdist = (block.x + 50) - (self.x - self.halfsize)
                        nextlblock = block
        return y, y_vel, nextblockdist, nextublock.y, nextlblock.y
