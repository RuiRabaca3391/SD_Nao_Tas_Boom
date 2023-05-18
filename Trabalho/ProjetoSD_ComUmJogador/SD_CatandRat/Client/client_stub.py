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

        lst = []
        dados_recebidos_1: bytes = self.s.recv(constante.N_BYTES)
        dados_recebidos_2: bytes = self.s.recv(constante.N_BYTES)

        lst.append(int.from_bytes(dados_recebidos_1, byteorder='big', signed=True))
        lst.append(int.from_bytes(dados_recebidos_2, byteorder='big', signed=True))
        print(lst)

        return lst


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


    def espaco(self, nr_player: str) -> Union[int, None]:

        msg = constante.ESPACO
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        # Manda o numero do jogador
        msg = nr_player
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        dados_recebidos: bytes = self.s.recv(constante.N_BYTES)
        return int.from_bytes(dados_recebidos, byteorder='big', signed=True)

