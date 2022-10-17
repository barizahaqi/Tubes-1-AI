from GameAction import GameAction
from GameState import GameState
import numpy as np


class LocalSearchNode:
    """
    Node untuk pencarian dengan Local Search
    """

    def __init__(self, state: GameState, action: GameAction = None):
        self.state = state
        self.action = action
        self.value = -2
        self.board_status = state.board_status.copy()
        self.row_status = state.row_status.copy()
        self.col_status = state.col_status.copy()
        self.current_box = self.countBox()
        if action is not None:
            self.update(action)

    def update(self, action: GameAction):
        x = action.position[0]
        y = action.position[1]
        number_of_dots = 4

        if y < (number_of_dots-1) and x < (number_of_dots-1):
            self.board_status[y][x] = (abs(self.board_status[y][x]) + 1)

        if action.action_type == 'row':
            self.row_status[y][x] = 1
            if y >= 1:
                self.board_status[y -
                                  1][x] = (abs(self.board_status[y-1][x]) + 1)

        elif action.action_type == 'col':
            self.col_status[y][x] = 1
            if x >= 1:
                self.board_status[y][x -
                                     1] = (abs(self.board_status[y][x-1]) + 1)
        self.value = self.calculateValue()

    def countBox(self):
        """
        Menghitung jumlah kotak yang terbentuk
        """

        return np.count_nonzero(abs(self.board_status) == 4)

    def calculateValue(self):
        """
        Menghitung nilai dari node
        """

        if (self.countBox() - self.current_box) > 0:
            return 1
        if (np.any(self.board_status == 3)):
            return -1
        return 0
