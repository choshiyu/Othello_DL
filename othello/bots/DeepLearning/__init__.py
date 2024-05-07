import numpy as np
from othello.OthelloUtil import getValidMoves
from MinMaxOthello.bots_minmax.MinMax import BOT_minmax
from othello.bots.DeepLearning.OthelloModel import OthelloModel
from othello.OthelloGame import OthelloGame
import random

bot_MinMax = BOT_minmax(6)

class BOT():

    def __init__(self, board_size, *args, **kargs):
        self.board_size=board_size
        self.minmax_generate = False  # 沒權重會用minmax_generate生棋譜
        self.model = OthelloModel( input_shape=(self.board_size, self.board_size) )
        try:
            self.model.load_weights()
            print('model loaded')
        except:
            print('no model exist')
            self.minmax_generate = True
            pass
        
        self.collect_gaming_data=False
        self.history=[]
        self.getAction_call_count = -1 # getAction的計數器
    
    def getAction(self, game, color):
        
        self.getAction_call_count += 1 # 每被呼叫一次就+1
        
        if self.minmax_generate: # 如果沒有權重，用minmax生棋譜
            
            prob = random.random()
            print(prob)
            if self.getAction_call_count < 14 and prob < 0.46:
                print('#####random')
                valids = getValidMoves(game, color)
                position = np.random.choice(range(len(valids)), size=1)[0]
                position = valids[position]
                print(position)
                
                # 如果盤面蒐集完成
                if self.collect_gaming_data:
                    tmp = np.zeros_like(game)  # 創一個和pred大小一樣的盤面
                    # 把剛剛得到的最佳valid move設置成1(代表要下這個位置)[0,0,0.8,0,0,0,0,0,0] => [0,0,1,0,0,0,0,0,0]
                    tmp[tuple(position)] = 1.0
                    tmp = tmp.flatten()  # 2維flatten成1維
                    print(tmp)
                    # 紀錄的list會記下該[原始盤面,下哪一步,旗子顏色]
                    self.history.append([np.array(game.copy()), tmp, color])

                return position
            
            else:
                print('#####MinMax')
                position = bot_MinMax.getAction(game, color)
                print(position)
                
                if self.collect_gaming_data:
                    tmp = np.zeros_like(game)  # 創一個和pred大小一樣的盤面
                    # 把剛剛得到的最佳valid move設置成1(代表要下這個位置)[0,0,0.8,0,0,0,0,0,0] => [0,0,1,0,0,0,0,0,0]
                    tmp[tuple(position)] = 1.0
                    tmp = tmp.flatten()  # 2維flatten成1維
                    print(tmp)
                    # 紀錄的list會記下該[原始盤面,下哪一步,旗子顏色]
                    self.history.append([np.array(game.copy()), tmp, color])

                return position 
        
        else:
        
            predict = self.model.predict( game )  ##登登!!!!會影響到這邊而回傳下一步，所以要去改第10行的OthelloModel
            valid_positions=getValidMoves(game, color)
            valids=np.zeros((game.size), dtype='int')
            valids[ [i[0]*self.board_size+i[1] for i in valid_positions] ]=1
            predict*=valids
            position = np.argmax(predict)
            print(position)
            
            if self.collect_gaming_data:
                tmp=np.zeros_like(predict)
                tmp[position]=1.0
                self.history.append([np.array(game.copy()), tmp, color])
            
            position=(position//self.board_size, position%self.board_size)
            return position
    
    def self_play_train(self, args): # 傳進來參數
        self.collect_gaming_data=True
        def gen_data():
            def getSymmetries(board, pi):
                # mirror, rotational
                pi_board = np.reshape(pi, (len(board), len(board)))
                l = []
                for i in range(1, 5):
                    for j in [True, False]:
                        newB = np.rot90(board, i)
                        newPi = np.rot90(pi_board, i)
                        if j:
                            newB = np.fliplr(newB)
                            newPi = np.fliplr(newPi)
                        l += [( newB, list(newPi.ravel()) )]
                return l
            self.history=[]
            history=[]
            game=OthelloGame(self.board_size)
            game.play(self, self, verbose=args['verbose'])
            for step, (board, probs, player) in enumerate(self.history):
                sym = getSymmetries(board, probs)
                for b,p in sym:
                    history.append([b, p, player])
            self.history.clear()
            game_result=game.isEndGame()
            self.getAction_call_count = -1 #重新計算
            return [(x[0],x[1]) for x in history if (game_result==0 or x[2]==game_result)]
        
        data=[]
        for i in range(args['num_of_generate_data_for_train']):
            if args['verbose']:
                print('self playing', i+1)
            data+=gen_data()
        
        self.collect_gaming_data=False
        
        self.model.fit(data, batch_size = args['batch_size'], epochs = args['epochs'])
        self.model.save_weights()
        
