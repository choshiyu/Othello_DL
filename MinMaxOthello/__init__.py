from MinMaxOthello.OthelloGame import OthelloGame

class OthelloGame(OthelloGame):
    def __new__(cls, *args, **kargs):
        return super().__new__(cls, *args, **kargs)
