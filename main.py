# main.py
# Ryan Moe
# Runs the pentago game, and prompts both user and AI
# when it is their turn to move.




import pruning as mm


import pentago
from random import randint




# validate user's input for their turn
def validate(move):
    result = False

    if len(move) == 6:
        if all([move[0].isnumeric(), move[1] == '/', move[2].isnumeric(),\
            move[4].isnumeric(), move[5].isalpha()]):
            result = (int(move[0]),int(move[2]), int(move[4]), move[5])
        else:
            print("Invalid format. Please try again.")
    elif move == "exit":
        result = "exit"
    else:
        print("Invalid format. Please try again.")
    return result


gameboard = pentago.pentago()
colorDict = {'b':'Black', 'w':'White'}
pColor = ''
aColor = ''
pTurn = 0
score = gameboard.checkChains()

print("Welcome to Pentago!")

while pColor != 'b' and pColor != 'w':
    pColor = input("Would you like to play black, white, or random? (b,w,r):")
    pColor = pColor.lower()
    if pColor == 'r':
        pColor = ('b','w')[randint(0,1)]
    elif pColor != 'b' and pColor != 'w':
        print("Invalid Selection. Please try again.")

print("Ok. You will play as", colorDict[pColor])

if pColor == 'b':
    aColor = 'w'
else:
    aColor = 'b'

while pTurn != '1' and pTurn != '2' and pTurn != 'r':
    pTurn = input("Would you like to go first, second, or random? (1,2,r):")
    pTurn = pTurn.lower()
    if pTurn == 'r':
        pTurn = ('1','2')[randint(0,1)]
    elif pTurn != '1' and pTurn != '2':
        print("Invalid Selection. Please try again.")

print("Ok. You will go", {'1': "first.", '2':"second."}[pTurn])

if pTurn == '1':
    pTurn = True
else:
    pTurn = False

print("\nMove format is: (Quadrant)/(Space) (Quadrant)(Direction)")
print("For Example: 3/8 1R")
print("Type \"exit\" to quit early\n")

# Main Loop
# Validates and executes player's move on their turn
# Queries for AI's move on their turn
while(score[0] < 5 and score[1] < 5):
    gameboard.display();
    if pTurn:
        print(colorDict[pColor], "turn.")
        cont = False
        while not cont:
            pMove = validate(input("Your move:"))
            if pMove == "exit":
                print("Closing...")
                exit()
            elif pMove:
                valid = gameboard.move(pColor, pMove[0], pMove[1])
                if valid:
                    score = gameboard.checkChains()
                    if score[0] >= 5 or score[1] >= 5:
                        break
                else:
                    continue

                valid = gameboard.rotate(pMove[2], pMove[3])
                if valid:
                    score = gameboard.checkChains()
                else:
                    gameboard.move('.', pMove[0], pMove[1]) #undo move
                    continue

                cont = True

    else:
        print(colorDict[aColor], "turn.")

        print("Thinking...")
        aMove = mm.mNode(gameboard, 0, 4, False,\
                                [-10,10], aColor).bestmove
        print("Computer's move:", aMove)
        aMove = validate(aMove)
        gameboard.move(aColor, aMove[0], aMove[1])
        score = gameboard.checkChains()
        if score[0] >= 5 or score[1] >= 5:
            break
        gameboard.rotate(aMove[2], aMove[3])
        score = gameboard.checkChains()

    pTurn = not pTurn

if score[0] == score[1]:
    print("Game tied!")
elif score[0] == 5:
    print("Black wins!")
elif score[1] == 5:
    print("White wins!")
else:
    print("Error: Invalid final score.")

print("Winning board:")
gameboard.display()
