from MinMaxOthello.OthelloUtil import getValidMoves, makeMove, isEndGame

class BOT_minmax():
    def __init__(self, boardsize):
        self.boardsize = boardsize
        self.player_color = 1

    def eval_fn(self, board, color): #回傳board的分數
        '''
        我的權重分數盤面，定義每個位置的分數
        棋盤的角角很重要、邊邊很危險、中間有點重要、角角的鄰近邊邊跟鄰近對角很危險
        '''
        scores = [[99, -8, 8, 8, -8, 99],
                    [-8, -24, -4, -4, -24, -8],
                    [8, -4, 7, 7, -4, 8],
                    [8, -4, 7, 7, -4, 8],
                    [-8, -24, -4, -4, -24, -8],
                    [99, -8, 8, 8, -8, 99]]

        point = 0
        
        for i in range(6):
            for j in range(6):
                if board[i][j] == self.player_color:
                    point += scores[i][j] #加相對應權重的分數
        
        for i in range(6):
            for j in range(6):
                if board[i][j] == -self.player_color:
                    point -= scores[i][j] #減相對應權重的分數

        return point #回傳盤面的分數

    def min_max(self, board, player, depth, alpha, beta):
        bestMove = [-1, -1]
        
        if depth == 0 or isEndGame(board) != None: #如果遊戲結束或是搜到我要的深度了
            return (self.eval_fn(board, self.player_color), bestMove) #回傳最佳的分數及最好的下棋座標

        moves = getValidMoves(board, player) #取得當層的合法步

        if len(moves) == 0: #如果我沒地方下，就往下一層(對手層)繼續搜尋
            return self.min_max(board.copy(), -player, depth-1, alpha, beta)

        if player == self.player_color: #自己下棋那層
            for move in moves:
                newBoard = makeMove(board.copy(), player, move) #拿到下可走步後的盤面
                (score, _) = self.min_max(newBoard, -player, depth-1, alpha, beta) #取得下一層回傳回來的最佳分數
                if score > alpha:
                    alpha = score #當前搜到的最大值
                    bestMove = move #若是最佳的score，就去取得他的index
                if alpha >= beta: # 當alpha大於等於beta時剪枝
                    break # 停止搜索
            return (alpha, bestMove)
        
        if player == -self.player_color: #對手下棋那層
            for move in moves:
                newBoard = makeMove(board.copy(), player, move) #拿到下可走步後的盤面
                (score, _) = self.min_max(newBoard, -player, depth-1, alpha, beta)
                if score < beta:
                    beta = score #當前搜到的最小值
                    bestMove = move #若是最佳的score，就去取得他的index
                if alpha >= beta: # 當alpha大於等於beta時剪枝
                    break # 停止搜索

            return (beta, bestMove)

    def getAction(self, board, player):
        self.player_color = player
        (score, bestMove) = self.min_max(board.copy(), player, 7, -100000, 100000) #傳入當前盤面、玩家、我設定的深度、alpha、beta

        return bestMove #回傳的是一個xy座標