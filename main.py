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
        self.winsize = 500  # window size
        pygame.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)  # font for ingame text
        self.win = pygame.display.set_mode((self.winsize, self.winsize))
        self.bg = pygame.image.load("bg500.png")  # background image
        pygame.display.set_caption("FlappyNN")  # caption in game window
        self.player = Player(self.winsize)  # initiate the player
        self.blocktimer = 0  # variable to count when its time to spawn new blocks
        self.blocks = []  # list of blocks which are currently displayed
        self.hitlist = []   # list to check if a block got hit by the player
        self.clock = pygame.time.Clock()
        self.running = True
        self.highscore = 0  # variable to save the current highscore

    def run(self):
        while self.running:
            self.clock.tick(60)     # set FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:    # detect if player wants to jump
                    if event.key == pygame.K_UP:
                        self.player.jump()
            if self.blocktimer == 0:    # if blocktimer is zero new blocks get spawned
                self.blocks.append(UpperBlock(self.winsize))
                self.blocks.append(LowerBlock(self.winsize, self.blocks[-1]))
                self.blocktimer = self.blocktimer + 1
            elif self.blocktimer == 80:     # reset blocktimer to zero after 80 frames
                self.blocktimer = 0
            else:
                self.blocktimer = self.blocktimer + 1   # increase blocktimer in every second
            for block in self.blocks:   # delete blocks if they went out of vision range
                if block.x < -50:
                    self.blocks.remove(block)
            # print(self.player.getdists(self.blocks))

            self.player.gravity()   # affet gravity on the player object
            self.player.move()  # move the player objet depending on the current speed of the player

            self.win.blit(self.bg, (0, 0))  # drawing the background

            for block in self.blocks:   # move the blocks to the left and draw the blocks
                block.move()
                block.draw(self.win)

            self.player.draw(self.win)      # draw the player

            # display current score and highscore
            text_score = self.myfont.render("current score: " + str(self.player.score), True, (0, 0, 0))
            text_highscore = self.myfont.render("highscore: " + str(self.highscore), True, (0, 0, 0))
            self.win.blit(text_score, (10, 10))
            self.win.blit(text_highscore, (10, 25))

            pygame.display.update()

            self.hitlist.clear()
            for block in self.blocks:   # collision detection
                self.hitlist.append(block.hitplayer(self.player))
            if any(self.hitlist):   # if player hit a block, reset game and save score as highscore if necessary
                self.clock.tick(1)
                print("You achieved " + str(self.player.score) + " points!")
                if self.player.score > self.highscore:
                    self.highscore = self.player.score
                self.player = Player(self.winsize)
                self.blocks.clear()
                self.blocktimer = 0
            self.player.score_point(self.blocks)  # check if player passed another pair of blocks

    # method that runs the nn version of the game
    def __rungamenn(self, genomes, config):
        runninglist = []    # list how many players are still alive
        players = []    # list of all players controlled by the nn's
        nets = []   # list of the neural networks controlling the players
        ge = []     # list of genomes
        maxfitness = 0  # variable to store the best fitness value
        self.blocks = []    # list of blocks
        self.blocktimer = 0     # counter to check if its time to spawn a new block
        for _, g in genomes:  # loop to create the nets
            players.append(Player(self.winsize))
            nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            g.fitness = 0
            ge.append(g)
            runninglist.append(True)

        while any(runninglist):
            self.clock.tick(60)  # set FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if self.blocktimer == 0:    # spawn new blocks if necessary
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
            for x, player in enumerate(players):    # check if net wants the player to jump
                if runninglist[x]:
                    output = nets[x].activate(player.getdists(self.blocks))
                    if output[0] > 0.5:
                        player.jump()
                    player.gravity()
                    player.move()
            self.win.blit(self.bg, (0, 0))

            for block in self.blocks:   # move and draw the blocks
                block.move()
                block.draw(self.win)

            for x, player in enumerate(players):    # draw the players
                if runninglist[x]:
                    player.draw(self.win)
            # display current fitness and how many individuals are alive as text on screen
            text_current_fitness = self.myfont.render("current fitness: " + str(maxfitness) , True, (0, 0, 0))
            text_indv_alive = self.myfont.render("individuals alive: " + str(runninglist.count(True)), True, (0, 0, 0))
            self.win.blit(text_current_fitness, (10, 10))
            self.win.blit(text_indv_alive, (10, 25))
            pygame.display.update()

            for x, player in enumerate(players):  # collision detection for all players
                if runninglist[x]:
                    self.hitlist.clear()
                    for block in self.blocks:
                        self.hitlist.append(block.hitplayer(player))
                    if any(self.hitlist):
                        runninglist[x] = False
                    else:
                        player.score_dist_add()
                        ge[x].fitness = player.score_dist   # save fitness of the individual after dying
                        if ge[x].fitness > maxfitness:
                            maxfitness = ge[x].fitness
                        if ge[x].fitness > 10000:   # cancel ga if threshold is reached
                            runninglist[x] = False

    def runga(self):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, "neatconfig.txt")  # load the neat config from config file
        p = neat.Population(config)     # create the population
        p.add_reporter(neat.StdOutReporter(True))  # add a reporter to check progress after every generation
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.__rungamenn, 50)  # run the ga


if __name__ == "__main__":
    # add a decision to play yourself(1) or train a nn to play the game(2)
    inputstr = "Falls du selber spielen möchtest, tippe 1.\n" \
               "Falls du ein neuronales Netz trainieren möchtest, welches das Spiel spielt, tippe 2.\n" \
               "Falls du abbrechen möchtest, mache eine andere beliebige Eingabe.\n"
    i = input(inputstr)
    if i == "1":
        game = FlappyNNGame()
        game.run()
    elif i == "2":
        game = FlappyNNGame()
        game.runga()

        

