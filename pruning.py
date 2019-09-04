# pruning.py
# Ryan Moe
# Implementation of a specialized minimax algorithm using
# alpha-beta pruning to determine the AI's next move.

import pentago

# minmax node
# recursively creates a minmax tree under itself
# note: Nodes fall into two categories (placement, rotation)
# and two alignments (min or max), for a total of 4 possible behaviors.
# Placement nodes create nodes below them that have new tokens.
# Rotation nodes create nodes that have rotated boards.
# Min and Max attempt to minimize or maximize the score respectively.
# Because the root node will always be Max-Placement type,
# the depth can be used to determine which type the current node is.
class mNode:
    # board: (pentago) copy of pentago board, with hypothetical move made
    # depth: (int) depth of this node
    # maxdepth: (int) depth at which the tree should stop
    # cmd: (string) fragment of command needed to get here
    # AB: (list) The alpha and beta values from the parent node.
    # aiColor: (string) The token that max will place.
    def __init__(self, board, depth, maxdepth, cmd, AB, aiColor):
        self.board = board
        self.cmd = cmd
        self.children = []
        self.AB = AB.copy()
        self.nodesBelow = 0

        # Placement nodes will always have depth % 4 == 0 or 2
        # rotation nodes will have depth % 4 == 1 or 3
        if depth % 4 in (0,2):
            self.categ = True   #Placement
        else:
            self.categ = False  #Rotation

        # note: max nodes will always have depth % 4 == 0 or 1
        # min nodes will have depth % 4 == 2 or 3
        if depth % 4 in (0,1):
            self.align = True   #Max
            self.color = aiColor
        else:
            self.align = False  #Min
            if aiColor == 'b':
                self.color = 'w'
            else:
                self.color = 'b'

        if depth == maxdepth:
            chains = board.checkChains()
            if aiColor == 'b':
                self.value = chains[0] * chains[0] - chains[1] * chains[1]
            else:
                self.value = chains[1] * chains[1] - chains[0] * chains[0]
        else:
            if self.categ:
                for i in range(4):
                    for j in range(9):
                        if board.board[i][j] == '.':
                            nextcmd = str(i+1) + "/" + str(j+1)
                            self.board.move(self.color, i+1, j+1)
                            nextNode = mNode(self.board, depth+1, maxdepth,\
                                        nextcmd, self.AB, aiColor)
                            self.children.append(nextNode)
                            self.checkVals(nextNode)
                            self.nodesBelow += nextNode.nodesBelow + 1
                            self.board.move('.', i+1, j+1)

                            # if alpha > beta, stop expanding
                            if self.AB[0] > self.AB[1]:
                                break;
                    # if alpha > beta, stop expanding
                    if self.AB[0] > self.AB[1]:
                        break;
            else:
                for i in range(4):
                    for j in ('l','r'):
                        nextcmd = str(i+1) + str(j)
                        self.board.rotate(i+1, j)
                        nextNode = mNode(self.board, depth+1,\
                        maxdepth, nextcmd, self.AB, aiColor)
                        self.children.append(nextNode)
                        self.checkVals(nextNode)
                        self.nodesBelow += nextNode.nodesBelow + 1

                        if j == 'l':
                            self.board.rotate(i+1, 'r')
                        else:
                            self.board.rotate(i+1, 'l')

                        # if alpha > beta, stop expanding
                        if self.AB[0] > self.AB[1]:
                            break;
                    # if alpha > beta, stop expanding
                    if self.AB[0] > self.AB[1]:
                        break;

            if depth == 0:
                self.bestmove = self.bestchild.cmd\
                    + " " + self.bestchild.bestchild.cmd
                self.nodesBelow += 1

            self.children.clear()


    # Check the node value, best child, and alpha-beta values
    # against the new node to see if they need to be updated.
    def checkVals(self, nextNode):
        if nextNode == self.children[0]:
            # If this is the first node in the list
            # of children, take its value. We need
            # something to check against.
            self.value = nextNode.value
            self.bestchild = nextNode

        # Check for better node value
        # Check for better alpha-beta values
        if self.align:
            if nextNode.value > self.value:
                self.value = nextNode.value
                self.bestchild = nextNode
            if self.value > self.AB[0]:
                self.AB[0] = nextNode.value
        else:
            if nextNode.value < self.value:
                self.value = nextNode.value
                self.bestchild = nextNode
            if self.value < self.AB[1]:
                self.AB[1] = nextNode.value
