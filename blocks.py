import pygame
import random

blockcolor = (37, 158, 0)


# class for upper blocks
class UpperBlock:
    def __init__(self, winsize):
        self.x = winsize
        maxy = winsize - 200
        miny = 50
        self.y = random.randint(miny, maxy)  # height randomly chosen
        self.scored = False  # variable that stores if the player passed the block yet

    def draw(self, win):
        pygame.draw.rect(win, blockcolor, (self.x, 0, 50, self.y))      # method to draw the block

    def move(self):     # mathod to move the block by 3 pixels every frame
        self.x = self.x - 3

    def hitplayer(self, player):  # collision detection method
        if player.x + player.halfsize < self.x:
            return False
        elif player.x - player.halfsize > self.x + 50:
            return False
        elif player.y - player.halfsize > self.y:
            return False
        else:
            return True


# class for lower blocks
class LowerBlock:
    def __init__(self, winsize, ublock):
        self.x = winsize
        self.y = ublock.y + 150  # height depends on the upper block
        self.winsize = winsize

    def draw(self, win):    # method to draw the block
        pygame.draw.rect(win, blockcolor, (self.x, self.y, 50, self.winsize - self.y))

    def move(self):     # method to move the block
        self.x = self.x - 3

    def hitplayer(self, player):    # method for collision detection
        if player.x + player.halfsize < self.x:
            return False
        elif player.x - player.halfsize > self.x + 50:
            return False
        elif player.y + player.halfsize < self.y:
            return False
        else:
            return True
