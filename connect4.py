from os import system, name
import time
import curses

def reverse_enum(L):
   for index in reversed(range(len(L))):
      yield index, L[index]


class Connect4:
    WIDTH = 7
    HEIGHT = 6
    SPACE = 3
    BORDER = 1
    CHIPSIZE = 1
    LEFT = 'l'
    RIGHT = 'r'
    RED = '🔴'
    BLUE = '🔵'

    gameBoard = []
    selector = 0
    status = False
    size = 0
    screen = None
    debug = None
    turn = True
    winner = None
    # true = red, false = blue

    def __init__(
        self,
    ):
        self.gameBoard = [[None] * self.WIDTH for i in range(self.HEIGHT)]
        self.selector = 0

    def printGameBoard(self, screen):
        self.printBar(screen)
        for y, _ in enumerate(range(self.HEIGHT)):
            self.printSpots(screen, y)
            self.printBar(screen)

    def printSpots(self, screen, y: int):
        s = ''
        for x, _ in enumerate(range(self.WIDTH)):
            for _ in range(self.BORDER):
                s += '|'
            for i, _ in enumerate(range(self.SPACE)):
                if (int(sum(range(1, self.SPACE)) / self.SPACE)) == i:
                    if self.gameBoard[y][x]:
                        s += self.gameBoard[y][x]
                    else:
                        s += '  '
                else:
                    s += ' '
        for _ in range(self.BORDER):
            s += "|"
        self.render(s)

    def printBar(self, screen):
        s = ''
        for i, _ in enumerate(range(self.WIDTH)):
            s += "+" * self.BORDER + "=" * self.SPACE + "="
            if i == self.WIDTH - 1:
                s += "+" * self.BORDER
        self.render(s)
    
    def render(self, s: str):
        try:
            self.screen.addstr(s+'\n')
        except curses.error:
            pass

    def getStatus(self):
        return self.status
    
    def dropChip(self):
        # do checking if the column is filled
            for i, v in reverse_enum(self.gameBoard):
                if not v[self.selector]:
                    self.gameBoard[i][self.selector] = self.RED if self.turn else self.BLUE
                    self.turn = not self.turn
                    break
    
    def main(self, screen):
        self.screen = screen
        x = 0
        y = 0
        # Clear screen
        screen.clear()
        screen.refresh()

        # Don't wait for input when calling getch
        screen.nodelay(1)
        while True:
            # screen.clear()
            # Get user input
            key = screen.getch()

            # Check for ESC key to exit the loop
            if key == 27:  # 27 is the ASCII code for ESC
                break
            
            if (self.winner):
                continue
        
            if key == 260 or key == 261:
                self.updateSelector(self.LEFT if key == 260 else self.RIGHT)
                
            if key == 32 or key == 10:
                self.dropChip()
                self.checkWin(self.BLUE if self.turn else self.RED)
            
            screen.clear()
            self.render("LEFT & RIGHT key to select, SPACE to drop (ESC to exit):\n")
            self.printGameBoard(screen)
            self.printSelector()
            if (self.winner):
                self.render(f"{self.winner} is the winner\n")
            else:
                self.render(f"It's {self.RED if self.turn else self.BLUE}'s turn\n")
            screen.refresh()
            time.sleep(0.1)


    def startGame(self):
        curses.wrapper(self.main)
        pass

    def printSelector(self):
        s = ''
        for i, _ in enumerate(range(self.WIDTH)):
            s +=" " * self.BORDER
            for z, _ in enumerate(range(self.SPACE)):
                if (int(sum(range(1, self.SPACE)) / self.SPACE)) == z and i == self.selector:
                    s += "/\\"
                else:
                    s += " "
            s += " " * self.BORDER

        self.render(s)
    
    def updateSelector(self, dir):
        if dir == self.LEFT and self.selector > 0:
            self.selector -= 1
        if dir == self.RIGHT and self.selector < self.WIDTH - 1:
            self.selector += 1

    def checkWin(self, chip):
        ## check horizontal
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH - 3):
                if (
                    self.gameBoard[y][x] == chip and
                    self.gameBoard[y][x+1] == chip and
                    self.gameBoard[y][x+2] == chip and
                    self.gameBoard[y][x+3] == chip
                ):
                    self.winner = chip
        ## check vertical
        for y in range(self.HEIGHT - 3):
            for x in range(self.WIDTH):
                if (
                    self.gameBoard[y][x] == chip and
                    self.gameBoard[y+1][x] == chip and
                    self.gameBoard[y+2][x] == chip and
                    self.gameBoard[y+3][x] == chip
                ):
                    self.winner = chip
        
        # ## check diagonal
        for y in range(self.HEIGHT - 3):
            for x in range(3, self.WIDTH):
                if (
                    self.gameBoard[y][x] == chip and 
                    self.gameBoard[y+1][x-1] == chip and 
                    self.gameBoard[y+2][x-2] == chip and 
                    self.gameBoard[y+3][x-3] == chip
                ):
                    self.winner = chip
        for y in range(self.HEIGHT - 3):
            for x in range(self.WIDTH - 3):
                if (
                    self.gameBoard[y][x] == chip and 
                    self.gameBoard[y+1][x+1] == chip and 
                    self.gameBoard[y+2][x+2] == chip and 
                    self.gameBoard[y+3][x+3] == chip
                ):
                    self.winner = chip

        pass



if __name__ == "__main__":
    game = Connect4()
    game.startGame()
