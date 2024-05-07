import numpy as np
from MinMaxOthello.OthelloUtil import getValidMoves, makeMove, isValidMove, isEndGame

BLACK = 1
WHITE = -1

class OthelloGame(np.ndarray):
    def __new__(cls, n):
        return super().__new__(cls, shape=(n,n), dtype='int')
    
    def __init__(self, n):
        self.n=n
        self.current_player=BLACK
        self[np.where(self!=0)]=0
        self[int(n/2)][int(n/2)]=WHITE
        self[int(n/2)-1][int(n/2)-1]=WHITE
        self[int(n/2)-1][int(n/2)]=BLACK
        self[int(n/2)][int(n/2)-1]=BLACK
        
    def move(self, position):
        if isValidMove(self, self.current_player, position):
            makeMove(self, self.current_player, position)
            self.current_player=-self.current_player
        else:
            raise Exception('invalid move')
    
    def play(self, black, white, verbose=True):
        while isEndGame(self) == None:
            if verbose:
                print('{:#^30}'.format( ' Player '+str(self.current_player)+' ' ))
                self.showBoard()
            if len(getValidMoves(self, self.current_player))==0:
                if verbose:
                    print('no valid move, next player')
                self.current_player=-self.current_player
                continue
            if self.current_player==WHITE:
                position=white.getAction(self, self.current_player)
            else:
                position=black.getAction(self, self.current_player)
            try:
                self.move(position)
            except:
                if verbose:
                    print('invalid move', end='\n\n')
                continue
        
        if verbose:
            print('---------- Result ----------', end='\n\n')
            self.showBoard()
            print()
            print('Winner:', isEndGame(self))
        return isEndGame(self)
    
    def showBoard(self):
        corner_offset_format='{:^'+str(len(str(self.n))+1)+'}'
        print(corner_offset_format.format(''), end='')
        for i in range(self.n):
            print('{:^3}'.format( chr(ord('A')+i) ), end='')
        print()
        print(corner_offset_format.format(''), end='')
        for i in range(self.n):
            print('{:^3}'.format('-'), end='')
        print()
        for i in range(self.n):
            print(corner_offset_format.format(i+1), end='')
            for j in range(self.n):
                if isValidMove(self, self.current_player, (i,j)):
                    print('{:^3}'.format('∎'), end='')
                else:
                    print('{:^3}'.format(self[i][j]), end='')
            print()
    
    def clone(self):
        new=self.copy()
        new.n=self.n
        new.current_player=self.current_player
        return new
    
