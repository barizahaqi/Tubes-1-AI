class DotsAndBoxes:
    #class untuk membuat game Dots and Boxes yang dimainkan secara otomatis untuk pohon algoritma
    def __init__(self):
        self.board = [None] * 24 # total 24 buah garis
        self.listMove = self.makeMove() #move yang tersedia
        self.skor = [0, 0] # skor yang didapat dari banyaknya kotak yang dibuat. skor[0] = lawan, skor[1] = player

    def makeMove(self):
        #membuat list move board 4x4
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
    
    def formedBox(self, x, y, player): 
        #mmenambah poin dan mengembalikan true jika ada kotak yang terbentuk
        formed = False
        if x % 2 == 0: # horizontal
            if x<6 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y+3] and self.board[x*4-x//2 + y + 4] and self.board[(x+2)*4-x//2+ y -1]:
                formed = True
                self.skor[player] += 1
            if x>0 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y-3] and self.board[x*4-x//2 + y - 4] and self.board[(x-2)*4-x//2+ y +1]:
                formed = True
                self.skor[player] += 1
        else: #x%2==1, vertical
            if y<3 and self.board[x*4 -(x-1)//2 + y -1] and self.board[x*4-(x-1)//2 + y] and self.board[x*4-(x-1)//2 + y - 4] and self.board[(x+1)*4-(x-1)//2+ y -1]:
                formed = True
                self.skor[player] += 1
            if y>0 and self.board[x*4 -(x-1)//2 + y -2] and self.board[x*4-(x-1)//2 + y-1] and self.board[x*4-(x-1)//2 + y - 5] and self.board[(x+1)*4-(x-1)//2+ y -2]:
                formed = True
                self.skor[player] += 1
        return formed

    def move(self, x, y, player):
        #mengisi board dan menghapus move pada listMove
        if x % 2 == 0:
            self.board[x*4-x//2 + y] = True
        else:
            self.board[x*4-(x-1)//2 + y -1] = True
        self.listMove.remove((x, y))
        turn = self.formedBox(x, y, player) #jika true, player akan mendapatkan gilirannya lagi
        return turn

    def copy(self):
        #membuat copy dari objek sendiri
        dab = DotsAndBoxes()
        dab.board = self.board[:]
        dab.listMove = self.listMove[:]
        dab.skor = self.skor[:]
        return dab