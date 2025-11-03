from enum import nonmember

from app.controller.game_controller import GameController

if __name__ == "__main__":
    controller = GameController()
    controller.start_game()