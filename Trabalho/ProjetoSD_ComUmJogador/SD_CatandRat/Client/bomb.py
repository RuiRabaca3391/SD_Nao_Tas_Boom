import pygame



class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, w_size: int, *groups):
        super().__init__(*groups)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load('bomb.gif')
        initial_size = self.image.get_size()
        size_rate = w_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * w_size, pos_y * w_size), self.image.get_size())
        self.ticks = 0

    def get_size(self):
        return self.new_size

    def update(self, game: object, dt):
        self.ticks += dt
        #world_now = game.world[(self.pos_x, self.pos_y)]
        #print("Time", world_now)
        #if world_now != []:
        if self.ticks / 1000 >= 2.5:
            self.kill()
        self.dirty = 1
