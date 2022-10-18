from Bot import Bot
from AlphaBetaNode import AlphaBetaNode
from GameAction import GameAction
from GameState import GameState
import numpy as np
import time


class AlphaBetaBot(Bot):
    """
    Bot untuk bermain dengan algoritma Minimax alpha-beta pruning
    """
    global start_time

    def get_action(self, state: GameState) -> GameAction:
        """
        Menentukan aksi yang akan diambil bot berdasarkan state saat ini
        """
        global start_time
        node = AlphaBetaNode()
        node.update(state.row_status, state.col_status)
        countRowAndColNotMarked = 24 - \
            np.count_nonzero(state.row_status == 1) - \
            np.count_nonzero(state.col_status == 1)
        maxNode, depth = 1, 0
        while (True):
            maxNode *= countRowAndColNotMarked
            depth += 1
            countRowAndColNotMarked -= 1
            if (maxNode > 4000000 or countRowAndColNotMarked < 0):
                depth -= 1
                break
        start_time = time.time()
        moveResult = self.minimax_alpha_beta_algorithm(
            node, True, depth, (0, 0), -10, 10)[0]
        if moveResult[0] % 2 == 0:
            return GameAction('row', [moveResult[1], moveResult[0]//2])
        else:
            return GameAction('col', [moveResult[1], moveResult[0]//2])

    def minimax_alpha_beta_algorithm(self, node: AlphaBetaNode, playerTurn: bool, depth: int, move: (int, int), alpha: int, beta: int) -> (int, int):
        """
        Algoritma Minimax dengan alpha-beta pruning
        """
        global start_time
        end_time = time.time() - start_time
        if depth == 0 or len(node.listMove) == 0 or end_time > 4.5:
            return [move, node.score[True] - node.score[False]]
        else:
            move = ()
            if playerTurn:  # jika true akan mencari nilai maksimum
                bestScore = -9
                for x, y in node.listMove:
                    currentNode = node.copy()
                    turn = currentNode.move(playerTurn, x, y)
                    result = self.minimax_alpha_beta_algorithm(
                        currentNode, turn, depth - 1, (x, y), alpha, beta)
                    if result[1] > bestScore:
                        bestScore = result[1]
                        move = (x, y)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
                return [move, bestScore]
            else:  # false akan mencari nilai minimum
                worstScore = 9
                for x, y in node.listMove:
                    currentNode = node.copy()
                    turn = currentNode.move(playerTurn, x, y)
                    result = self.minimax_alpha_beta_algorithm(
                        currentNode, not turn, depth - 1, (x, y), alpha, beta)
                    if result[1] < worstScore:
                        worstScore = result[1]
                        move = (x, y)
                    beta = min(beta, worstScore)
                    if beta <= alpha:
                        break
                return [move, worstScore]
