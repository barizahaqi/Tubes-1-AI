from Bot import Bot
from DotsAndBoxes import DotsAndBoxes
from GameAction import GameAction
from GameState import GameState
import numpy as np

class newBot(Bot):
    def alphaBetaAlgorithm(self, node, depth, alpha, beta, isMax, playerTurn, move):
        #algoritma alpha beta pruning
        if len(node.listMove) == 0 or depth == 0:
            return [move, node.skor[playerTurn] - node.skor[not playerTurn]] # base case
        else:
            if isMax:
                bestScore = -10
                bestMove =  ()
                for x, y in node.listMove:
                    currentNode = node.copy() #buat node baru untuk ditelusuri
                    turn = currentNode.move(x, y, playerTurn)
                    result = self.alphaBetaAlgorithm(currentNode, depth - 1, alpha, beta, turn, playerTurn, (x, y))
                    if result[1] > bestScore:
                        bestMove = (x, y)
                        bestScore = result[1]
                    alpha = max(bestScore, alpha)
                    if beta <= alpha:
                        break
                return [bestMove, bestScore]
            else:
                worstScore = 10
                worstMove = ()
                for x, y in node.listMove:
                    currentNode = node.copy()
                    turn = currentNode.move(x, y, not playerTurn)
                    result = self.alphaBetaAlgorithm(currentNode, depth - 1, alpha, beta, not turn, playerTurn, (x, y))
                    if result[1] < worstScore:
                        worstMove = (x, y)
                        worstScore = result[1]
                    beta = min(beta, worstScore)
                    if beta <= alpha:
                        break
                return [worstMove, worstScore]

    def get_action(self, state: GameState) -> GameAction:
        #GameAction yang akan dikirimkan ke permainan
        row_status = state.row_status
        col_status = state.col_status
        dab=DotsAndBoxes()
        dab.updateMove(row_status, col_status)
        move = self.alphaBetaAlgorithm(dab,6,-10,10,True,True,(0,0))[0]
        if move[0]%2==0:
            return GameAction('row', [move[1], move[0]//2])
        else:
            return GameAction('col', [move[1], move[0]//2])

    
