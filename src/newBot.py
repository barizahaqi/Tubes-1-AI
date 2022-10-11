from Bot import Bot
from DotsAndBoxes import DotsAndBoxes
from GameAction import GameAction
from GameState import GameState
import numpy as np

class newBot(Bot):
    def alphaBetaAlgorithm(self, node, playerTurn, isMax, depth, move, alpha, beta):
        #algoritma alpha beta pruning
        if len(node.listMove) == 0 or depth == 0:
            return [move, node.skor[playerTurn] - node.skor[not playerTurn]] # base case
        else:
            if isMax:
                bestScore = -10
                bestMove =  ()
                for x, y in node.listMove:
                    currentNode = node.copy() #buat node baru untuk ditelusuri
                    turn = currentNode.move(playerTurn, x, y)
                    result = self.alphaBetaAlgorithm(currentNode, playerTurn, turn, depth - 1, (x, y), alpha, beta)
                    if result[1] > bestScore:
                        bestScore = result[1]
                        bestMove = (x, y)
                    alpha = max(bestScore, alpha)
                    if beta <= alpha:
                        break
                return [bestMove, bestScore]
            else:
                worstScore = 10
                worstMove = ()
                for x, y in node.listMove:
                    currentNode = node.copy()
                    turn = currentNode.move(not playerTurn, x, y)
                    result = self.alphaBetaAlgorithm(currentNode, playerTurn, not turn, depth - 1, (x, y), alpha, beta)
                    if result[1] < worstScore:
                        worstScore = result[1]
                        worstMove = (x, y)
                    beta = min(beta, worstScore)
                    if beta <= alpha:
                        break
                return [worstMove, worstScore]

    def get_action(self, state: GameState) -> GameAction:
        #GameAction yang akan dikirimkan ke permainan
        row_status = state.row_status
        col_status = state.col_status
        node=DotsAndBoxes()
        node.updateMove(row_status, col_status)
        moveResult = self.alphaBetaAlgorithm(node,True,True, 6,(0,0),-10,10)[0]
        if moveResult[0]%2==0:
            return GameAction('row', [moveResult[1], moveResult[0]//2])
        else:
            return GameAction('col', [moveResult[1], moveResult[0]//2])

    
