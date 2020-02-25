from tkinter import *
from time import *
from KO_Othello import AI
from reversiModule import *
from copy import deepcopy as cp

myAI = AI()

master = Tk()
screen = Canvas(master, width=500, height=600, background="#007b00", highlightthickness=0)
screen.pack()

animation = True
maxWait = 3
blackWin = whiteWin = tie = 0
curtime = 0
waitTime = 0

def wait(t):
    global curtime, waitTime
    curtime = time()
    waitTime = max(0, min(maxWait, t))
    sleep(waitTime)

def _drawStone(c, x1, y1, x2, y2, tag):
    if c == 'b':
        screen.create_oval(x1, y1, x2, y2, tags=tag, fill="#555",outline="#555")
        screen.create_oval(x1, y1-2, x2, y2-2, tags=tag, fill="#000", outline="#000")
    else:
        screen.create_oval(x1, y1, x2, y2, tags=tag, fill="#aaa",outline="#aaa")
        screen.create_oval(x1, y1-2, x2, y2-2, tags=tag, fill="#fff", outline="#fff")

def drawStone(c, x, y, tag = None):
    if tag is None: tag = "tile {0}-{1}".format(x, y)
    _drawStone(c, 54+50*x, 54+50*y, 96+50*x, 96+50*y, tag)

def _drawAnimation(c, x, y, i):
    _drawStone(c, 54+i+50*x, 54+i+50*y, 96-i+50*x, 96-i+50*y, "tile animated")

def drawAnimation(_to, x, y):
    _from = reverse(_to)
    screen.delete("{0}-{1}".format(x, y))

    if animation:
        #Shrinking
        for i in range(21):
            _drawAnimation(_from, x, y, i)
            if i%3 == 0: wait(0.01)
            screen.update()
            screen.delete("animated")

        #Growing
        for i in reversed(range(21)):
            _drawAnimation(_to, x, y, i)
            if i%3 == 0: wait(0.01)
            screen.update()
            screen.delete("animated")

    drawStone(_to, x, y, tag = "tile")

def create_buttons():
    # Restart button
    # Background/shadow
    screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
    screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

    # Arrow
    screen.create_arc(5, 5, 45, 45, fill="#000088", width="2", style="arc", outline="white", extent=300)
    screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

    # Quit button
    # Background/shadow
    screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
    screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")

    # "X"
    screen.create_line(455, 5, 495, 45, fill="white", width="3")
    screen.create_line(495, 5, 455, 45, fill="white", width="3")

def selectMenu():
    screen.delete(ALL)

    # USER VS USER
    screen.create_rectangle(120, 170, 380, 220, fill="#000", outline="#000")
    screen.create_rectangle(125, 175, 375, 215, fill="#111", outline="#111")
    screen.create_text(250, 194, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 195, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 196, anchor="c", text="vs", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(180, 194, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 195, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 196, anchor="c", text="USER", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(320, 194, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 195, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 196, anchor="c", text="USER", font=("Consolas", 25), fill="#ffd700")

    # USER VS AI
    screen.create_rectangle(120, 245, 380, 295, fill="#000", outline="#000")
    screen.create_rectangle(125, 250, 375, 290, fill="#111", outline="#111")
    screen.create_text(250, 269, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 270, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 271, anchor="c", text="vs", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(180, 269, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 270, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 271, anchor="c", text="USER", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(320, 269, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 270, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 271, anchor="c", text="AI", font=("Consolas", 25), fill="#ffd700")

    # AI VS USER
    screen.create_rectangle(120, 320, 380, 370, fill="#000", outline="#000")
    screen.create_rectangle(125, 325, 375, 365, fill="#111", outline="#111")
    screen.create_text(250, 344, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 345, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 346, anchor="c", text="vs", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(180, 344, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 345, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 346, anchor="c", text="AI", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(320, 344, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 345, anchor="c", text="USER", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 346, anchor="c", text="USER", font=("Consolas", 25), fill="#ffd700")

    # AI VS AI
    screen.create_rectangle(120, 395, 380, 445, fill="#000", outline="#000")
    screen.create_rectangle(125, 400, 375, 440, fill="#111", outline="#111")
    screen.create_text(250, 419, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 420, anchor="c", text="vs", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 421, anchor="c", text="vs", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(180, 419, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 420, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(180, 421, anchor="c", text="AI", font=("Consolas", 25), fill="#ffd700")
    screen.create_text(320, 419, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 420, anchor="c", text="AI", font=("Consolas", 25), fill="#b29600")
    screen.create_text(320, 421, anchor="c", text="AI", font=("Consolas", 25), fill="#ffd700")

    screen.update()

# Method for drawing the gridlines
def drawGridBackground(outline=False):
    # If we want an outline on the board then draw one
    if outline:
        screen.create_rectangle(50,50,450,450,outline="#111")

    # Drawing the intermediate lines
    for i in range(7):
        lineShift = 50+50*(i+1)
        # Horizontal line
        screen.create_line(50,lineShift,450,lineShift,fill="#111")
        # Vertical line
        screen.create_line(lineShift,50,lineShift,450,fill="#111")

    screen.update()

def runGame():
    global running, keyStroke, menu
    running = keyStroke = menu = False

    # Title and shadow
    screen.create_text(250, 203, anchor="c", text="Othello", font=("Consolas", 50), fill="#aaa")
    screen.create_text(250, 200, anchor="c", text="Othello", font=("Consolas", 50), fill="#fff")

    # Start Button
    screen.create_rectangle(190, 310, 310, 360, fill="#000", outline="#000")
    screen.create_rectangle(195, 315, 305, 355, fill="#111", outline="#111")
    screen.create_text(250, 334, anchor="c", text="Start", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 335, anchor="c", text="Start", font=("Consolas", 25), fill="#b29600")
    screen.create_text(250, 334, anchor="c", text="Start", font=("Consolas", 25), fill="#ffd700")
    screen.update()

def clickHandle(event):
    global keyStroke, menu, running

    if keyStroke: return
    if time() < curtime + waitTime + 0.05: return
    keyStroke = True

    if running:
        if event.x >= 450 and event.y <= 50: master.destroy()
        elif event.x <= 50 and event.y <= 50:
            running = False
            selectMenu()
            menu = True
        elif game.isUser():
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            if 0 <= x <= 7 and 0 <= y <= 7:
                if game.validMove(x, y):
                    game.move(x, y)

    elif menu:
        if 120 <= event.x <= 380:
            if 170 <= event.y <= 220: startGame()
            elif 245 <= event.y <= 295: startGame(white = "AI")
            elif 320 <= event.y <= 370: startGame(black = "AI")
            elif 395 <= event.y <= 445:
                global animation, maxWait
                animation = False
                #maxWait = 0
                startGame(black = "AI", white = "AI")
                game.update()
                animation = True
                maxWait = 3

    elif 310 <= event.y <= 360 and 180 <= event.x <= 310:
        selectMenu()
        menu = True

    keyStroke = False

def startGame(black = None, white = None):
    global game, running, menu
    running = True
    menu = False

    screen.delete(ALL)
    create_buttons()
    drawGridBackground()

    if black is "AI": black = myAI
    if white is "AI": white = myAI
    game = Game(agentBlack = black, agentWhite = white)
    game.update()
    if game.isUser():
        game.showAppearance()
    else: game.aiMove()


class Game:
    def __init__(self, agentBlack = None, agentWhite = None):
        self.player = 'black'
        self.gameover = False
        self.agent = {'black' : agentBlack, 'white' : agentWhite}
        self.board = cp(initialBoard)
        self.prevBoard = cp(self.board)
        self.recentMove = None

    def changePlayer(self):
        self.player = opponent(self.player)

    def isUser(self):
        if self.agent[self.player] is None:
            return True
        return False

    def showAppearance(self):
        p, v = myAI.neuralNet(self.board, self.player)
        for x, y in getPossibleMove(self.board, self.player):
            screen.create_oval(68 + 50 * x, 68 + 50 * y,
                               32 + 50 * (x + 1), 32 + 50 * (y + 1),
                               tags = "highlight", fill = "orange",
                               outline = "#b29600")
            screen.create_text(20 + 50 * (x + 1), 8 + 50 * (y + 1),
                               tags = "policy", font = ("Arial", 9),
                               text = str(round(p[x][y], 3)))
        screen.create_text(300, 560, font = ("Arial", 15), tags = "value",
                           text = "value: " + str(round(64 * v)))
        '''
        for x, y in getPossibleMove(self.board, self.player):
        '''

    def aiMove(self):
        # This is for AI move! Automated moving
        wait(1)
        ai = self.agent[self.player]
        res = ai.nextMove(self.board, self.player)
        if res:
            x, y = res
            self.move(x, y)
        else: return

    def update(self):
        screen.delete("highlight")
        screen.delete("tile")
        screen.delete("policy")
        screen.delete("value")
        for x in range(8):
            for y in range(8):
                if self.prevBoard[x][y] is not None:
                    drawStone(self.prevBoard[x][y], x, y)
                elif self.board[x][y] is not None:
                    drawStone(self.board[x][y], x, y)
        screen.update()

        if self.recentMove is not None:
            i, j = self.recentMove
            c = self.board[i][j]
            for d in range(8):
                x, y = i + vx[d], j + vy[d]
                while inBoard(x, y) and self.board[x][y] != self.prevBoard[x][y]:
                    drawAnimation(self.board[x][y], x, y)
                    x, y = x + vx[d], y + vy[d]
                    screen.update()

        self.drawScoreBoard()

    def validMove(self, x, y):
        return validMove(self.board, self.player, x, y)

    def move(self, x, y):
        self.recentMove = [x, y]
        self.prevBoard = cp(self.board)
        move(self.board, self.player, x, y)
        self.changePlayer()
        self.update()

        status = isEndOrPassOrNot(self.board, self.player)
        if status == "end":
            global blackWin, whiteWin, tie
            winner = whoWin(self.board)
            if winner == "black": blackWin += 1
            elif winner == "white": whiteWin += 1
            else: tie += 1
            screen.create_text(300, 560, anchor="c",font=("Arial", 15), text="The game is done!")
            return
        elif status == "pass":
            self.changePlayer()
            wait(3)

        if self.isUser():
            self.showAppearance()
        else: self.aiMove()

    def drawScoreBoard(self):
        screen.delete("score")
        blackScore = whiteScore = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 'b':
                    blackScore += 1
                elif self.board[x][y] == 'w':
                    whiteScore += 1

        screen.create_oval(60, 475, 90, 505, fill = 'black', outline = 'black')
        screen.create_oval(60, 540, 90, 570, fill = 'white', outline = 'white')
        screen.create_text(130, 490, anchor = "c", tags = "score",
                           font = ("Arial", 40), fill = "black", text = blackScore)
        screen.create_text(130, 555, anchor = "c", tags = "score",
                           font = ("Arial", 39), fill = "white", text = whiteScore)
        screen.create_text(250, 480, anchor = "c", tags = "score",
                           font = ("Arial", 20), fill = "white", text = blackWin)
        screen.create_text(300, 480, anchor = "c", tags = "score",
                           font = ("Arial", 20), fill = "white", text = tie)
        screen.create_text(350, 480, anchor = "c", tags = "score",
                           font = ("Arial", 20), fill = "white", text = whiteWin)
        screen.create_text(250, 520, anchor = "c", tags = "score",
                           font = ("Arial", 20), fill = "black", text = "B")
        screen.create_text(300, 520, anchor = "c", tags = "score",
                           font = ("Arial", 20), fill = "black", text = "T")
        screen.create_text(350, 520, anchor = "c", tags = "score",
                           font = ("Arial", 20), fill = "black", text = "W")
        screen.update()

if __name__=="__main__":
    runGame()

    # Binding, setting
    screen.bind("<Button-1>", clickHandle)
    #screen.bind("<Key>", keyHandle)
    screen.focus_set()

    # Run forever
    master.wm_title("Othello")
    master.mainloop()



