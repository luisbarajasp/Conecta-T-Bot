# Player class
import random
from Node import Node
import operator

class Player(object):

    root = Node()

    def move(self, board, turn):
        depth = 5
        self.get_value(board,turn,0)

        return check_move(board,turn,root,depth-1,True)
        # return random.randint(0,6)

    def first_move(self,board):
        for column in range(7):
            if board[0][column] != 0:
                return False

        return True

    def check_move(self,board,turn,root,depth,maximum):
        if depth == 0:
            return root.get_data()

        if maximum:
            mult = 1
        else:
            mult = -1
            
        values = [i * mult for i in self.get_values(board,turn)]
        for column in range(7):
            child = Node(values[column])
            root.add_child(child)

        # TODO: comprobar dependiendo del max o min, modificas el tablero y mandas a llamar al siguiente checkmove

        for child in root.get_children():
            check_move(board,turn,child,depth-1,not maximum)

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
        if self.check_T(board,turn,row,column)


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
