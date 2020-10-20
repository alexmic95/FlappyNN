import pygame
from player import Player
from blocks import UpperBlock, LowerBlock

pygame.init()

winsize = 500

win = pygame.display.set_mode((winsize, winsize))

pygame.display.set_caption("FlappyNN")

player = Player(winsize)
blocktimer = 0
blocks = []

clock = pygame.time.Clock()


# mainloop
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()

    keys = pygame.key.get_pressed()

    if blocktimer == 0:
        blocks.append(UpperBlock(winsize))
        blocks.append(LowerBlock(winsize, blocks[-1]))
        blocktimer = blocktimer + 1
    elif blocktimer == 80:
        blocktimer = 0
    else:
        blocktimer = blocktimer + 1
    for block in blocks:
        if block.x < -50:
            blocks.remove(block)

    player.gravity()
    player.move()

    win.fill((0, 0, 0))

    for block in blocks:
        block.move()
        block.draw(win)

    player.draw(win)

    pygame.display.update()
