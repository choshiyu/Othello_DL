from AIGamePlatform import Othello
from othello.bots.DeepLearning import BOT
from MinMaxOthello.bots_minmax.MinMax import BOT_minmax
import time


app=Othello() # 會開啟瀏覽器登入Google Account，目前只接受@mail1.ncnu.edu.tw及@mail.ncnu.edu.tw
bot=BOT(6)
bot_MinMax = BOT_minmax(6)

counter = -1

@app.competition(competition_id='111機器學習複賽')
def _callback_(board, color): # 函數名稱可以自訂，board是當前盤面，color代表黑子或白子
    global counter
    time.sleep(0.1)
    counter+=1
    if counter < 6: # 前幾步給model下
        return bot.getAction(board, color) # 回傳要落子的座標
    else: # 後面直接給MinMax搜整個盤面
        return bot_MinMax.getAction(board, color)