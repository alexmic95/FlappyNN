import pygame
from player import Player

pygame.init()

winsize = 500

win = pygame.display.set_mode((winsize, winsize))

pygame.display.set_caption("FlappyNN")

player = Player(winsize)

clock = pygame.time.Clock()


# mainloop
run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()

    keys = pygame.key.get_pressed()

    player.gravity()
    player.move()

    win.fill((0, 0, 0))
    player.draw(win)

    pygame.display.update()
