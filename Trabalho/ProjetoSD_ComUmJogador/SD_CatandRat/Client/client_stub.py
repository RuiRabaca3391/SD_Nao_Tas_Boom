import socket
from typing import Union

import constante
#self.s.send(value1.to_bytes(constante.N_BYTES, byteorder="big", signed=True))
#self.s.send(value2.to_bytes(constante.N_BYTES, byteorder="big", signed=True))

#if msg != constante.FIM:
        #    dados_recebidos: bytes = self.s.recv(constante.TAMANHO_MENSAGEM)
        #    return dados_recebidos.decode(constante.CODIFICACAO_STR)
        #else:
        #    self.s.close()

# Stub do lado do cliente: como comunicar com o servidor...

class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constante.ENDERECO_SERVIDOR, constante.PORTO))

    def cima(self, nr_player: str) -> Union[int, None]:

        msg = constante.CIMA
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        lst = []
        dados_recebidos_1: bytes = self.s.recv(constante.N_BYTES)
        dados_recebidos_2: bytes = self.s.recv(constante.N_BYTES)

        lst.append(int.from_bytes(dados_recebidos_1, byteorder='big', signed=True))
        lst.append(int.from_bytes(dados_recebidos_2, byteorder='big', signed=True))
        print(lst)

        return lst


    def baixo(self, nr_player: str) -> Union[int, None]:
        print("Inicio baixo stub")
        msg = constante.BAIXO
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))
        print("Meio Baixo Stub")
        lst = []
        dados_recebidos_1: bytes = self.s.recv(constante.N_BYTES)
        dados_recebidos_2: bytes = self.s.recv(constante.N_BYTES)
        print("Mensagem recebidas stub")
        print("X : ", int.from_bytes(dados_recebidos_1, byteorder='big', signed=True))
        print("Y : ", int.from_bytes(dados_recebidos_2, byteorder='big', signed=True))

        lst.append(int.from_bytes(dados_recebidos_1, byteorder='big', signed=True))
        lst.append(int.from_bytes(dados_recebidos_2, byteorder='big', signed=True))
        print(lst)

        return lst

    def get_me(self):
        msg = constante.GET_PLAYER
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        msg = "fake"
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        dados_recebidos_1: bytes = self.s.recv(constante.N_BYTES)
        i = int.from_bytes(dados_recebidos_1, byteorder='big', signed=True)
        if i == 1:
            ret = "p1"
        elif i == 2 :
            ret = "p2"

        return ret

    def esquerda(self, nr_player: str) -> Union[int, None]:

        msg = constante.ESQUERDA
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        lst = []
        dados_recebidos_1: bytes = self.s.recv(constante.N_BYTES)
        dados_recebidos_2: bytes = self.s.recv(constante.N_BYTES)

        lst.append(int.from_bytes(dados_recebidos_1, byteorder='big', signed=True))
        lst.append(int.from_bytes(dados_recebidos_2, byteorder='big', signed=True))
        print(lst)

        return lst


    def direita(self, nr_player: str) -> Union[int, None]:

        msg = constante.DIREITA
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        lst = []
        dados_recebidos_1: bytes = self.s.recv(constante.N_BYTES)
        dados_recebidos_2: bytes = self.s.recv(constante.N_BYTES)

        lst.append(int.from_bytes(dados_recebidos_1, byteorder='big', signed=True))
        lst.append(int.from_bytes(dados_recebidos_2, byteorder='big', signed=True))
        print(lst)

        return lst


    def espaco(self, nr_player: str):

        msg = constante.ESPACO
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

    def show_progression_client(self, nr_player: str):

        msg = constante.SHOW_PROGRESSION
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        lst_b = []
        lst_e = []
        lst_p = []

        # Recebe o tamanho bombas
        dados_recebidos_size: bytes = self.s.recv(constante.N_BYTES)
        size_b = int.from_bytes(dados_recebidos_size, byteorder='big', signed=True)
        print(size_b)
        if size_b != 0:
            lst_b = []
            for i in range(size_b):
                dados_recebidos_coords: bytes = self.s.recv(constante.N_BYTES)
                lst_b.append(int.from_bytes(dados_recebidos_coords, byteorder='big', signed=True))
            print("Server gettting : ", lst_b)

        # Recebe o tamanho das explosões
        dados_recebidos_size: bytes = self.s.recv(constante.N_BYTES)
        size_e = int.from_bytes(dados_recebidos_size, byteorder='big', signed=True)
        print(size_e)
        if size_e != 0:
            lst_e = []
            for i in range(size_e):
                dados_recebidos_coords: bytes = self.s.recv(constante.N_BYTES)
                lst_e.append(int.from_bytes(dados_recebidos_coords, byteorder='big', signed=True))
            print("Server gettting : ", lst_e)

        # Coordenadas do player adversário
        dados_recebidos_coords_1: bytes = self.s.recv(constante.N_BYTES)
        lst_p.append(int.from_bytes(dados_recebidos_coords_1, byteorder='big', signed=True))

        dados_recebidos_coords_2: bytes = self.s.recv(constante.N_BYTES)
        lst_p.append(int.from_bytes(dados_recebidos_coords_2, byteorder='big', signed=True))
        print("Server gettting : ", lst_p)

        return lst_b, lst_e, lst_p

    def show_explosions_client(self):

        msg = constante.SHOW_EXPLOSIONS
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = "fake"
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        lst = []

        # Recebe o tamanho
        dados_recebidos_size: bytes = self.s.recv(constante.N_BYTES)
        size = int.from_bytes(dados_recebidos_size, byteorder='big', signed=True)
        print(size)
        if size != 0:
            lst = []
            for i in range(size):
                dados_recebidos_coords: bytes = self.s.recv(constante.N_BYTES)
                lst.append(int.from_bytes(dados_recebidos_coords, byteorder='big', signed=True))
            print("Server gettting : ", lst)
        return lst