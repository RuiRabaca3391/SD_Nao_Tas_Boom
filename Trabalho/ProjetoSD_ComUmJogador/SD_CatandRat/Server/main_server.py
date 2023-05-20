from Server.game_mech import GameMech
from Server.server_skeleton import SkeletonServer


def main():
    gm = GameMech(15, 13)
    gm.print_world()
    gm.print_position(1, 1)
    gm.print_position(0, 1)
    ui = SkeletonServer(gm)
    ui.run()


main()