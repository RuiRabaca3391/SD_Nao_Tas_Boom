from threading import Thread
from game_mech import GameMech
import constante
import logging
import pygame

# shr: shared.SharedServerState,

class ClientSession(Thread):
    """Maintains a session with the client"""

    def __init__(self, socket_client: int,  game_mech: GameMech, player_list: list):
        """
        Constructs a thread to hold a session with the client
        :param shared_state: The server's state shared by threads
        :param client_socket: The client's socket
        """
        Thread.__init__(self)
        # self._shared = shr
        self.socket_client = socket_client
        self.gm_obj = game_mech
        self.clock = pygame.time.Clock()
        self.player_list = player_list

    def processa_movimento_up(self,s_c,  dados_pl):

        # Meter depois o nome do jogador
        new_stuff_1, new_stuff_2 = self.gm_obj.go_up(dados_pl)
        # Mandar as coordenadas
        s_c.send(new_stuff_1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        s_c.send(new_stuff_2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def processa_movimento_down(self, s_c, dados_pl):
        # Meter depois o nome do jogador
        new_stuff_1, new_stuff_2 = self.gm_obj.go_down(dados_pl)
        #new_stuff_1 = str(new_stuff_1)
        print("hello",new_stuff_1)
        #new_stuff_2 = str(new_stuff_2)
        # Mandar as coordenadas
        s_c.send(new_stuff_1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        s_c.send(new_stuff_2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def processa_movimento_right(self, s_c,  dados_pl):

        # Meter depois o nome do jogador
        new_stuff_1, new_stuff_2 = self.gm_obj.go_right(dados_pl)
        # Mandar as coordenadas
        s_c.send(new_stuff_1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        s_c.send(new_stuff_2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def processa_movimento_left(self, s_c,  dados_pl):

        # Meter depois o nome do jogador
        new_stuff_1, new_stuff_2 = self.gm_obj.go_left(dados_pl)
        # Mandar as coordenadas
        s_c.send(new_stuff_1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        s_c.send(new_stuff_2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def processa_movimento_bomb(self, s_c,  dados_pl):

        # Meter depois o nome do jogador
        self.gm_obj.bomb_maker(dados_pl)

    def collect_and_send_progress(self, s_c, nr_player):

        lst_b = []
        lst_e = []

        # Para as bombas
        for x in range(0, self.gm_obj.x_max - 1):
            for y in range(0, self.gm_obj.y_max - 1):
                if self.gm_obj.world[(x, y)] != [] and self.gm_obj.world[(x, y)][0][1] == "bomb":
                    lst_b.append(x)
                    lst_b.append(y)

        size = len(lst_b)
        s_c.send(size.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        if size != 0:
            lst = self.gm_obj.collect_bombs()
            for i in lst:
                s_c.send(i.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

        # Para as explosões
        for x in range(0, self.gm_obj.x_max - 1):
            for y in range(0, self.gm_obj.y_max - 1):
                if self.gm_obj.world[(x, y)] != [] and self.gm_obj.world[(x, y)][0][1] == "explosion":
                    print("I Exist")
                    lst_e.append(x)
                    lst_e.append(y)

        size = len(lst_e)
        s_c.send(size.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        if size != 0:
            lst = self.gm_obj.collect_explosions()
            print("Lista exp : ", lst)
            for i in lst:
                s_c.send(i.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

        x, y = self.gm_obj.collect_player_adv(nr_player)
        s_c.send(x.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        s_c.send(y.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

        return lst_b, lst_e

    def collect_and_send_player(self, s_c):

        i = len(self.player_list)
        s_c.send(i.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def dispatch_request(self, socket_client) -> bool:
        """
        :return:
        """
        lr = False
        # Recebe o comando
        dados_recebidos: bytes = socket_client.recv(constante.TAMANHO_MENSAGEM)
        dados = dados_recebidos.decode(constante.CODIFICACAO_STR)

        # Recebe o player
        dados_recebidos: bytes = socket_client.recv(constante.TAMANHO_MENSAGEM)
        dados_pl = dados_recebidos.decode(constante.CODIFICACAO_STR)

        if dados != "":
            logging.debug("o cliente enviou: \"" + dados + "\"")
            logging.debug("o cliente enviou: \"" + dados_pl + "\"")

        if dados == constante.SHOW_PROGRESSION:
            self.collect_and_send_progress(socket_client, dados_pl)

        if dados == constante.GET_PLAYER:
            self.collect_and_send_player(socket_client)

        if dados == constante.CIMA:
            self.processa_movimento_up(socket_client, dados_pl)

        if dados == constante.BAIXO:
            self.processa_movimento_down(socket_client, dados_pl)

        if dados == constante.ESQUERDA:
            self.processa_movimento_left(socket_client, dados_pl)

        if dados == constante.DIREITA:
            self.processa_movimento_right(socket_client, dados_pl)

        if dados == constante.ESPACO:

            self.processa_movimento_bomb(socket_client, dados_pl)

        elif dados == constante.FIM:
            lr = True

        return lr

    def run(self):
        """Maintains a session with the client, following the established protocol"""
        #logging.debug("Client " + str(client.peer_addr) + " just connected")
        last_request = False
        while not last_request:
            dt = self.clock.tick(10)
            last_request = self.dispatch_request(self.socket_client)
            self.gm_obj.bomb_ticking(dt)
            self.gm_obj.explosion_ticking(dt)
        logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")
        # Sared stuff (TODO)
        #self._shared_state.remove_client(self._client_connection)
        #self._shared_state.concurrent_clients.release()