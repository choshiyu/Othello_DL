from othello.OthelloGame import OthelloGame
from AIGamePlatform import Othello
from othello.bots.DeepLearning import BOT
from MinMaxOthello.bots_minmax.MinMax import BOT_minmax
import time

start = time.time()

game = OthelloGame(6)
# black:1、white:-1
game.play(BOT(6), BOT_minmax(6))

end = time.time()
print("執行時間：%f 秒" % (end - start))