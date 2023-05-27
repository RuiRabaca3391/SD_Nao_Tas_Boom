import socket
import logging
import constante
import pygame
from typing import Union
from Server.game_mech import GameMech
from Server.client_management_session import ClientSession
# Está no lado do servidor: Skeleton to user interface (permite ter informação
# de como comunicar com o cliente)

# AJUDAS
        # -- int.from_bytes(dados_recebidos, byteorder='big', signed=True)
        # -- to_bytes(constante.N_BYTES, byteorder="big", signed=True)

class SkeletonServer:

    def __init__(self, gm: GameMech):
        self.gm = gm
        self.s = socket.socket()
        self.s.bind((constante.ENDERECO_SERVIDOR, constante.PORTO))
        self.s.listen()
        self.clock = pygame.time.Clock()

        #------------------------------------------
        # Added timeout
        self.s.settimeout(constante.ACCEPT_TIMEOUT)
        #------------------------------------------
        self.keep_running = True

    def accept(self) -> Union['Socket', None]:
        """
        A new definition of accept() to provide a return if a timeout occurs.
        """
        try:
            client_connection, address = self.s.accept()
            logging.info("o cliente com endereço " + str(address) + " ligou-se!")

            return client_connection
        except socket.timeout:
            return None

    def run(self):
        logging.info("a escutar no porto " + str(constante.PORTO))
        while self.keep_running:
            socket_client = self.accept()
            if socket_client is not None:
                # Add client
                # self._state.add_client(socket_client)
                ClientSession(socket_client, self.gm).start()

        self.s.close()


logging.basicConfig(filename=constante.NOME_FICHEIRO_LOG,
                    level=constante.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')
