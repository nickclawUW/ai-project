
class Player:

    def __init__(self, name):
        self.k = 0
        self.symbol = ""
        self.h = 0
        self.w = 0
        self.players = []
        self.nm = name

    def init(self, board, k, symbol, players):
        self.h = len(board)
        self.w = len(board[0])
        self.k = k
        self.symbol = symbol
        self.players = players

    def name(self):
        return self.nm

    def introduce(self):
        return "Hello, I am {0}".format(self.name())

    def move(self, board, turn, remarks):
        return (0, 0), ""