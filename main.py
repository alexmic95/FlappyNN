import pygame
from player import Player
from blocks import UpperBlock, LowerBlock
# import os
import neat

# headless mode
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.environ["SDL_VIDEODRIVER"] = "dummy"


class FlappyNNGame:
    def __init__(self):
        self.winsize = 500
        pygame.init()
        self.win = pygame.display.set_mode((self.winsize, self.winsize))
        self.bg = pygame.image.load("bg500.png")
        pygame.display.set_caption("FlappyNN")
        self.player = Player(self.winsize)
        self.blocktimer = 0
        self.blocks = []
        self.hitlist = []
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.jump()
            if self.blocktimer == 0:
                self.blocks.append(UpperBlock(self.winsize))
                self.blocks.append(LowerBlock(self.winsize, self.blocks[-1]))
                self.blocktimer = self.blocktimer + 1
            elif self.blocktimer == 80:
                self.blocktimer = 0
            else:
                self.blocktimer = self.blocktimer + 1
            for block in self.blocks:
                if block.x < -50:
                    self.blocks.remove(block)
            # print(self.player.getdists(self.blocks))

            self.player.gravity()
            self.player.move()

            self.win.blit(self.bg, (0, 0))

            for block in self.blocks:
                block.move()
                block.draw(self.win)

            self.player.draw(self.win)

            pygame.display.update()

            self.hitlist.clear()
            for block in self.blocks:
                self.hitlist.append(block.hitplayer(self.player))
            if any(self.hitlist):
                self.clock.tick(1)
                print(self.player.score_dist)
                self.player = Player(self.winsize)
                self.blocks.clear()
                self.blocktimer = 0
            self.player.score_dist_add()


    def __rungamenn(self, genomes, config):
        runninglist = []
        players = []
        nets = []
        ge = []
        self.blocks = []
        self.blocktimer = 0
        for _, g in genomes:
            players.append(Player(self.winsize))
            nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            g.fitness = 0
            ge.append(g)
            runninglist.append(True)

        while any(runninglist):
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if self.blocktimer == 0:
                self.blocks.append(UpperBlock(self.winsize))
                self.blocks.append(LowerBlock(self.winsize, self.blocks[-1]))
                self.blocktimer = self.blocktimer + 1
            elif self.blocktimer == 80:
                self.blocktimer = 0
            else:
                self.blocktimer = self.blocktimer + 1
            for block in self.blocks:
                if block.x < -50:
                    self.blocks.remove(block)
            for x, player in enumerate(players):
                if runninglist[x]:
                    output = nets[x].activate(player.getdists(self.blocks))
                    if output[0] > 0.5:
                        player.jump()
                    player.gravity()
                    player.move()
            self.win.blit(self.bg, (0, 0))

            for block in self.blocks:
                block.move()
                block.draw(self.win)

            for x, player in enumerate(players):
                if runninglist[x]:
                    player.draw(self.win)
            pygame.display.update()

            for x, player in enumerate(players):
                if runninglist[x]:
                    self.hitlist.clear()
                    for block in self.blocks:
                        self.hitlist.append(block.hitplayer(player))
                    if any(self.hitlist):
                        runninglist[x] = False
                    else:
                        player.score_dist_add()
                        ge[x].fitness = player.score_dist






    def runga(self):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "neatconfig.txt")
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.__rungamenn, 50)



if __name__ == "__main__":
    game = FlappyNNGame()
    game.runga()
