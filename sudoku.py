import numpy as np


class Sudoku():
    def __init__(self):
        self.board = np.array([0]*81).reshape((9, 9))
        self.mask = np.array([False]*81).reshape((9, 9))

    def getBoard(self):
        return self.board

    def getMask(self):
        return self.mask

    def updateMask(self):
        self.mask = self.board > 0

    def inputBoard(self, board):
        self.board = board
        self.updateMask()

    def userInputBoard(self):
        self.board = input("Please enter the gameboard: ")
        self.board = np.array([int(i) for i in self.board])
        self.board = self.board.reshape((9, 9))
        self.updateMask()


class SudokuSolver(Sudoku):
    def checkValid(self, m, n):  # m=row 0-8, n=column
        num = self.board[m, n]  # that value in that pos
        for i in range(9):  # i: 0-8, check vectical line   1
            if i != m and self.board[i, n] == num:
                return False
        for i in range(9):  # check horizontal line         2
            if i != n and self.board[m, i] == num:
                return False
        for i in range(m//3*3, m//3*3+3):  # check 3x3      3
            for j in range(n//3*3, n//3*3+3):
                if i != m and j != n and self.board[i, j] == num:
                    return False
        return True  # valid

    @staticmethod
    def getNextPos(row, col):
        col += 1
        if col == 9:
            col = 0
            row += 1
        return row, col

    @staticmethod
    def getPrevPos(row, col):
        col -= 1
        if col == -1:
            col = 8
            row -= 1
        return row, col

    def solve(self):
        cur_row = 0
        cur_col = 0
        while cur_row != 9:
            if self.mask[cur_row, cur_col]:  # if the value in that pos is fixed
                cur_row, cur_col = self.getNextPos(cur_row, cur_col)
                continue
            # if =9, no possible number for that position
            if self.board[cur_row, cur_col] != 9:
                self.board[cur_row, cur_col] += 1
                if self.checkValid(cur_row, cur_col):
                    cur_row, cur_col = self.getNextPos(cur_row, cur_col)
            else:  # =9 case
                while True:
                    if cur_row == -1:  # no solution
                        print("The Sudoku has no solutions.")
                        return False
                    if self.board[cur_row, cur_col] == 9 and not self.mask[cur_row, cur_col]:
                        self.board[cur_row, cur_col] = 0
                    elif not self.mask[cur_row, cur_col]:
                        break
                    cur_row, cur_col = self.getPrevPos(cur_row, cur_col)  # go back to prev positions
        return True


class SudokuGenerator(SudokuSolver):
    def randomPosition(self):
        x, y = np.random.randint(low=0, high=9, size=(2))
        if self.board[x, y]:
            return self.randomPosition()
        return x, y

    def randomNumber(self):
        num = np.random.randint(low=1, high=10)
        x, y = self.randomPosition()
        self.board[x, y] = num
        if not self.checkValid(x, y):
            self.board[x, y] = 0
            self.randomNumber()

    def Generate(self):
        for _ in range(13):
            self.randomNumber()
        if not self.solve():
            return self.Generate()
        print(self.board)
        solvedBoard = self.board
        self.board = np.array([0]*81).reshape((9, 9))
        for _ in range(np.random.randint(low=26, high=40)):
            x, y = self.randomPosition()
            self.board[x, y] = solvedBoard[x, y]
        print(self.board)
        return self.board
