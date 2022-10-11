from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import numpy as np


class DotsAndBoxes:
    #class untuk membuat game Dots and Boxes yang dimainkan secara otomatis untuk alpha beta pruning
    def __init__(self):
        self.board = [None] * 24 # total 24 buah garis
        self.listMove = self.makeMove() #move yang tersedia
        self.skor = [0, 0] # skor yang didapat dari banyaknya kotak yang dibuat. skor[0] = lawan, skor[1] = player

    def makeMove(self):
        #membuat list move yang tersedia
        moves, j = [], 0
        for i in range(7):
            if i%2==0: #horizontal
                while (j<3):
                    moves.append((i, j))
                    j+=1
            else:
                while (j<4):
                    moves.append((i, j))
                    j+=1
            j=0
        return moves

    def updateMove(self, row, col):
        #menyesuaikan variabel listMove dan board dengan list move yang tersedia pada game yang sedang berlangsung
        j=0
        for i in range(7):
            if i%2==0: #horizontal
                while (j<3):
                    if (row[i//2][j] == 1):
                        self.listMove.remove((i, j))
                        self.board[i*4-i//2 + j] = True
                    j+=1
            else:
                while (j<4):
                    if (col[i//2][j] == 1):
                        self.listMove.remove((i, j))
                        self.board[i*4 -(i-1)//2 + j - 1] = True
                    j+=1
            j=0
    
    def markedBox(self, x, y, player): 
        #mmenambah poin dan mengembalikan true jika ada kotak yang terbentuk
        marked = False
        if x % 2 == 0: # horizontal
            if x<6 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y+3] and self.board[x*4-x//2 + y + 4] and self.board[(x+2)*4-x//2+ y -1]:
                marked = True
                self.skor[player] += 1
            if x>0 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y-3] and self.board[x*4-x//2 + y - 4] and self.board[(x-2)*4-x//2+ y +1]:
                marked = True
                self.skor[player] += 1
        else: #x%2==1, vertical
            if y<3 and self.board[x*4 -(x-1)//2 + y -1] and self.board[x*4-(x-1)//2 + y] and self.board[x*4-(x-1)//2 + y - 4] and self.board[(x+1)*4-(x-1)//2+ y -1]:
                marked = True
                self.skor[player] += 1
            if y>0 and self.board[x*4 -(x-1)//2 + y -2] and self.board[x*4-(x-1)//2 + y-1] and self.board[x*4-(x-1)//2 + y - 5] and self.board[(x+1)*4-(x-1)//2+ y -2]:
                marked = True
                self.skor[player] += 1
        return marked

    def move(self, x, y, player):
        #mengisi board dan menghapus move pada listMove
        if x % 2 == 0:
            self.board[x*4-x//2 + y] = True
        else:
            self.board[x*4-(x-1)//2 + y -1] = True
        self.listMove.remove((x, y))
        turn = self.markedBox(x, y, player) #jika true, player akan mendapatkan gilirannya lagi
        return turn

    def copy(self):
        #membuat copy dari objek sendiri
        dab = DotsAndBoxes()
        dab.board = self.board[:]
        dab.listMove = self.listMove[:]
        dab.skor = self.skor[:]
        return dab

class newBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        #GameAction yang akan dikirimkan ke permainan
        row_status = state.row_status
        col_status = state.col_status
        dab=DotsAndBoxes()
        dab.updateMove(row_status, col_status)
        move = self.alphaBetaAlgorithm(dab)[0]
        if move[0]%2==0:
            return GameAction('row', [move[1], move[0]//2])
        else:
            return GameAction('col', [move[1], move[0]//2])

    def alphaBetaAlgorithm(self, node, depth = 6, alpha = -10, beta = 10, isMax = True, playerTurn = True, move = (0,0)):
        #algoritma alpha beta pruning
        if len(node.listMove) == 0 or depth == 0:
            return [move, node.skor[playerTurn] - node.skor[not playerTurn]] # base case
        else:
            if isMax:
                bestMove =  ()
                bestScore = -10
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
                worstMove = ()
                worstScore = 10
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
