import random


class AlphaBetaNode:
    # class untuk node pohon alpha beta pruning
    def __init__(self):
        self.board = [None] * 24  # total 24 buah garis
        self.listMove = []  # move yang tersedia
        self.score = [0, 0] # score yang didapat dari banyaknya kotak yang dibuat. score[0] = lawan, score[1] = playerTurn

    def update(self, row, col):
        # menyesuaikan variabel listMove dan board dengan list move yang tersedia pada game yang sedang berlangsung
        j = 0
        for i in range(7):
            if i % 2 == 0:  # horizontal
                while (j < 3):
                    if (row[i//2][j] == 1):
                        self.board[i*4-i//2 + j] = True
                    else:
                        self.listMove.append((i, j))
                    j += 1
            else:  # vertical
                while (j < 4):
                    if (col[i//2][j] == 1):
                        self.board[i*4 - (i-1)//2 + j - 1] = True
                    else:
                        self.listMove.append((i, j))
                    j += 1
            j = 0
        random.shuffle(self.listMove)

    def move(self, playerTurn, x, y):
        # menambah poin dan mengembalikan true jika ada kotak yang terbentuk
        formed = False
        if x % 2 == 0:  # horizontal
            self.board[x*4-x//2 + y] = True
            if x < 6 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y+3] and self.board[x*4-x//2 + y + 4] and self.board[(x+2)*4-x//2 + y - 1]:
                # kotak bagian atas
                self.score[playerTurn] += 1
                formed = True
            if x > 0 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y-3] and self.board[x*4-x//2 + y - 4] and self.board[(x-2)*4-x//2 + y + 1]:
                # kotak bagian bawah
                self.score[playerTurn] += 1
                formed = True
        else:  # x%2==1, vertical
            self.board[x*4-(x-1)//2 + y - 1] = True
            if y < 3 and self.board[x*4 - (x-1)//2 + y - 1] and self.board[x*4-(x-1)//2 + y] and self.board[x*4-(x-1)//2 + y - 4] and self.board[(x+1)*4-(x-1)//2 + y - 1]:
                # kotak bagian kanan
                self.score[playerTurn] += 1
                formed = True
            if y > 0 and self.board[x*4 - (x-1)//2 + y - 2] and self.board[x*4-(x-1)//2 + y-1] and self.board[x*4-(x-1)//2 + y - 5] and self.board[(x+1)*4-(x-1)//2 + y - 2]:
                # kotak bagian kiri
                self.score[playerTurn] += 1
                formed = True
        self.listMove.remove((x, y))
        return formed

    def copy(self):
        # membuat copy dari objek sendiri
        newNode = AlphaBetaNode()
        newNode.board = self.board[:]
        newNode.listMove = self.listMove[:]
        newNode.score = self.score[:]
        return newNode
