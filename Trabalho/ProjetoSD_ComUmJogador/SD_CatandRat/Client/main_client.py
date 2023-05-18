from Client.ui import Game
from Client.client_stub import StubClient

def main():
    stub = StubClient()
    gm = Game(15, 13, 65)
    gm.run(stub)


main()