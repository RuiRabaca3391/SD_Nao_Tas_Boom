import pygame
# Player 7 is part of the test example 7
# It defines a sprite with size rate

# Constantes
from Server import game_mech
from Client.client_stub import StubClient

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
BOMB = 4


class Player(pygame.sprite.DirtySprite):
    def __init__(self,number: int, pos_x:int, pos_y:int, sq_size:int, *groups ):
        super().__init__(*groups)
        self.image = pygame.image.load('gato.gif')
        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())
        self.number = number

    def get_size(self):
        return self.new_size

    def moveto(self,new_x:int, new_y:int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, game: object, stub: object, player: str):
        if player == "p1":
            last = self.rect.copy()
            key = pygame.key.get_pressed()
            # Para qualqer tecla, há que pedir ao Game Mech que nova posição
            # o jogador ocupa
            if key[pygame.K_LEFT]:

                lst = stub.esquerda("p1")
                self.rect.x = lst[0] * self.sq_size
                self.rect.y = lst[1] * self.sq_size

            if key[pygame.K_RIGHT]:

                lst = stub.direita("p1")
                self.rect.x = lst[0] * self.sq_size
                self.rect.y = lst[1] * self.sq_size

            if key[pygame.K_UP]:

                lst = stub.cima("p1")
                self.rect.x = lst[0] * self.sq_size
                self.rect.y = lst[1] * self.sq_size

            if key[pygame.K_DOWN]:

                lst = stub.baixo("p1")
                self.rect.x = lst[0] * self.sq_size
                self.rect.y = lst[1] * self.sq_size

            if key[pygame.K_SPACE]:
                stub.espaco("p1")

            new = self.rect
            for cell in pygame.sprite.spritecollide(self, game.walls, False):
                self.rect = last
                cell = cell.rect
                if last.right <= cell.left and new.right > cell.left:
                    new.right = cell.left
                if last.left >= cell.right and new.left < cell.right:
                    new.left = cell.right
                if last.bottom <= cell.top and new.bottom > cell.top:
                    new.bottom = cell.top
                if last.top >= cell.bottom and new.top < cell.bottom:
                    new.top = cell.bottom
            #game.update_bombs(self.sq_size, stub)
            # Keep visible
            self.dirty = 1