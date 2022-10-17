from Bot import Bot
from AlphaBetaNode import AlphaBetaNode
from GameAction import GameAction
from GameState import GameState
import numpy as np


class AlphaBetaBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        """
        menentukan aksi yang akan diambil bot
        """
        node = AlphaBetaNode()
        node.update(state.row_status, state.col_status)
        countRowAndColNotMarked = 24 - \
            np.count_nonzero(state.row_status == 1) - \
            np.count_nonzero(state.col_status == 1)
        maxNode, depth = 1, 0
        # batasi maxNode yang dibuat sampai 4037880
        while (maxNode < 4037880 and countRowAndColNotMarked > 0):
            maxNode *= countRowAndColNotMarked
            depth += 1
            countRowAndColNotMarked -= 1
        moveResult = self.alphaBetaAlgorithm(
            node, True, depth, (0, 0), -10, 10)[0]
        if moveResult[0] % 2 == 0:
            return GameAction('row', [moveResult[1], moveResult[0]//2])
        else:
            return GameAction('col', [moveResult[1], moveResult[0]//2])

    def alphaBetaAlgorithm(self, node, playerTurn, depth, move, alpha, beta):
        """
        algoritma alpha beta pruning
        """
        if depth == 0 or len(node.listMove) == 0:
            return [move, node.score[True] - node.score[False]]
        else:
            move = ()
            if playerTurn:  # jika true akan mencari nilai maksimum
                bestScore = -9
                for x, y in node.listMove:
                    currentNode = node.copy()  # buat node baru untuk ditelusuri
                    turn = currentNode.move(playerTurn, x, y)
                    result = self.alphaBetaAlgorithm(
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
                    result = self.alphaBetaAlgorithm(
                        currentNode, not turn, depth - 1, (x, y), alpha, beta)
                    if result[1] < worstScore:
                        worstScore = result[1]
                        move = (x, y)
                    beta = min(beta, worstScore)
                    if beta <= alpha:
                        break
                return [move, worstScore]
