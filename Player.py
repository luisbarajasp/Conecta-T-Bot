# Player class
import random
from Node import Node
import operator

class Player(object):

    def move(self, board, turn):
        if self.first_move(board):
            return 3

        root = Node(0)

        depth = 3

        self.check_move(board,turn,root,depth,True)

        self.getMiniMax(root, depth-1, True)

        for child in root.get_children():
            print(child.get_data())

        move = root.next_hop[0]

        # print(move)

        # root.print_node()

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

                self.check_move(alt_board,turn,child,depth-1,not is_my_turn)

        # count = 0
        # for child in root.get_children():
        #     count += 1
        #     print(count)

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

        # legal_columns = []

        # if self.first_move(board):
        #     return [0,1,2,10,2,1,0]
        # else:
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
        count = 0
        if turn == 1:
            opp_turn = 2

        if self.make_T(board,turn,row,column):
            count += 1000000
        if self.make_T(board,opp_turn,row,column):
            count += 999999
        if self.make_three(board,turn,row,column):
            count += 100
        if self.make_three(board,opp_turn,row,column):
            count += 99
        if self.make_two(board,turn,row,column):
            count += 10
        if self.make_two(board,opp_turn,row,column):
            count += 9
        return count

    def make_T(self,board,turn,row,column):
        try:
            return (board[row+1][column+1] == turn and board[row][column+1] == turn and board[row-1][column+1] == turn or board[row+1][column-1] == turn and board[row][column-1] == turn and board[row-1][column-1] == turn) or (board[row-1][column-1] == turn and board[row-1][column] == turn and board[row-1][column+1] == turn or board[row+1][column-1] == turn and board[row+1][column] == turn and board[row+1][column+1] == turn) or (board[row+2][column] == turn and board[row+1][column+1] == turn and board[row][column+2] == turn or board[row][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column] == turn) or (board[row-2][column] == turn and board[row-1][column-1] == turn and board[row][column+2] == turn or board[row][column-2] == turn and board[row+1][column-1] == turn and board[row+2][column] == turn) or (board[row-1][column-1] == turn and board[row-1][column] == turn and board[row-2][column] == turn or board[row][column-2] == turn and board[row][column-1] == turn and board[row-1][column-1] == turn) or (board[row][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column-2] == turn or board[row+2][column-2] == turn and board[row+2][column-1] == turn and board[row][column-2] == turn) or (board[row+1][column-1] == turn and board[row+1][column] == turn and board[row+2][column] == turn or board[row][column-2] == turn and board[row][column-1] == turn and board[row+1][column-1] == turn) or (board[row+2][column-2] == turn and board[row+1][column-1] == turn and board[row+2][column] == turn or board[row+2][column] == turn and board[row+1][column+1] == turn and board[row+2][column+2] == turn) or (board[row+2][column] == turn and board[row+1][column] == turn and board[row+1][column+1] == turn or board[row+1][column+1] == turn and board[row][column+1] == turn and board[row][column+2] == turn) or (board[row][column+2] == turn and board[row-1][column+1] == turn and board[row-2][column+2] == turn or board[row+2][column+2] == turn and board[row+1][column+1] == turn and board[row][column+2] == turn) or (board[row-1][column] == turn and board[row-2][column] == turn and board[row-1][column+1] == turn or board[row][column+1] == turn and board[row-1][column+1] == turn and board[row][column+2] == turn) or (board[row-2][column] == turn and board[row-1][column+1] == turn and board[row-2][column+2] == turn or board[row-2][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column] == turn)
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
            or (board[row][column-2] == turn and board[row+1][column-1] == turn and board[row][column-1] == 0)):
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


        next_hop = childrenHop[index]
        next_hop.insert(0, index)
        root.set_next_hop(next_hop)

        return root.get_data()
