import socket
import logging
import constante
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
        new_stuff_1, new_stuff_2 = self.gm_obj.someone_set_us_the_bomb(dados_pl)
        # Mandar as coordenadas
        s_c.send(new_stuff_1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
        s_c.send(new_stuff_2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

    def run(self):
        logging.info("a escutar no porto " + str(constante.PORTO))
        socket_client, endereco = self.s.accept()

        logging.info("o cliente com endereço " + str(endereco) + " ligou-se!")

        dados: str = ""
        fim = False
        while fim == False:
            # Recebe o comando
            dados_recebidos: bytes = socket_client.recv(constante.TAMANHO_MENSAGEM)
            dados = dados_recebidos.decode(constante.CODIFICACAO_STR)

            # Recebe o player
            dados_recebidos: bytes = socket_client.recv(constante.TAMANHO_MENSAGEM)
            dados_pl = dados_recebidos.decode(constante.CODIFICACAO_STR)
            if dados != "":
                logging.debug("o cliente enviou: \"" + dados + "\"")
                logging.debug("o cliente enviou: \"" + dados_pl + "\"")

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

        socket_client.close()
        logging.info("o cliente com endereço o " + str(endereco) + " desligou-se!")

        self.s.close()


logging.basicConfig(filename=constante.NOME_FICHEIRO_LOG,
                    level=constante.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')
