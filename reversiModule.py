import numpy as np

vx = [-1, -1, -1, 0, 1, 1, 1, 0]
vy = [-1, 0, 1, 1, 1, 0, -1, -1]

initialBoard = [[None for y in range(8)] for x in range(8)]
initialBoard[3][3] = initialBoard[4][4] = 'w'
initialBoard[3][4] = initialBoard[4][3] = 'b'

def getAuxilaryBoard(board, player):
    res = [[0 for y in range(8)] for x in range(8)]
    for x in range(8):
        for y in range(8):
            if board[x][y] is None: pass
            elif player == 'black':
                res[x][y] = 1 if board[x][y] == 'b' else -1
            else: res[x][y] = 1 if board[x][y] == 'w' else -1
    return res

def getInput(board, player):
    return np.array([getAuxilaryBoard(board, player)])
    '''
    return np.array([getAuxilaryBoard(board, player),
                     getAuxilaryBoard(board, opponent(player))])
    '''

def getInputLegal(board, player, penalty):
    res = [[0 for y in range(8)] for x in range(8)]
    for x in range(8):
        for y in range(8):
            if not validMove(board, player, x, y):
                res[x][y] = -penalty
    return np.array([res])

'''
def getState(board, player):
    state = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] is None: num = 0
            elif player == 'black':
                num = 1 if board[x][y] == 'b' else 2
            else: num = 1 if board[x][y] == 'w' else 2
            state = 3 * state + num
    return state * 100

def getAction(x, y):
    return 8 * x + y
'''

def reverse(c):
    return 'b' if c == 'w' else 'w'

def opponent(player):
    return 'black' if player == 'white' else 'white'

def inBoard(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def check(board, x, y, c):
    return inBoard(x, y) and board[x][y] == c

def cnt_b_w(board):
    cnt_b = cnt_w = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'b': cnt_b += 1
            elif board[x][y] == 'w': cnt_w += 1
    return cnt_b, cnt_w

def score(board, player):
    cnt_b, cnt_w = cnt_b_w(board)
    if cnt_b == cnt_w: return 0
    if cnt_b < cnt_w:
        cnt_w = 64 - cnt_b
    else: cnt_b = 64 - cnt_w
    if player == 'black':
        return cnt_b - cnt_w
    else: return cnt_w - cnt_b

def whoWin(board):
    cnt_b, cnt_w = cnt_b_w(board)
    if cnt_b > cnt_w: return 'black'
    elif cnt_b < cnt_w: return 'white'
    else: return None

def validMove(board, player, x, y):
    if not check(board, x, y, None): return False
    c = 'b' if player == 'black' else 'w'
    for d in range(8):
        i, j = x + vx[d], y + vy[d]
        while check(board, i, j, reverse(c)):
            i, j = i + vx[d], j + vy[d]
            if check(board, i, j, c):
                return True
    return False

def getPossibleMove(board, player):
    possibleMove = []
    for x in range(8):
        for y in range(8):
            if validMove(board, player, x, y):
                possibleMove.append((x, y))
    return possibleMove

def move(board, player, x, y):
    c = 'b' if player == 'black' else 'w'
    for d in range(8):
        i, j = x + vx[d], y + vy[d]
        while check(board, i, j, reverse(c)):
            i, j = i + vx[d], j + vy[d]
        if check(board, i, j, c):
            while i != x or j != y:
                i, j = i - vx[d], j - vy[d]
                board[i][j] = c

def isEndOrPassOrNot(board, player):
    for x in range(8):
        for y in range(8):
            if validMove(board, player, x, y):
                return None
    player = opponent(player)
    for x in range(8):
        for y in range(8):
            if validMove(board, player, x, y):
                return "pass"
    return "end"

