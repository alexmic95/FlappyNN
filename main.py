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
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
        self.win = pygame.display.set_mode((self.winsize, self.winsize))
        self.bg = pygame.image.load("bg500.png")
        pygame.display.set_caption("FlappyNN")
        self.player = Player(self.winsize)
        self.blocktimer = 0
        self.blocks = []
        self.hitlist = []
        self.clock = pygame.time.Clock()
        self.running = True
        self.highscore = 0

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

            text_score = self.myfont.render("current score: " + str(self.player.score), True, (0, 0, 0))
            text_highscore = self.myfont.render("highscore: " + str(self.highscore), True, (0, 0, 0))
            self.win.blit(text_score, (10, 10))
            self.win.blit(text_highscore, (10, 25))

            pygame.display.update()

            self.hitlist.clear()
            for block in self.blocks:
                self.hitlist.append(block.hitplayer(self.player))
            if any(self.hitlist):
                self.clock.tick(1)
                print("You achieved " + str(self.player.score) + " points!")
                if self.player.score > self.highscore:
                    self.highscore = self.player.score
                self.player = Player(self.winsize)
                self.blocks.clear()
                self.blocktimer = 0
            self.player.score_point(self.blocks)

    def __rungamenn(self, genomes, config):
        runninglist = []
        players = []
        nets = []
        ge = []
        maxfitness = 0
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
            text_current_fitness = self.myfont.render("current fitness: " + str(maxfitness) , True, (0, 0, 0))
            text_indv_alive = self.myfont.render("individuals alive: " + str(runninglist.count(True)), True, (0, 0, 0))
            self.win.blit(text_current_fitness, (10, 10))
            self.win.blit(text_indv_alive, (10, 25))
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
                        if ge[x].fitness > maxfitness:
                            maxfitness = ge[x].fitness
                        if ge[x].fitness > 10000:
                            runninglist[x] = False

    def runga(self):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "neatconfig.txt")
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.__rungamenn, 50)


if __name__ == "__main__":
    game = FlappyNNGame()
    game.run()
