from MinMaxOthello.OthelloGame import OthelloGame
from MinMaxOthello.bots_minmax.MinMax import BOT_minmax
import time

start = time.time()

game = OthelloGame(6)
game.play(BOT_minmax(6), BOT_minmax(6))

end = time.time()
print("執行時間：%f 秒" % (end - start))