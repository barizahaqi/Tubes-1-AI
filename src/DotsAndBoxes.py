class DotsAndBoxes:
    #class untuk membuat game Dots and Boxes yang dimainkan secara otomatis untuk pohon algoritma
    def __init__(self):
        self.board = [None] * 24 # total 24 buah garis
        self.listMove = self.makeMove() #move yang tersedia
        self.skor = [0, 0] # skor yang didapat dari banyaknya kotak yang dibuat. skor[0] = lawan, skor[1] = playerTurn

    def makeMove(self):
        #membuat list move board 4x4
        listMove, j = [], 0
        for i in range(7):
            if i%2==0: #horizontal
                while (j<3):
                    listMove.append((i, j))
                    j+=1
            else: #vertical
                while (j<4):
                    listMove.append((i, j))
                    j+=1
            j=0
        return listMove

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
            else: #vertical
                while (j<4):
                    if (col[i//2][j] == 1):
                        self.listMove.remove((i, j))
                        self.board[i*4 -(i-1)//2 + j - 1] = True
                    j+=1
            j=0
    
    def formedBox(self, playerTurn, x, y): 
        #menambah poin dan mengembalikan true jika ada kotak yang terbentuk
        formed = False
        if x % 2 == 0: # horizontal
            if x<6 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y+3] and self.board[x*4-x//2 + y + 4] and self.board[(x+2)*4-x//2+ y -1]:
                #kotak bagian atas
                self.skor[playerTurn] += 1
                formed = True
            if x>0 and self.board[x*4-x//2 + y] and self.board[x*4-x//2 + y-3] and self.board[x*4-x//2 + y - 4] and self.board[(x-2)*4-x//2+ y +1]:
                #kotak bagian bawah
                self.skor[playerTurn] += 1
                formed = True
        else: #x%2==1, vertical
            if y<3 and self.board[x*4 -(x-1)//2 + y -1] and self.board[x*4-(x-1)//2 + y] and self.board[x*4-(x-1)//2 + y - 4] and self.board[(x+1)*4-(x-1)//2+ y -1]:
                #kotak bagian kanan
                self.skor[playerTurn] += 1
                formed = True
            if y>0 and self.board[x*4 -(x-1)//2 + y -2] and self.board[x*4-(x-1)//2 + y-1] and self.board[x*4-(x-1)//2 + y - 5] and self.board[(x+1)*4-(x-1)//2+ y -2]:
                #kotak bagian kiri
                self.skor[playerTurn] += 1
                formed = True
        return formed

    def move(self, playerTurn, x, y):
        #mengisi board dan menghapus move pada listMove
        if x % 2 == 0:
            self.board[x*4-x//2 + y] = True
        else:
            self.board[x*4-(x-1)//2 + y -1] = True
        self.listMove.remove((x, y))
        turn = self.formedBox(playerTurn, x, y) #jika true, playerTurn akan mendapatkan gilirannya lagi
        return turn

    def copy(self):
        #membuat copy dari objek sendiri
        newNode = DotsAndBoxes()
        newNode.board = self.board[:]
        newNode.listMove = self.listMove[:]
        newNode.skor = self.skor[:]
        return newNode