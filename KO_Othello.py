from model import ReversiModel
from reversiModule import *
from util import *
from copy import deepcopy as cp
from collections import deque
import math
from time import time
import pickle

class Controller:
    def __init__(self):
        self.puct = 0.2
        self.play_now = 0
        self.plays = 3
        self.searches = 120
        self.replays = 100000
        self.mini_batches = 256
        self.trains = 20
        self.penalty = 10

class Node:
    def __init__(self, depth = 0):
        self.depth = depth
        self.n = self.p = self.w = self.q = 0
        self.edge = [[None for y in range(8)] for x in range(8)]

    def update(self, p, v):
        self.n += 1
        self.p = p
        self.w += v
        self.q = self.w / self.n

class AI:
    def __init__(self):
        self.temperature = 1
        self.param = Controller()
        self.root = None # type: Node
        self.replay_x = pickle.load(open("replay_x", "rb"))#deque()
        self.replay_l = pickle.load(open("replay_l", "rb"))#deque()
        self.replay_z = pickle.load(open("replay_z", "rb"))#deque()
        self.replay_pi = pickle.load(open("replay_pi", "rb"))#deque()
        self.model = ReversiModel('load')

    def nextMove(self, board, player):
        legalPos = getPossibleMove(board, player)
        p, v = self.neuralNet(board, player)

        pi = [[0 for y in range(8)] for x in range(8)]
        for x, y in legalPos: pi[x][y] = p[x][y]

        #fitToProb(pi)
        return pickByMax(pi)
        #return pickByProb(pi)

    def save(self):
        self.model.save()
        pickle.dump(self.replay_x, open("replay_x", "wb"))
        pickle.dump(self.replay_l, open("replay_l", "wb"))
        pickle.dump(self.replay_pi, open("replay_pi", "wb"))
        pickle.dump(self.replay_z, open("replay_z", "wb"))

    def saveReplay(self, board, player, pi, z):
        r = random.randrange(0, 8)
        r_board = rotate(board, r)

        r_x = getInput(r_board, player)
        r_l = getInputLegal(r_board, player, self.param.penalty)
        r_pi = flat(rotate(pi, r))

        self.replay_x.append(r_x)
        self.replay_l.append(r_l)
        self.replay_pi.append(r_pi)
        self.replay_z.append(z)

        while len(self.replay_x) > self.param.replays:
            self.replay_x.popleft()
            self.replay_l.popleft()
            self.replay_z.popleft()
            self.replay_pi.popleft()

    def play(self, node, board, player):
        sign = -1  # return minus value to opponent

        '''
        for row in board:
            for x in row:
                if x is None: print('o', end = "")
                else: print(x, end = "")
            print()
        '''

        status = isEndOrPassOrNot(board, player)
        if status == "end": # final reward
            #return -score(board, player) / 64
            winner = whoWin(board)
            if winner is None: return 0
            elif winner == player: return -1
            else: return 1
        elif status == "pass":
            player = opponent(player)
            sign = 1

        timer = time()
        temp = cp(board)
        searches = (self.param.plays - self.param.play_now) *\
                   self.param.searches // (60 - node.depth)
        pi = self.MCTS(node, searches, cp(board), player)
        x, y = pickByMax(pi)
        move(board, player, x, y)
        print("move", node.depth + 1)
        print(time() - timer)

        z = self.play(node.edge[x][y], board, opponent(player))
        self.saveReplay(temp, player, pi, z)

        return sign * z

    def MCTS(self, node, searches, board, player):
        for i in range(searches):
            self.search(node, cp(board), player)

        pi = [[0 for y in range(8)] for x in range(8)]

        for x in range(8):
            for y in range(8):
                edge = node.edge[x][y]
                if edge is not None:
                    pi[x][y] = math.pow(
                        edge.n, 2.001 - math.exp(node.depth / 100)
                    ) #N ^ (1 / T)

        fitToProb(pi)

        return pi

    def search(self, node, board, player):
        sign = -1  # return minus value to opponent

        status = isEndOrPassOrNot(board, player)
        if status == "pass":
            player = opponent(player)
            sign = 1

        p, v = self.neuralNet(board, player)

        if status == "end": return v # leaf node

        # select next move
        x, y = self.select(node, board, player, p)

        if node.edge[x][y] is None:
            node.edge[x][y] = Node(node.depth + 1)
        edge = node.edge[x][y]

        # move and update
        move(board, player, x, y)  # board changed
        v = self.search(edge, board, opponent(player))
        edge.update(p[x][y], v)

        return sign * v

    def select(self, node, board, player, p):
        legalPos = getPossibleMove(board, player)

        if not legalPos: return False

        totalCount = 0
        for x, y in legalPos:
            if node.edge[x][y] is not None:
                totalCount += node.edge[x][y].n
        sqrtTC = math.sqrt(totalCount)

        res = legalPos[0]
        maxValue = float('-inf')
        for x, y in legalPos:
            if node.edge[x][y] is not None:
                Q = node.edge[x][y].q
                n = node.edge[x][y].n
            else: Q = n = 0
            U = self.param.puct * p[x][y] * sqrtTC / (1 + n)

            if maxValue < Q + U:
                maxValue = Q + U
                res = x, y

        return res

    def neuralNet(self, board, player):
        input = [getInput(board, player).reshape(1, 1, 8, 8),
                 getInputLegal(board, player, self.param.penalty).reshape(1, 1, 8, 8)]
        policy, value = self.model.model.predict(input)
        policy, value = policy[0], value[0][0]
        return [[policy[8 * x + y] for y in range(8)] for x in range(8)], value

    def train(self):
        self.root = Node()
        for i in range(self.param.plays):
            timer = time()
            self.param.play_now = i
            self.play(self.root, cp(initialBoard), 'black')
            print("play", i + 1)
            print(time() - timer)

        length = len(self.replay_x)
        x = np.array(self.replay_x)
        l = np.array(self.replay_l)
        pi = np.array(self.replay_pi)
        z = np.array(self.replay_z)

        print("we have replays", length)

        for i in range(self.param.trains):
            r = random.sample(range(length),
                              min(length, self.param.mini_batches))
            x_train = [x[r], l[r]]
            y_train = [pi[r], z[r]]
            self.model.train(x_train, y_train)

if __name__ == "__main__":
    myAI = AI()

    i = 0
    while True:
        timer = time()
        myAI.train()
        print("train", i + 1)
        print(time() - timer)
        timer = time()
        myAI.save()
        print("save trained", i + 1)
        print(time() - timer)
        i += 1