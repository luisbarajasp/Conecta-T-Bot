# Player class
import random
from Node import Node
import operator

class Player(object):

    root = Node()

    def move(self, board, turn):
        depth = 5

        return check_move(board,turn,root,depth-1,True)
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

        values = [i * mult for i in self.get_values(board,turn)]
        for column in range(7):
            child = Node(values[column])
            root.add_child(child)

        # TODO: comprobar dependiendo del max o min, modificas el tablero y mandas a llamar al siguiente checkmove
        getMiniMax(root)

        opp_turn = 1
        if turn == 1:
            opp_turn = 2

        alt_board = board

        if is_my_turn:
            self.fill_board(alt_board, column, turn)
        else:
            self.fill_board(alt_board, column, opp_turn)

        for child in root.get_children():
            check_move(alt_board,turn,child,depth-1,not is_my_turn)

    def fill_board(self,board,column,turn):
        for row in range(6):
            if board[row][column] == 0:
                board[row][column] = turn
                return

    def validate_column(self, column, board):
        for row in range(6):
            for column in range(7):
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

        legal_columns = []

        if self.first_move(board):
            return [0,1,2,3,2,1,0]
        else:
            values = []
            for column in range(7):
                # Validates that there is still space
                if self.validate_column(column, board):
                    legal_columns.append(column)
                else:
                    values.append(-999999)
                    break
                # Iterates till finding first row in this column with 0, to assign value
                for row in range(6):
                    if board[row][column] == 0:
                        values.append(self.get_column_value(board,turn,row,column))
                        break

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
            # |-
        return (board[row+1][column+1] == turn && board[row][column+1] == turn && board[row-1][column+1] == turn || board[row+1][column-1] == turn && board[row][column-1] == turn && board[row-1][column-1] == turn ) or
            # —'—
            (board[row-1][column-1] == turn && board[row-1][column] == turn && board[row-1][column+1] == turn || board[row+1][column-1] == turn && board[row+1][column] == turn && board[row+1][column+1] == turn) or
            #,\
            (board[row+2][column] == turn && board[row+1][column+1] == turn && board[row][column+2] == turn || board[row][column-2] == turn && board[row-1][column-1] == turn && board[row-2][column] == turn) or
            #`/
            (board[row-2][column] == turn && board[row-1][column-1] == turn && board[row][column+2] == turn || board[row][column-2] == turn && board[row+1][column-1] == turn && board[row+2][column] == turn) or
            #￢
            (board[row-1][column-1] == turn && board[row-1][column] == turn && board[row-2][column] == turn || board[row][column-2] == turn && board[row][column-1] == turn && board[row-1][column-1] == turn) or
            # >
            (board[row][column-2] == turn && board[row-1][column-1] == turn && board[row-2][column-2] == turn || board[row+2][column-2] == turn && board[row+2][column-1] == turn && board[row][column-2] == turn) or
            # _|
            (board[row+1][column-1] == turn && board[row+1][column] == turn && board[row+2][column] == turn || board[row][column-2] == turn && board[row][column-1] == turn && board[row+1][column-1] == turn) or
            # ∨
            (board[row+2][column-2] == turn && board[row+1][column-1] == turn && board[row+2][column] == turn || board[row+2][column] == turn && board[row+1][column+1] == turn && board[row+2][column+2] == turn) or
            # |_
            (board[row+2][column] == turn && board[row+1][column] == turn && board[row+1][column+1] == turn || board[row+1][column+1] == turn && board[row][column+1] == turn && board[row][column+2] == turn) or
            # <
            (board[row][column+2] == turn && board[row-1][column+1] == turn && board[row-2][column+2] == turn || board[row+2][column+2] == turn && board[row+1][column+1] == turn && board[row][column+2] == turn) or
            # |¯
            (board[row-1][column] == turn && board[row-2][column] == turn && board[row-1][column+1] == turn || board[row][column+1] == turn && board[row-1][column+1] == turn && board[row][column+2] == turn) or
            #^
            (board[row-2][column] == turn && board[row-1][column+1] == turn && board[row-2][column+2] == turn || board[row-2][column-2] == turn && board[row-1][column-1] == turn && board[row-2][column] == turn)

    def make_three(self,board,turn,row,column):
        return (board[row+1][column] == turn && board[row+2][column] == turn) or (board[row+1][column] == turn && board[row+1][column+1] == turn) or (board[row+1][column] == turn && board[row+1][column-1] == turn) or
            (board[row+2][column] == turn && board[row+1][column+1] == turn) or (board[row+2][column] == turn && board[row+1][column-1] == turn) or (board[row+1][column+1] == turn && board[row][column+1] == turn) or
            (board[row+1][column+1] == turn && board[row][column+2] == turn) or (board[row][column+1] == turn && board[row][column+2] == turn) or (board[row][column+1] == turn && board[row-1][column+1] == turn) or
            (board[row][column+2] == turn && board[row-2][column+1] == turn) or (board[row-1][column+1] == turn && board[row-1][column] == turn) or (board[row-1][column+1] == turn && board[row-2][column] == turn) or
            (board[row-1][column] == turn && board[row-2][column] == turn) or (board[row-1][column] == turn && board[row-1][column-1] == turn) or (board[row-2][column] == turn && board[row-1][column-1] == turn) or
            (board[row-1][column-1] == turn && board[row][column-1] == turn) or (board[row-1][column-1] == turn && board[row][column-2] == turn) or (board[row][column-1] == turn && board[row][column-2] == turn) or
            (board[row][column-1] == turn && board[row+1][column-1] == turn) or (board[row][column-2] == turn && board[row+1][column-1] == turn)

    def make_two(self,board,turn,row,column):
        return board[row-1][column] == turn or board[row-1][column-1] == turn or board[row][column-1] == turn or board[row+1][column-1] == turn or board[row+1][column] == turn or board[row+1][column+1] == turn or
            board[row][column+1] == turn or board[row-1][column+1] == turn

    def getMiniMax(self, root,isMax=True):
        data = root.get_data()
        # if not data:
        childrenData = []
        childrenHop = []

        for child in root.get_children():
            childrenData.append(getMiniMax(child, not isMax))
            childrenHop.append(child.get_next_hop())

        if isMax:
            index, data = max(enumerate(childrenData), key=operator.itemgetter(1))
        else:
            index, data = min(enumerate(childrenData), key=operator.itemgetter(1))

        next_hop = childrenHop[index]
        next_hop.insert(0, index)
        root.set_next_hop(next_hop)
        # root.set_data(data)

        return data
