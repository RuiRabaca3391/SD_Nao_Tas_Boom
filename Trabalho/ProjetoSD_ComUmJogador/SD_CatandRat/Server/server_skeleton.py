import socket
import logging
import constante
import pygame
from Server.game_mech import GameMech
# Está no lado do servidor: Skeleton to user interface (permite ter informação
# de como comunicar com o cliente)

# AJUDAS
        # -- int.from_bytes(dados_recebidos, byteorder='big', signed=True)
        # -- to_bytes(constante.N_BYTES, byteorder="big", signed=True)

class SkeletonServer:

    def __init__(self, gm: GameMech):
        self.gm_obj = gm
        self.s = socket.socket()
        self.s.bind((constante.ENDERECO_SERVIDOR, constante.PORTO))
        self.s.listen()
        self.clock = pygame.time.Clock()
        self.player_list = []

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

    def collect_and_send_progress(self, s_c):

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

        return lst_b, lst_e

    def collect_and_send_player(self, s_c):
        self.player_list.append("player")
        i = len(self.player_list)
        s_c.send(i.to_bytes(constante.N_BYTES, byteorder="big", signed=True))


    def run(self):
        logging.info("a escutar no porto " + str(constante.PORTO))
        socket_client, endereco = self.s.accept()

        logging.info("o cliente com endereço " + str(endereco) + " ligou-se!")

        dados: str = ""
        fim = False
        while fim == False:
            dt = self.clock.tick(10)
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

                self.collect_and_send_progress(socket_client)

            if dados == constante.GET_PLAYER:

                self.collect_and_send_player(socket_client)

            if dados == constante.CIMA:

                self.processa_movimento_up(socket_client,  dados_pl)

            if dados == constante.BAIXO:

                self.processa_movimento_down(socket_client,  dados_pl)

            if dados == constante.ESQUERDA:

                self.processa_movimento_left(socket_client,  dados_pl)

            if dados == constante.DIREITA:

                self.processa_movimento_right(socket_client,  dados_pl)

            if dados == constante.ESPACO:

                self.processa_movimento_bomb(socket_client,  dados_pl)

            elif dados == constante.FIM:
                fim = True
#            if dados != constante.FIM:
#                dados = self.eco_obj.eco(dados)
#                socket_client.send(dados.encode(constante.CODIFICACAO_STR))

            self.gm_obj.bomb_ticking(dt)
            self.gm_obj.explosion_ticking(dt)

        socket_client.close()
        logging.info("o cliente com endereço o " + str(endereco) + " desligou-se!")

        self.s.close()


logging.basicConfig(filename=constante.NOME_FICHEIRO_LOG,
                    level=constante.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')
