from GameAction import GameAction
from GameState import GameState
import random

class AlphaBetaNode:
    """
    Kelas untuk node pencarian Minimax alpha-beta pruning
    """

    def __init__(self, state: GameState, action: GameAction = None):
        """
        self.board: List[]
            list yang berisi 24 boolean yang menandakan apakah terdapat garis pada posisi tersebut

        self.listMove: List[]
            list yang berisi tuple yang menandakan semua posisi move yang tersedia

        self.score: List[]
            list yang berisi skor pemain. score[1] untuk pemain (playerTurn), score[0] untuk musuh
        """
        self.state = state
        self.row_status = state.row_status.copy()
        self.col_status = state.col_status.copy()
        self.board_status = state.board_status.copy()
        self.board = [None] * 24
        self.listMove = []
        self.score = [0, 0]

    def update(self):
        """
        Menyesuaikan variabel listMove dan board dengan list move yang tersedia pada game yang sedang berlangsung
        """
        j = 0
        for i in range(7):
            if i % 2 == 0:  # horizontal
                while (j < 3):
                    if not (self.row_status[i//2][j]):
                        self.listMove.append((i, j))
                    else:
                        self.board[i*4 - i//2 + j] = True
                    j += 1
            else:  # vertical
                while (j < 4):
                    if not (self.col_status[i//2][j]):
                        self.listMove.append((i, j))
                    else:
                        self.board[i*4 - (i-1)//2 + j - 1] = True
                    j += 1
            j = 0
        print(self.board)
        random.shuffle(self.listMove)

    def move(self, playerTurn: bool, x: int, y: int) -> bool:
        """
        Menambah skor pemain serta mengembalikan true jika ada kotak yang terbentuk
        """
        self.listMove.remove((x, y))
        if x % 2 == 0:  # horizontal
            self.board[x*4-x//2 + y] = True
            if x < 6 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y+3] and self.board[x*4-x//2 + y + 4] and self.board[(x+2)*4-x//2 + y - 1]:
                # kotak bagian atas
                self.score[playerTurn] += 1
                return True
            if x > 0 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y-3] and self.board[x*4-x//2 + y - 4] and self.board[(x-2)*4-x//2 + y + 1]:
                # kotak bagian bawah
                self.score[playerTurn] += 1
                return True
        else:  # x%2==1, vertical
            self.board[x*4-(x-1)//2 + y - 1] = True
            if y < 3 and self.board[x*4 - (x-1)//2 + y - 1] and self.board[x*4-(x-1)//2 + y] and self.board[x*4-(x-1)//2 + y - 4] and self.board[(x+1)*4-(x-1)//2 + y - 1]:
                # kotak bagian kanan
                self.score[playerTurn] += 1
                return True
            if y > 0 and self.board[x*4 - (x-1)//2 + y - 2] and self.board[x*4-(x-1)//2 + y-1] and self.board[x*4-(x-1)//2 + y - 5] and self.board[(x+1)*4-(x-1)//2 + y - 2]:
                # kotak bagian kiri
                self.score[playerTurn] += 1
                return True
        return False

    def copy(self):
        """
        Membuat copy dari objek sendiri
        """
        newNode = AlphaBetaNode(self.state)
        newNode.board = self.board[:]
        newNode.listMove = self.listMove[:]
        newNode.score = self.score[:]
        return newNode
