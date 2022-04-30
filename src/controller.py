import sys
import pygame
import random
from src import hero
from src import enemy
from src import sapling


class Controller:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((250, 250, 250))  # set the background to white
        pygame.font.init()  # you have to call this at the start, if you want to use this module.
        pygame.key.set_repeat(1, 50)  # initialize a held keey to act as repeated key strikes
        """Load the sprites that we need"""

        self.enemies = pygame.sprite.Group()
        num_enemies = 3
        for i in range(num_enemies):
            x = random.randrange(100, 400)
            y = random.randrange(100, 400)
            self.enemies.add(enemy.Enemy("Boogie", x, y, 'assets/enemy.png'))
        self.hero = hero.Hero("Conan", 50, 80, "assets/hero.png")
        self.all_sprites = pygame.sprite.Group((self.hero,) + tuple(self.enemies))
        self.state = "GAME"

        # Variables for trees
        self.saplings = pygame.sprite.Group()
        self.treecount = 0

        # Moved some variables for convenience
        self.myfont = pygame.font.SysFont(None, 30)
        
        

    def mainLoop(self):
        while True:
            if(self.state == "GAME"):
                self.gameLoop()
            elif(self.state == "GAMEOVER"):
                self.gameOver()
            elif(self.state == "WIN"):
                self.gameWin()

    def gameLoop(self):
        while self.state == "GAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_UP):
                        self.hero.move_up()
                    elif(event.key == pygame.K_DOWN):
                        self.hero.move_down()
                    elif(event.key == pygame.K_LEFT):
                        self.hero.move_left()
                    elif(event.key == pygame.K_RIGHT):
                        self.hero.move_right()
                    # Plant a tree by pressing space
                    if(event.key == pygame.K_SPACE):
                      self.plantTree()

            # check for collisions
            fights = pygame.sprite.spritecollide(self.hero, self.enemies, True)
            if(fights):
                for e in fights:
                    if(self.hero.fight(e)):
                        e.kill()
                        self.background.fill((250, 250, 250))
                    else:
                        self.background.fill((250, 0, 0))
                        self.enemies.add(e)

            # redraw the entire screen
            self.enemies.update()
            self.screen.blit(self.background, (0, 0))
            # Constantly updates tree count
            self.updateTreeCount()
            if(self.hero.health == 0):
                self.state = "GAMEOVER"
            if(self.treecount >= 50):
                self.state = "WIN"
            self.saplings.draw(self.screen)
            self.all_sprites.draw(self.screen)


            # update the screen
            pygame.display.flip()

    def gameOver(self):
        self.hero.kill()
        message = self.myfont.render('Game Over', False, (0, 0, 0))
        self.screen.blit(message, (self.width / 2, self.height / 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def gameWin(self):
        '''
        Draws the game completion screen.
        '''
        win_message = self.myfont.render('You won!', False, (0, 0, 0))
        self.background.fill((46, 226, 51))
        self.screen.blit(self.background, (0,0))
        self.updateTreeCount()
        self.screen.blit(win_message, (self.width / 2, self.height / 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
    def plantTree(self):
        '''
        Plants a tree in front of the hero.
        '''
        x = self.hero.rect.x + 70    # Some random numbers so the tree
        y = self.hero.rect.y + 30    # lands in front of the hero
        self.saplings.add(sapling.Sapling(x, y, "assets/sapling2.png"))
        self.treecount += 1

    def updateTreeCount(self):
        '''
        Updates the tree count on screen.
        '''
        treecount_message = f'Trees planted: {self.treecount}'
        treecount = self.myfont.render(treecount_message , False, (0, 0, 0))
        self.screen.blit(treecount, (10, 10))
        