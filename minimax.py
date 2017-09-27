import random
width, height = 7, 6

class Minimax(object):
    """ Minimax object that takes a current connect four board board
    """

    players = [1, 2]

            
    def bestMove(self, depth, board, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        
        # determine opponent's player
        if curr_player == self.players[0]:
            opp_player = self.players[1]
        else:
            opp_player = self.players[0]
        
        # enumerate all legal moves
        possible_moves = {} # will map legal move boards to their alpha values
        for col in range(7):
            # if column i is a legal move...
            if self.canMakeMove(col, board):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(board, col, curr_player)
                possible_moves[col] = -self.search(depth-1, temp, opp_player)
        
        best_alpha = -99999999
        best_move = None
        moves = possible_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move, best_alpha
        
    def search(self, depth, board, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the board is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        
        # enumerate all legal moves from this board
        possible_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.canMakeMove(i, board):
                # make the move in column i for curr_player
                temp = self.makeMove(board, i, curr_player)
                possible_moves.append(temp)
        
        # if this node (board) is a terminal node or depth == 0...
        if depth == 0 or len(possible_moves) == 0 or self.gameIsOver(board):
            # return the heuristic value of node
            return self.value(board, curr_player)
        
        # determine opponent's player
        if curr_player == self.players[0]:
            opp_player = self.players[1]
        else:
            opp_player = self.players[0]

        alpha = -99999999
        for child in possible_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

    def canMakeMove(self, column, board):
        """ Boolean function to check if a move (column) is a legal move
        """
        
        for i in range(6):
            if board[column][i] == 0:
                # once we find the first empty, we know it's a legal move
                return True
        
        # if we get here, the column is full
        return False
    
    def gameIsOver(self, board):
        if self.checkForStreak(board, self.players[0], 4) >= 1:
            return True
        elif self.checkForStreak(board, self.players[1], 4) >= 1:
            return True
        else:
            return False
        
    
    def makeMove(self, board, column, player):
        """ Change a board object to reflect a player, denoted by player,
            making a move at column 'column'
            
            Returns a copy of new board array with the added move
        """
        
        temp = [x[:] for x in board]
        for i in range(6):
            if temp[column][i] == 0:
                temp[column][i] = player
                return temp

    def value(self, board, player):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if player == self.players[0]:
            o_player = self.players[1]
        else:
            o_player = self.players[0]
        
        my_fours = self.checkForStreak(board, player, 4)
        my_threes = self.checkForStreak(board, player, 3)
        my_twos = self.checkForStreak(board, player, 2)
        opp_fours = self.checkForStreak(board, o_player, 4)
        opp_threes = self.checkForStreak(board, o_player, 3)
        opp_twos = self.checkForStreak(board, o_player, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos
        

    def checkForStreak(self, board, player, streak):
        count = 0
        # for each piece in the board...
        for i in range(7):
            for j in range(6):
                # ...that is of the player we're looking for...
                if board[i][j] == player:
                    if (streak == 4):
                        count += self.checkAnyT(i, j, player, board)
                    else:
                        # check if a vertical streak starts at (i, j)
                        count += self.verticalStreak(i, j, board, streak)
                        
                        # check if a horizontal four-in-a-row starts at (i, j)
                        count += self.horizontalStreak(i, j, board, streak)
                        
                        # check if a diagonal (either way) four-in-a-row starts at (i, j)
                        count += self.diagonalCheck(i, j, board, streak)
        # return the sum of streaks of length 'streak'
        return count
        
    def checkAnyT(self, i, j, player_number, board):
        if (self.checkWinBelow(j, i, player_number, board)
        or self.checkWinAbove(j, i, player_number, board)
        or self.checkLeft(j, i, player_number, board)
        or self.checkRight(j, i, player_number, board)
        or self.checkWinBottomRight(j, i, player_number, board)
        or self.checkWinBottomLeft(j, i, player_number, board)
        or self.checkWinTopLeft(j, i, player_number, board)
        or self.checkWinTopRight(j, i, player_number, board)):                    
            return 1
        return 0   
    
    def checkWinBelow(self, col, row, player_number, board):
        global width, height
        if(col+1 == height or row == 0 or row+1 == width): return False
        if(board[row-1][col+1] == player_number and board[row][col+1] == player_number and board[row+1][col+1] == player_number): return True
        return False

    def checkWinAbove(self, col, row, player_number, board):
        global width, height
        if(col == 0 or row == 0 or row+1 == width): return False
        if(board[row-1][col-1] == player_number and board[row][col-1] == player_number and board[row+1][col-1] == player_number): return True
        return False
        
    def checkLeft(self, col, row, player_number, board):
        global width, height
        if(row + 1 >= width or col + 1 >= height or col - 1 < 0 ): return False
        if(board[row+1][col-1] == board[row+1][col] == board[row+1][col+1] == player_number): return True
        return False
        
    def checkRight(self, col, row, player_number, board):
        global width, height
        if(row - 1 < 0 or col + 1 >= height or col - 1 < 0 ): return False
        if(board[row-1][col-1] == board[row-1][col] == board[row-1][col+1] == player_number): return True
        return False
        
    def checkWinBottomRight(self, col, row, player_number, board):
        global width, height
        if(row - 2 < 0 or col + 2 >= height): return False
        if(board[row-2][col] == player_number and board[row-1][col+1] == player_number and board[row][col+2] == player_number): return True
        return False
    
    def checkWinBottomLeft(self, col, row, player_number, board):
        global width, height
        if(row + 2 >= width or col - 2 < 0): return False
        if(board[row+2][col] == player_number and board[row+1][col-1] == player_number and board[row][col-2] == player_number): return True
        return False
        
    def checkWinTopLeft(self, col, row, player_number, board):
        global width, height
        if(row + 2 >= width or col - 2 < 0): return False
        if(board[row+2][col] == player_number and board[row+1][col-1] == player_number and board[row][col-2] == player_number): return True
        return False
        
    def checkWinTopRight(self, col, row, player_number, board):
        global width, height
        if(row - 2 < 0 or col - 2 < 0): return False
        if(board[row-2][col] == player_number and board[row-1][col-1] == player_number and board[row][col-2] == player_number): return True
        return False
            
    def verticalStreak(self, row, col, board, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if board[col][i] == board[col][row]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def horizontalStreak(self, col, row, board, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if board[j][row] == board[col][row]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def diagonalCheck(self, col, row, board, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif board[j][i] == board[col][row]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif board[j][i] == board[col][row]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total