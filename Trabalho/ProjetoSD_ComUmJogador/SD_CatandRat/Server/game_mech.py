class GameMech:
    def __init__(self, nr_max_x: int, nr_max_y: int):
        self.world = dict()
        self.players = dict()
        self.walls = dict()
        self.bombs = dict()
        self.explosions = dict()
        self.x_max = nr_max_x
        self.y_max = nr_max_y
        for x in range(nr_max_x):
            for y in range(nr_max_y):
                self.world[(x, y)] = []
        # Criar paredes à volta do mundo
        nr_walls = 0
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1) or ((x % 2) == 0 and (y % 2) == 0):
                    self.walls[nr_walls] = ["wall", (x, y)]
                    self.world[(x, y)].append(["obst", "wall", nr_walls])
                    nr_walls += 1
        # Criar jogador
        self.players[0] = ["p1", (1, 1)]
        self.world[(1, 1)].append(["player", "p1", 0])
        self.players[1] = ["p2", (13, 11)]
        self.world[(2, 2)].append(["player", "p2", 1])

    # Placing bombs in the grid
    def bomb_maker(self, x, y):
        if len(self.world[(x, y)]) == 1:
            nr_bombs = len(self.bombs)
            self.bombs[nr_bombs] = ["bomb", (x, y)]
            self.world[(x, y)].append(["obst", "bomb", nr_bombs, 0])

    # Tracking time ticks for bombs and calling explosion the time ticks function
    def bomb_ticking(self, ticks):
        for x in range(0, self.x_max - 1):
            for y in range(0, self.y_max - 1):
                if self.world[(x, y)] != [] and self.world[(x, y)][0][1] == "bomb":
                    self.world[(x, y)][0][3] += ticks
                    #print(self.world[(x, y)][0][3])
                    if self.world[(x, y)][0][3] / 1000 >= 3:
                        #print(self.world[(x, y)])
                        self.world[(x, y)].remove(self.world[(x, y)][0])
                        #print(self.world[(x, y)])
                        nr_explosions = len(self.explosions)
                        self.explosions[nr_explosions] = ["explosion", (x, y)]
                        self.world[(x, y)].append(["obst", "explosion", nr_explosions, 0])
                        self.explosion_maker(x, y)
                        #print(self.world[(x, y)])
        self.explosion_ticking(ticks)

    # Crossing explosion pattern and checking surroundings for walls
    def explosion_maker(self, x, y):
        if self.world[(x, y + 1)] == [] or self.world[(x, y + 1)][0][1] != ["wall"]:
            nr_explosions = len(self.explosions)
            self.explosions[nr_explosions] = ["explosion", (x, y + 1)]
            self.world[(x, y + 1)].append(["obst", "explosion", nr_explosions, 0])
            #print("y + 1")

        if self.world[(x, y - 1)] == [] or self.world[(x, y - 1)][0][1] != ["wall"]:
            nr_explosions = len(self.explosions)
            self.explosions[nr_explosions] = ["explosion", (x, y - 1)]
            self.world[(x, y - 1)].append(["obst", "explosion", nr_explosions, 0])
            #print("y - 1")

        if self.world[(x + 1, y)] == [] or self.world[(x + 1, y)][0][1] != ["wall"]:
            nr_explosions = len(self.explosions)
            self.explosions[nr_explosions] = ["explosion", (x + 1, y)]
            self.world[(x + 1, y)].append(["obst", "explosion", nr_explosions, 0])

        if self.world[(x - 1, y)] == [] or self.world[(x - 1, y)][0][1] != ["wall"]:
            nr_explosions = len(self.explosions)
            self.explosions[nr_explosions] = ["explosion", (x - 1, y)]
            self.world[(x - 1, y)].append(["obst", "explosion", nr_explosions, 0])

    # Checking if everybody is still in one piece
    def somebody_blew_up(self):
        for x in range(0,self.x_max-1):
            for y in range(0,self.y_max-1):
                check_it = []
                if self.world[(x, y)] != [] and len(self.world[(x, y)]) > 1:
                    for i in self.world[(x, y)]:
                        check_it.append(i[1])
                    #print(check_it)
                if ("p1" in check_it or "p2" in check_it) and "explosion" in check_it:
                    return True

    # Explosions time tick tracker
    def explosion_ticking(self, ticks):
        for x in range(0, self.x_max - 1):
            for y in range(0, self.y_max - 1):
                if self.world[(x, y)] != [] and self.world[(x, y)][0][1] == "explosion":
                    self.world[(x, y)][0][3] += ticks
                    # print(self.world[(x, y)][0][3])
                    if self.world[(x, y)][0][3] / 1000 >= 1.5:
                        # print(self.world[(x, y)])
                        self.world[(x, y)].remove(self.world[(x, y)][0])
                        # print(self.world[(x, y)])
                        # print(self.world[(x, y)])

    def go_up(self, nr_player: str) -> tuple:
        player_order = 0
        if nr_player == "p1":
            x = self.players[0][1][0]
            y = self.players[0][1][1]
            player_order = 0
        elif nr_player == "p2":
            x = self.players[1][1][0]
            y = self.players[1][1][1]
            player_order = 1

        name = nr_player
        new_x = x
        new_y = y - 1
        # Alterar o mundo - retirar o jogador em posição anterior e colocá-lo na nova posição
        # Atenção: Há que verificar que a nova posição não é umobstáculo. Se for, o jogador fica na mesma posição.
        test = self.world[(new_x, new_y)]

        if test == []:
            print(self.world[(x, y)])
            self.world[(x, y)].remove(["player", name, player_order])
            self.world[(new_x, new_y)].append(["player", name, player_order])
            # Alterar o jogador: colocar o jogador na nova posição
            self.players[player_order] = [name, (new_x, new_y)]

            return new_x, new_y
        else:
            return x, y

    def go_down(self, nr_player: str) -> tuple:
        player_order = 0
        if nr_player == "p1":
            x = self.players[0][1][0]
            y = self.players[0][1][1]
            player_order = 0
        elif nr_player == "p2":
            x = self.players[1][1][0]
            y = self.players[1][1][1]
            player_order = 1

        name = nr_player
        new_x = x
        new_y = y + 1
        # Alterar o mundo - retirar o jogador em posição anterior e colocá-lo na nova posição
        # Atenção: Há que verificar que a nova posição não é umobstáculo. Se for, o jogador fica na mesma posição.
        test = self.world[(new_x, new_y)]

        if test == []:
            print(self.world[(x, y)])
            self.world[(x, y)].remove(["player", name, player_order])
            self.world[(new_x, new_y)].append(["player", name, player_order])
            # Alterar o jogador: colocar o jogador na nova posição
            self.players[player_order] = [name, (new_x, new_y)]

            return new_x, new_y
        else:
            return x, y

    def go_right(self, nr_player: str) -> tuple:
        player_order = 0
        if nr_player == "p1":
            x = self.players[0][1][0]
            y = self.players[0][1][1]
            player_order = 0
        elif nr_player == "p2":
            x = self.players[1][1][0]
            y = self.players[1][1][1]
            player_order = 1

        name = nr_player
        new_x = x + 1
        new_y = y
        # Alterar o mundo - retirar o jogador em posição anterior e colocá-lo na nova posição
        # Atenção: Há que verificar que a nova posição não é umobstáculo. Se for, o jogador fica na mesma posição.
        test = self.world[(new_x, new_y)]
        print(test)

        if test == []:
            print(self.world[(x, y)])
            self.world[(x, y)].remove(["player", name, player_order])
            self.world[(new_x, new_y)].append(["player", name, player_order])
            # Alterar o jogador: colocar o jogador na nova posição
            self.players[player_order] = [name, (new_x, new_y)]

            return new_x, new_y
        else:
            return x, y

    def go_left(self, nr_player: str) -> tuple:
        player_order = 0
        if nr_player == "p1":
            x = self.players[0][1][0]
            y = self.players[0][1][1]
            player_order = 0
        elif nr_player == "p2":
            x = self.players[1][1][0]
            y = self.players[1][1][1]
            player_order = 1


        name = nr_player
        new_x = x - 1
        new_y = y
        # Alterar o mundo - retirar o jogador em posição anterior e colocá-lo na nova posição
        # Atenção: Há que verificar que a nova posição não é umobstáculo. Se for, o jogador fica na mesma posição.
        test = self.world[(new_x, new_y)]
        print(test)

        if test == []:
            print(self.world[(x, y)])
            self.world[(x, y)].remove(["player", name, player_order])
            self.world[(new_x, new_y)].append(["player", name, player_order])
            # Alterar o jogador: colocar o jogador na nova posição
            self.players[player_order] = [name, (new_x, new_y)]

            return new_x, new_y
        else:
            return x, y

    def someone_set_us_the_bomb(self, nr_player: int, direction: int) -> tuple:
        x = self.players[nr_player][1][0]
        y = self.players[nr_player][1][1]
        name = self.players[nr_player][0]
        self.bomb_maker(x, y)


    def print_position(self, x: int, y: int):
        print("Position (", x, ",", y, "):", self.world[(x, y)])

    def get_world(self):
        return self.world

    def get_bombs(self):
        return self.bombs

    def get_explosions(self):
        return self.explosions

    def print_world(self):
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                print("(", x, ",", y, ")=", self.world[(x, y)])


