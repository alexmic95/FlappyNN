import pygame


class Player:
    def __init__(self, winsize):
        self.x = int(winsize/2)
        self.y = int(winsize/2)
        self.winsize = winsize
        self.x_vel = 0
        self.y_vel = 0
        self.size = 30
        self.halfsize = int(self.size / 2)

    def draw(self, win):

        pygame.draw.rect(win, (255, 255, 0), (self.x - self.halfsize, self.y - self.halfsize, self.size, self.size))

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

