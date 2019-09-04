#  Pentago.py
#  Ryan Moe
#  Contains the board object and the methods used to interact with it

class pentago:
    def __init__(self, copyTarget = False):
        #Make the board
        self.board = []

        if copyTarget:
            for i in copyTarget.board:
                self.board.append(i.copy())
        else:
        #Populate it with the 4 sections, and . for the spaces
            for i in range(4):
                self.board.append([])
                for j in range(9):
                    self.board[i].append('.')

    #print the game board
    def display(self):
        s = self.board
        i = 0
        print("+-------+-------+")
        while i < 9:
            print("|", s[0][i], s[0][i+1], s[0][i+2], \
            "|", s[1][i], s[1][i+1], s[1][i+2], "|")
            i += 3
        print("+-------+-------+")
        i = 0
        while i < 9:
            print("|", s[2][i], s[2][i+1], s[2][i+2], \
            "|", s[3][i], s[3][i+1], s[3][i+2],"|")
            i += 3
        print("+-------+-------+")

    # Make a move: place a token and rotate a quadrant
    # player: string "b" or "w", the color of the token (black or white)
    # tokQuad: int from 1 to 4, the quadrant in which to place a token
    # tokSpace: int from 1 to 9, the space in which to place a token
    def move(self, player, tokQuad, tokSpace):
        player = player.lower()
        result = False
        if any([(player != "b" and player != "w" and player != '.'),
                tokQuad > 4, tokQuad < 1, tokSpace > 9, tokSpace < 1]):
            print("Error: Invalid token placement")
        elif self.board[tokQuad-1][tokSpace-1] != '.' and player != '.':
            print("Space already has token!")
            result = False
        else:
            self.board[tokQuad-1][tokSpace-1] = player
            result = True
        return result

    # rotate quadrant rotQuad 90 degrees in direction rotDir
    # rotQuad: int from 1 to 4, the quadrant to rotate
    # rotDir: string "r" or "l", the direction to rotate (right or left)
    def rotate(self, rotQuad, rotDir):
        rotQuad -= 1
        rotDir = rotDir.lower()

        nQuad = [] #This quadrant will replace the current one
        oQuad = self.board[rotQuad] #reference to the old quadrant
        result = False

        if  (rotQuad <= 3 and rotQuad >= 0 and \
            (rotDir == "r" or rotDir == "l")):
            if rotDir == "l":
                for i in range(3):
                    for j in range(1,4):
                        nQuad.append(oQuad[3*j - i - 1])
                result = True
            else:
                for i in range(3):
                    for j in range(3):
                        nQuad.append(oQuad[(2-j) * 3 + i])
                result = True
        else:
            print("Error: Invalid rotation")
            nQuad = oQuad
        self.board[rotQuad] = nQuad

        return result


    # Iterates the board with 4 quadrants row by row into a single list
    def __getBoardAsList(self):
        bo = self.board
        listboard = []
        for i in range(3):
            for j in range(3):
                listboard.append(bo[0][i*3 + j])
            for j in range(3):
                listboard.append(bo[1][i*3 + j])
        for i in range(3):
            for j in range(3):
                listboard.append(bo[2][i*3 + j])
            for j in range(3):
                listboard.append(bo[3][i*3 + j])
        return listboard

    # Iterates through the rows, columns, and valid diagonals of the
    # board, looking for the longest chain of both black and white.
    # Returns a tuple (b, w) containing the max chain of black and
    # white repectively.
    # Rationale: The game must know when one or both players have
    # reached 5 in a row, and the difference can be used as the
    # minmax heuristic.
    def checkChains(self):
        board = self.__getBoardAsList()
        gridMax = {'b': 0, 'w': 0}

        for i in range(6):   # pass 1: rows
            rowMax = self.__checkChainsLine(board, i*6, 1, 6)
            gridMax['b'] = max(gridMax['b'], rowMax[0])
            gridMax['w'] = max(gridMax['w'], rowMax[1])

        for i in range(6):   # pass 2: columns
            rowMax = self.__checkChainsLine(board, i, 6, 6)
            gridMax['b'] = max(gridMax['b'], rowMax[0])
            gridMax['w'] = max(gridMax['w'], rowMax[1])

        # pass 3: top-left to bottom-right
        rowMax = self.__checkChainsLine(board, 0, 7, 6)
        gridMax['b'] = max(gridMax['b'], rowMax[0])
        gridMax['w'] = max(gridMax['w'], rowMax[1])

        rowMax = self.__checkChainsLine(board, 1, 7, 5)
        gridMax['b'] = max(gridMax['b'], rowMax[0])
        gridMax['w'] = max(gridMax['w'], rowMax[1])

        rowMax = self.__checkChainsLine(board, 6, 7, 5)
        gridMax['b'] = max(gridMax['b'], rowMax[0])
        gridMax['w'] = max(gridMax['w'], rowMax[1])

        # pass 4: top-right to bottom-left
        rowMax = self.__checkChainsLine(board, 5, 5, 6)
        gridMax['b'] = max(gridMax['b'], rowMax[0])
        gridMax['w'] = max(gridMax['w'], rowMax[1])

        rowMax = self.__checkChainsLine(board, 4, 5, 5)
        gridMax['b'] = max(gridMax['b'], rowMax[0])
        gridMax['w'] = max(gridMax['w'], rowMax[1])

        rowMax = self.__checkChainsLine(board, 11, 5, 5)
        gridMax['b'] = max(gridMax['b'], rowMax[0])
        gridMax['w'] = max(gridMax['w'], rowMax[1])

        if gridMax['b'] != 5 and gridMax['w'] != 5 and '.' not in board:
            gridMax['b'] = 5    # if there are no moves left and neither
            gridMax['w'] = 5    # player has a win, force a tie

        return (gridMax['b'], gridMax['w'])

    # Iterates through a set of indices, checking the max black
    # and white tokens in a row.
    # Returns tuple (b, w), where b and w are max chains of black
    # and white tokens.
    # board: a list of all tokens on the board
    # start: (int) The first index to check
    # increment: (int) The number of indices between elements to check
    # reps: (int) The number of repetitions in the set
    def __checkChainsLine(self, board, start, increment, reps):
        rowMax = {'b': 0, 'w': 0}
        color = board[start]
        colorTotal = 0

        for i in range(reps):
            element = board[start + i * increment]
            if element == color:
                colorTotal += 1
            else:
                if color != '.':
                    if colorTotal > rowMax[color]:
                        rowMax[color] = colorTotal
                colorTotal = 1
                color = element

        if color != '.':
            if colorTotal > rowMax[color]:
                rowMax[color] = colorTotal

        return (rowMax['b'], rowMax['w'])


    # Returns (int) number of pieces on the board
    def pieces(self):
        total = 0
        for i in self.board:
            for j in i:
                if j != '.':
                    total += 1
        return total
