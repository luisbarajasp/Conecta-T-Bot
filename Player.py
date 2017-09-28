# Player class
import random
from Node import Node
import operator

class Player(object):

    def move(self, board, turn):
        root = Node()

        depth = 5

        return self.check_move(board,turn,root,depth-1,True)
        # return random.randint(0,6)

    def first_move(self,board):
        for column in range(7):
            if board[0][column] != 0:
                return False

        return True

    def check_move(self,board,turn,root,depth,is_my_turn):
        if depth == 0:
            return root.get_data()

        if is_my_turn:
            mult = 1
        else:
            mult = -1

        values = self.get_values(board,turn)
        values = [i * mult for i in values]
        for column in range(7):
            child = Node(values[column])
            root.add_child([child])

        self.getMiniMax(root, depth-1, is_my_turn)

        opp_turn = 1
        if turn == 1:
            opp_turn = 2

        alt_board = board

        if is_my_turn:
            self.fill_board(alt_board, column, turn)
        else:
            self.fill_board(alt_board, column, opp_turn)

        for child in root.get_children():
            self.check_move(alt_board,turn,child,depth-1,not is_my_turn)

        return root.next_hop[0]

    def fill_board(self,board,column,turn):
        for row in range(6):
            if board[row][column] == 0:
                board[row][column] = turn
                return

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

        if self.first_move(board):
            return [0,1,2,3,2,1,0]
        else:
            values = []
            for column in range(7):
                # Iterates til finding first row in this column with 0, to assign value
                for row in range(6):
                    if board[row][column] == 0:
                        value = self.get_column_value(board,turn,row,column)
                        values.append(value)
                        break
                    if row == 5 and board[row][column] != 0:
                        values.append(-999999)

            return values


    def get_column_value(self,board,turn,row,column):
        opp_turn = 1
        if turn == 1:
            opp_turn = 2
        if self.make_T(board,turn,row,column):
            return 1000000
        elif self.make_T(board,opp_turn,row,column):
            return 999999
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
            return (board[row+1][column+1] == turn and board[row][column+1] == turn and board[row-1][column+1] == turn or board[row+1][column-1] == turn and board[row][column-1] == turn and board[row-1][column-1] == turn) or (board[row-1][column-1] == turn and board[row-1][column] == turn and board[row-1][column+1] == turn or board[row+1][column-1] == turn and board[row+1][column] == turn and board[row+1][column+1] == turn) or (board[row+2][column] == turn and board[row+1][column+1] == turn and board[row][column+2] == turn or board[row][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column] == turn) or (board[row-2][column] == turn and board[row-1][column-1] == turn and board[row][column+2] == turn or board[row][column-2] == turn and board[row+1][column-1] == turn and board[row+2][column] == turn) or (board[row-1][column-1] == turn and board[row-1][column] == turn and board[row-2][column] == turn or board[row][column-2] == turn and board[row][column-1] == turn and board[row-1][column-1] == turn) or (board[row][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column-2] == turn or board[row+2][column-2] == turn and board[row+2][column-1] == turn and board[row][column-2] == turn) or (board[row+1][column-1] == turn and board[row+1][column] == turn and board[row+2][column] == turn or board[row][column-2] == turn and board[row][column-1] == turn and board[row+1][column-1] == turn) or (board[row+2][column-2] == turn and board[row+1][column-1] == turn and board[row+2][column] == turn or board[row+2][column] == turn and board[row+1][column+1] == turn and board[row+2][column+2] == turn) or (board[row+2][column] == turn and board[row+1][column] == turn and board[row+1][column+1] == turn or board[row+1][column+1] == turn and board[row][column+1] == turn and board[row][column+2] == turn) or (board[row][column+2] == turn and board[row-1][column+1] == turn and board[row-2][column+2] == turn or board[row+2][column+2] == turn and board[row+1][column+1] == turn and board[row][column+2] == turn) or (board[row-1][column] == turn and board[row-2][column] == turn and board[row-1][column+1] == turn or board[row][column+1] == turn and board[row-1][column+1] == turn and board[row][column+2] == turn) or (board[row-2][column] == turn and board[row-1][column+1] == turn and board[row-2][column+2] == turn or board[row-2][column-2] == turn and board[row-1][column-1] == turn and board[row-2][column] == turn)
        except IndexError:
            pass

    def make_three(self,board,turn,row,column):
        try:
            return (board[row+1][column] == turn and board[row+2][column] == turn) or (board[row+1][column] == turn and board[row+1][column+1] == turn) or (board[row+1][column] == turn and board[row+1][column-1] == turn) or(board[row+2][column] == turn and board[row+1][column+1] == turn) or (board[row+2][column] == turn and board[row+1][column-1] == turn) or (board[row+1][column+1] == turn and board[row][column+1] == turn) or(board[row+1][column+1] == turn and board[row][column+2] == turn) or (board[row][column+1] == turn and board[row][column+2] == turn) or (board[row][column+1] == turn and board[row-1][column+1] == turn) or(board[row][column+2] == turn and board[row-2][column+1] == turn) or (board[row-1][column+1] == turn and board[row-1][column] == turn) or (board[row-1][column+1] == turn and board[row-2][column] == turn) or(board[row-1][column] == turn and board[row-2][column] == turn) or (board[row-1][column] == turn and board[row-1][column-1] == turn) or (board[row-2][column] == turn and board[row-1][column-1] == turn) or(board[row-1][column-1] == turn and board[row][column-1] == turn) or (board[row-1][column-1] == turn and board[row][column-2] == turn) or (board[row][column-1] == turn and board[row][column-2] == turn) or(board[row][column-1] == turn and board[row+1][column-1] == turn) or (board[row][column-2] == turn and board[row+1][column-1] == turn)
        except IndexError:
            pass

    def make_two(self,board,turn,row,column):
        try:
            return board[row-1][column] == turn or board[row-1][column-1] == turn or board[row][column-1] == turn or board[row+1][column-1] == turn or board[row+1][column] == turn or board[row+1][column+1] == turn or board[row][column+1] == turn or board[row-1][column+1] == turn
        except IndexError:
            pass

    def getMiniMax(self, root, depth, isMax=True):
        # if depth == 0:

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
        # root.set_data(data)


        return root.get_data()
