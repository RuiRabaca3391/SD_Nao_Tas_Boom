import pygame
from Client.client_stub import StubClient
import Client.player8
import Client.player_rato
from Client import wall8, bomb, explosion

import sys

# ---------------------
# The grid now is built based on the number of squares in x and y.
# This allows us to associate the size of the space to a matrix or to a dictionary
# that will keep data about each position in the environment.
# Moreover, we now can control the movement of the objects.
class Game(object):
    def __init__(self, x_nr_sq:int = 20, y_nr_sq:int = 20, grid_size:int  = 20):
        self.x_max = x_nr_sq
        self.y_max = y_nr_sq
        self.width, self.height = x_nr_sq * grid_size, y_nr_sq * grid_size
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("first game")
        self.clock = pygame.time.Clock()
        # RGB colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        # Grid
        self.grid_size = grid_size
        grid_colour = self.black
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.white)
        self.screen.blit(self.background,(0,0))
        self.draw_grid(self.black)
        # Atenção: O Game deveria pedir dimensões do jogo ao GameMech e
        # não o contrário. Portanto, GameMech deverá ser gerado fora do
        # Game.
        self.bombs_list = []
        self.bombs = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        #self.gm = game_mech.GameMech(self.x_max, self.y_max)
        self.stub = ""
        pygame.display.update()


    # Drawing a square grid
    def draw_grid(self, colour:tuple):

        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size,0), ( x * self.grid_size, self.height))
        for y in range(0,self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def create_players(self,size:int) -> None:
        #self.players = pygame.sprite.Group()
        self.players = pygame.sprite.LayeredDirty()
        # Atenção, os jogadores têm de ser criados pelo GameMech e só depois
        # gerados aqui pelo Game
        self.playerA = Client.player8.Player(0, 1,1,size,self.players)
        #self.playerB = Client.player_rato.PlayerR(0, 13, 11, size, self.players)
        self.players.add(self.playerA)
        #self.players.add(self.playerB)

    def create_walls(self, wall_size:int):
        # Create Wall (sprites) around world
        self.walls = pygame.sprite.Group()
        for x in range(0,self.x_max):
            for y in range(0,self.y_max):
                if x in (0,self.x_max - 1) or y in (0, self.y_max - 1) or ((x % 2) == 0 and (y % 2) == 0):
                    w = wall8.Wall(x, y, wall_size, self.walls)
                    self.walls.add(w)
        # More walls
        w = wall8.Wall(20, 20, wall_size, self.walls)
        self.walls.add(w)

    def update_bombs(self, bomb_size:int):
        bombs_now = self.gm.get_world()
        for x in range(0,self.x_max-1):
            for y in range(0,self.y_max-1):
                if bombs_now[(x, y)] != [] and bombs_now[(x, y)][0][1] == "bomb":
                    b = bomb.Bomb(x, y, bomb_size, self.bombs)
                    self.bombs.add(b)


    def update_explosions(self, explosion_size:int):
        explosion_now = self.gm.get_world()
        for x in range(0,self.x_max-1):
            for y in range(0,self.y_max-1):
                if explosion_now[(x, y)] != [] and explosion_now[(x, y)][0][1] == "explosion":
                    e = explosion.Explosion(x, y, explosion_size, self.explosions)
                    self.explosions.add(e)


    def run(self, stub):
        #Create Sprites
        self.create_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.create_players(self.grid_size)
        self.stub = stub

        end = False
        while end == False:
            dt = self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True

            #self.update_bombs(self.grid_size)
            #self.update_explosions(self.grid_size)
            self.players.update(self, self.stub)
            #self.bombs.update(self.gm)
            #self.explosions.update(self.gm)
            #bombas = self.bombs.draw(self.screen)
            #explosions = self.explosions.draw(self.screen)
            #self.explosions.update(dt)

            rects = self.players.draw(self.screen)
            #rects3 = self.explosions.draw(self.screen)

            #pygame.display.update(rects2)
            #pygame.display.update(rects3)
            pygame.display.update(rects)
            #pygame.display.update(bombas)
            #pygame.display.update(explosions)

            self.walls.draw(self.screen)
            #self.bombs.draw(self.screen)  # draw bombs here
            self.players.draw(self.screen)
            #self.explosions.draw(self.screen)
            self.draw_grid(self.black)

            pygame.display.update()

            self.players.clear(self.screen,self.background)
            #self.bombs.clear(self.screen, self.background)
            #self.explosions.clear(self.screen, self.background)

            # Verify if somebody blew up
            #if self.gm.somebody_blew_up() == True:
                #print("GAME ENDED WITH A BOOM!!!")
                #pygame.display.quit()
                #pygame.quit()
                #sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    gm = Game(15,13,65)
    gm.run()
