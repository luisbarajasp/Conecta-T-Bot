# Player class
import random
from Node import Node
import operator
import math

width, height = 7, 6

class Player(object):

    def move(self, board, turn):
        if self.first_move(board):
            return 3

        root = Node(0)

        depth = 4

        self.check_move(board,turn,root,depth,True)

        # for index, child in enumerate(root.get_children()):
        #     if(child.get_data() > 999998):
        #         return index
        #         for ch in child.get_children():
        #             if(ch.get_data() > 999999):
        #                 child.set_data(-math.inf)

        self.getMiniMax(root, depth-1, True)
        #
        # for child in root.get_children():
        #     print(child.get_data())

        move = root.get_next_hop()[0]
        print(move)
        return move

    def first_move(self,board):
        for column in range(7):
            if board[0][column] > 0:
                return False

        return True
    def check_move(self,board,turn,root,depth,is_my_turn):
        if depth == 0:
            return root.get_data()

        opp_turn = 1
        if turn == 1:
            opp_turn = 2

        if is_my_turn:
            mult = 1
            values = self.get_values(board,turn)
        else:
            mult = -1
            values = self.get_values(board,opp_turn)
        # mult = 1

        values = [i * mult for i in values]
        for column in range(7):
            child = Node(values[column])
            root.add_child([child])
            alt_board = [x[:] for x in board]

            if self.validate_column(column, board):
                if is_my_turn:
                    alt_board = self.fill_board(alt_board, column, turn)
                else:
                    alt_board = self.fill_board(alt_board, column, opp_turn)

                # print(values)
                # self.print_game(alt_board)

                self.check_move(alt_board,turn,child,depth-1,not is_my_turn)

    def print_game(self,board):
        for row in range(5, -1, -1):
            for col in range(0, 7):
                # if(board[x][y] == 0):
                #   print (" ")
                print (board[row][col], end="  ")
            print ("\n")
        print ("\n")

    def fill_board(self,board,column,turn):
        for row in range(6):
            if board[row][column] == 0:
                board[row][column] = turn
                return board

    def validate_column(self, column, board):
        for row in range(6):
            if board[row][column] == 0:
                return True

        return False

    def get_values(self,board,turn):
        # Heuristics
        #   Make T: 1000000
        #   Block T: 999999
        #   Make 3: 100
        #   Block 3: 99
        #   Make 2: 10
        #   Block 2: 9
        #   If self begins game: 0|1|2|3|2|1|0

        values = []
        for column in range(7):
            # Iterates til finding first row in this column with 0, to assign value
            for row in range(6):
                # self.print_game(board)
                if board[row][column] == 0:
                    value = self.get_column_value(board,turn,row,column)
                    values.append(value)
                    break
                if row == 5 and board[row][column] > 0:
                    values.append(-999999)

        return values


    def get_column_value(self,board,turn,row,column):
        opp_turn = 1
        if turn == 1:
            opp_turn = 2

        if self.make_T(board,turn,row,column):
        # if self.checkAnyT(board,turn,row,column):
            return 1000000
        elif self.make_T(board,opp_turn,row,column):
        # if self.checkAnyT(board,opp_turn,row,column):
            return 999999
        elif self.make_square(board,turn,row,column):
            return 200
        elif self.make_square(board,opp_turn,row,column):
            return 199
        elif self.make_three(board,turn,row,column):
            return 100
        elif self.make_three(board,opp_turn,row,column):
            return 99
        elif self.make_two(board,turn,row,column):
            return 10
        elif self.make_two(board,opp_turn,row,column):
            return 9
        else:
            return 0

    def make_T(self,board,turn,row,column):
        try:
            if ((board[row+1][column+1] == turn and board[row][column+1] == turn and board[row-1][column+1] == turn or board[row+1][column-1] == turn and board[row][column-1] == turn and board[row-1][column-1] == turn)
            or (board[row-1][column-1] == turn and board[row-1][column] == turn and board[row-1][column+1] == turn or board[row+1][column-1] == turn and board[row+1][column] == turn and board[row+1][column+1] == turn)
            or (board[row+2][column] == turn and board[row+1][column+1] == turn and board[row][column+2] == turn or board[row][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column] == turn)
            or (board[row-2][column] == turn and board[row-1][column-1] == turn and board[row][column+2] == turn or board[row][column-2] == turn and board[row+1][column-1] == turn and board[row+2][column] == turn)
            or (board[row-1][column-1] == turn and board[row-1][column] == turn and board[row-2][column] == turn or board[row][column-2] == turn and board[row][column-1] == turn and board[row-1][column-1] == turn)
            or (board[row][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column-2] == turn or board[row+2][column-2] == turn and board[row+2][column-1] == turn and board[row][column-2] == turn)
            or (board[row+1][column-1] == turn and board[row+1][column] == turn and board[row+2][column] == turn or board[row][column-2] == turn and board[row][column-1] == turn and board[row+1][column-1] == turn)
            or (board[row+2][column-2] == turn and board[row+1][column-1] == turn and board[row+2][column] == turn or board[row+2][column] == turn and board[row+1][column+1] == turn and board[row+2][column+2] == turn)
            or (board[row+2][column] == turn and board[row+1][column] == turn and board[row+1][column+1] == turn or board[row+1][column+1] == turn and board[row][column+1] == turn and board[row][column+2] == turn)
            or (board[row][column+2] == turn and board[row-1][column+1] == turn and board[row-2][column+2] == turn or board[row+2][column+2] == turn and board[row+1][column+1] == turn and board[row][column+2] == turn)
            or (board[row-1][column] == turn and board[row-2][column] == turn and board[row-1][column+1] == turn or board[row][column+1] == turn and board[row-1][column+1] == turn and board[row][column+2] == turn)
            or (board[row-2][column] == turn and board[row-1][column+1] == turn and board[row-2][column+2] == turn or board[row-2][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column] == turn)
            or (board[row][column-1] == turn and board[row-1][column] == turn and board[row][column+1] == turn)):
                return True
        except IndexError:
            return False


    def checkAnyT(self,board,player_number, r, c,):
        if (self.checkWinBelow(r, c, player_number, board)
        or self.checkWinAbove(r, c, player_number, board)
        or self.checkLeft(r, c, player_number, board)
        or self.checkRight(r, c, player_number, board)
        or self.checkWinBottomRight(r, c, player_number, board)
        or self.checkWinBottomLeft(r, c, player_number, board)
        or self.checkWinTopLeft(r, c, player_number, board)
        or self.checkWinTopRight(r, c, player_number, board)):
            return True
        return False

    def checkWinBelow(self, row, col, player_number, board):
        global width, height
        if (col + 1 == width or row == 0 or row + 1 == height): return False
        if (board[row - 1][col + 1] == player_number and board[row][col + 1] == player_number and board[row + 1][
                col + 1] == player_number): return True
        return False

    def checkWinAbove(self, row, col, player_number, board):
        global width, height
        if (col == 0 or row == 0 or row + 1 == height): return False
        if (board[row - 1][col - 1] == player_number and board[row][col - 1] == player_number and board[row + 1][
                col - 1] == player_number): return True
        return False

    def checkLeft(self, row, col, player_number, board):
        global width, height
        if (row + 1 >= height or col + 1 >= width or col - 1 < 0): return False
        if (board[row + 1][col - 1] == board[row + 1][col] == board[row + 1][col + 1] == player_number): return True
        return False

    def checkRight(self, row, col, player_number, board):
        global width, height
        if (row - 1 < 0 or col + 1 >= width or col - 1 < 0): return False
        if (board[row - 1][col - 1] == board[row - 1][col] == board[row - 1][col + 1] == player_number): return True
        return False

    def checkWinBottomRight(self, row, col,player_number, board):
        global width, height
        if (row - 2 < 0 or col + 2 >= width): return False
        if (board[row - 2][col] == player_number and board[row - 1][col + 1] == player_number and board[row][
                col + 2] == player_number): return True
        return False

    def checkWinBottomLeft(self, row, col, player_number, board):
        global width, height
        if (row + 2 >= height or col - 2 < 0): return False
        if (board[row + 2][col] == player_number and board[row + 1][col - 1] == player_number and board[row][
                col - 2] == player_number): return True
        return False

    def checkWinTopLeft(self, row, col, player_number, board):
        global width, height
        if (row + 2 >= height or col - 2 < 0): return False
        if (board[row + 2][col] == player_number and board[row + 1][col - 1] == player_number and board[row][
                col - 2] == player_number): return True
        return False

    def checkWinTopRight(self, row, col, player_number, board):
        global width, height
        if (row - 2 < 0 or col - 2 < 0): return False
        if (board[row - 2][col] == player_number and board[row - 1][col - 1] == player_number and board[row][
                col - 2] == player_number): return True
        return False

    def make_square(self,board,turn,row,column):
        try:
            if ((board[row][column+1] == turn and board[row-1][column+1] == turn and board[row-1][column] == turn)
            or (board[row][column-1] == turn and board[row-1][column-1] == turn and board[row-1][column] == turn)):
                return True
        except IndexError:
            return False

    def make_three(self,board,turn,row,column):
        try:
            if ((board[row+1][column] == turn and board[row+2][column] == turn and board[row+1][column+1] == 0)
            or (board[row+1][column] == turn and board[row+1][column+1] == turn and board[row+1][column-1] == 0)
            or (board[row+1][column] == turn and board[row+1][column-1] == turn and board[row+1][column+1] == 0)
            or(board[row+2][column] == turn and board[row+1][column+1] == turn and board[row+1][column] == 0 )
            or (board[row+2][column] == turn and board[row+1][column-1] == turn and board[row+1][column] == 0)
            or (board[row+1][column+1] == turn and board[row][column+1] == turn and board[row-1][column+1] == 0)
            or(board[row+1][column+1] == turn and board[row][column+2] == turn and board[row][column+1] == 0)
            or (board[row][column+1] == turn and board[row][column+2] == turn and board[row+1][column+1] == 0)
            or (board[row][column+1] == turn and board[row-1][column+1] == turn and board[row+1][column+1] == 0)
            or(board[row][column+2] == turn and board[row-2][column+1] == turn and board[row][column+1] ==0)
            or (board[row-1][column+1] == turn and board[row-1][column] == turn and board[row-1][column-1] == 0)
            or (board[row-1][column+1] == turn and board[row-2][column] == turn and board[row-1][column] == 0)
            or(board[row-1][column] == turn and board[row-2][column] == turn and board[row-1][column+1] == 0)
            or (board[row-1][column] == turn and board[row-1][column-1] == turn and board[row-1][column+1] == 0)
            or (board[row-2][column] == turn and board[row-1][column-1] == turn and board[row-1][column] == 0)
            or(board[row-1][column-1] == turn and board[row][column-1] == turn and board[row+1][column+1] == 0)
            or (board[row-1][column-1] == turn and board[row][column-2] == turn and board[row][column-1] == 0)
            or (board[row][column-1] == turn and board[row][column-2] == turn and board[row+1][column-1] == 0)
            or(board[row][column-1] == turn and board[row+1][column-1] == turn and board[row-1][column-1] == 0)
            or (board[row][column-2] == turn and board[row+1][column-1] == turn and board[row][column-1] == 0)
            or (board[row+1][column+1] == turn and board[row-1][column+1] == turn and (board[row-1][column-1] == 0 or board[row+1][column-1] == 0))
            or (board[row+1][column-1] == turn and board[row-1][column-1] == turn and (board[row+1][column+1] == 0 or board[row-1][column+1] == 0))
            or (board[row][column-1] == turn and board[row][column+1] == turn)
            or (board[row][column-1] == turn and board[row-1][column] == turn)
            or (board[row-1][column-1] == turn and board[row-1][column+1] == turn and (board[row+1][column-1] == 0 or board[row+1][column+1] == 0))):
                return True
        except IndexError:
            return False

    def make_two(self,board,turn,row,column):
        try:
            return board[row-1][column] == turn or board[row-1][column-1] == turn or board[row][column-1] == turn or board[row+1][column-1] == turn or board[row+1][column] == turn or board[row+1][column+1] == turn or board[row][column+1] == turn or board[row-1][column+1] == turn
        except IndexError:
            return False

    def getMiniMax(self, root, depth, isMax=True):
        # if depth == 0:
        # print(depth)
        # if not data:
        childrenData = []
        childrenHop = []

        for child in root.get_children():
            childrenData.append(self.getMiniMax(child, depth-1, not isMax))
            childrenHop.append(child.get_next_hop())

        if not childrenData:
            return root.get_data()


        if isMax:
            index, data = max(enumerate(childrenData), key=operator.itemgetter(1))
        else:
            index, data = min(enumerate(childrenData), key=operator.itemgetter(1))

        # root.set_data(root.get_data() + data)
        next_hop = childrenHop[index]
        next_hop.insert(0, index)
        root.set_next_hop(next_hop)

        return root.get_data()
