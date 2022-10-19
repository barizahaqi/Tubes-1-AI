from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from LocalSearchNode import LocalSearchNode
import copy


class LocalSearchBot(Bot):
    """
    Bot untuk bermain dengan algoritma Local Search
    """

    def get_action(self, state: GameState) -> GameAction:
        """
        Menentukan aksi yang akan diambil bot berdasarkan state saat ini
        """
        action = self.hill_climbing_algorithm(state).action
        return action

    def hill_climbing_algorithm(self, state: GameState) -> GameState:
        """
        Algoritma Hill-Climbing
        """
        current = LocalSearchNode(state)
        while True:
            neighbor = self.get_neighbor(current)
            if neighbor is None:
                return current
            if neighbor.value < current.value:
                return current
            current = neighbor

    def get_neighbor(self, node: LocalSearchNode) -> LocalSearchNode:
        """
        Mendapatkan node tetangga sesuai tipe aksi
        """
        if (node.action is not None):
            if (node.action.action_type == "col") or (node.action.action_type == "row" and node.action.position[0] == 2 and node.action.position[1] == 3):
                return self.get_col_neighbor(node)
        return self.get_row_neighbor(node)

    def get_row_neighbor(self, node: LocalSearchNode) -> LocalSearchNode:
        """
        Mendapatkan node tetangga bertipe aksi row
        """
        if node.action is None:
            x = 0
            y = 0
        else:
            x = node.action.position[0] + 1
            y = node.action.position[1]
        found = False
        while y < 4:
            if x >= 3:
                x = 0
                y += 1
                continue
            if node.row_status[y][x] == 0:
                found = True
                break
            else:
                x += 1
        if found:
            return LocalSearchNode(copy.deepcopy(node.state), GameAction("row", (x, y)))
        else:
            return self.get_col_neighbor(node)

    def get_col_neighbor(self, node: LocalSearchNode) -> LocalSearchNode:
        """
        Mendapatkan node tetangga bertipe aksi col
        """
        if (node.action == None or node.action.action_type == "row"):
            x = 0
            y = 0
        else:
            x = node.action.position[0] + 1
            y = node.action.position[1]
        found = False
        while y < 3:
            if x >= 4:
                x = 0
                y += 1
                continue
            if node.col_status[y][x] == 0:
                found = True
                break
            else:
                x += 1
        if found:
            return LocalSearchNode(copy.deepcopy(node.state), GameAction("col", (x, y)))
        return None
