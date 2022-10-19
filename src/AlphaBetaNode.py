from GameAction import GameAction
from GameState import GameState
import random

class AlphaBetaNode:
    """
    Kelas untuk node pencarian Minimax alpha-beta pruning
    """

    def __init__(self, state: GameState, action: GameAction = None):
        """
        self.listMove: List[]
            list yang berisi tuple yang menandakan semua posisi move yang tersedia

        self.score: List[]
            list yang berisi skor pemain. score[1] untuk pemain (playerTurn), score[0] untuk musuh
        """
        self.state = state
        self.row_status = state.row_status.copy()
        self.col_status = state.col_status.copy()
        self.listMove = []
        self.score = [0, 0]

    def createListMove(self):
        """
        Menyesuaikan variabel listMove dengan list move yang tersedia pada game yang sedang berlangsung
        """
        j = 0
        for i in range(7):
            if i % 2 == 0:  # horizontal
                for j in range(3):
                    if not (self.row_status[i//2][j]):
                        self.listMove.append((i, j))
            else:  # vertical
                for j in range(4):
                    if not (self.col_status[i//2][j]):
                        self.listMove.append((i, j))
                    j += 1
            j = 0
        random.shuffle(self.listMove)

    def move(self, playerTurn: bool, y: int, x: int) -> bool:
        """
        Menambah skor pemain serta mengembalikan true jika ada kotak yang terbentuk
        """
        self.listMove.remove((y, x))
        if y % 2 == 0:  # horizontal
            self.row_status[y//2][x] = True
            if y < 6 and self.row_status[(y+2)//2][x] and self.col_status[(y//2)][x] and self.col_status[(y//2)][x+1]:
                # kotak bagian atas
                self.score[playerTurn] += 1
                return True
            if y > 0 and self.col_status[((y-2)//2)][x+1] and self.col_status[((y-2)//2)][x] and self.row_status[(y-2)//2][x]:
                # kotak bagian bawah
                self.score[playerTurn] += 1
                return True
        else:  # x%2==1, vertical
            self.col_status[y//2][x] = True
            if x < 3 and self.col_status[y//2][x+1] and self.row_status[y//2][x] and self.row_status[(y+2)//2][x]:
                # kotak bagian kanan
                self.score[playerTurn] += 1
                return True
            if x > 0 and self.col_status[y//2][x-1] and self.row_status[y//2][x-1] and self.row_status[(y+2)//2][x-1]:
                # kotak bagian kiri
                self.score[playerTurn] += 1
                return True
        return False

    def copy(self):
        """
        Membuat copy dari objek sendiri
        """
        newNode = AlphaBetaNode(self.state)
        newNode.state = self.state
        newNode.row_status = self.row_status.copy()
        newNode.col_status = self.col_status.copy()
        newNode.listMove = self.listMove[:]
        newNode.score = self.score[:]
        return newNode
