import math

rows=3
cols=3
maxVal_rowcol=3
X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(gameBoard):
    c1 = 0
    c2 = 0
    for i in range(maxVal_rowcol):
        for j in range(maxVal_rowcol):
            if gameBoard[i][j] == X:
                c1 += 1
            elif gameBoard[i][j] == O:
                c2 += 1

    if c1 == c2:
        return X
    elif c1 > c2:
        return O
    else:
        return X


def actions(gameBoard):
    actions = set()
    for i in range(3):
        for j in range(3):
            if gameBoard[i][j] == None:
                actions.add((i, j))

    return actions


# def result(gameBoard, action):
#
#     if action not in actions(gameBoard):
#         return
#     new_gameBoard = [row[:] for row in gameBoard]
#     new_gameBoard[action[0]][action[1]] = player(gameBoard)
#
#     return new_gameBoard
def result(gameBoard, action):
    if action not in actions(gameBoard):
        return gameBoard  # Return the original game board if action is not valid
    new_gameBoard = [row[:] for row in gameBoard]
    new_gameBoard[action[0]][action[1]] = player(gameBoard)
    return new_gameBoard



def winner(gameBoard):

    for i in range(maxVal_rowcol):
        if gameBoard[i][0] == gameBoard[i][1] == gameBoard[i][2]:
            if gameBoard[i][0] != None:
                return gameBoard[i][0]

        if gameBoard[0][i] == gameBoard[1][i] == gameBoard[2][i]:
            if gameBoard[0][i] != None:
                return gameBoard[0][i]

    if gameBoard[0][0] == gameBoard[1][1] == gameBoard[2][2]:
        if gameBoard[0][0] != None:
            return gameBoard[0][0]
    if gameBoard[0][2] == gameBoard[1][1] == gameBoard[2][0]:
        if gameBoard[0][2] != None:
            return gameBoard[0][2]

    return None


def terminal(gameBoard):

    if winner(gameBoard) != None:
        return True
    else:
        for i in range(rows):
            for j in range(cols):
                if gameBoard[i][j] == None:
                    return False
        return True


def utility(gameBoard):

    if winner(gameBoard) == X:
        return 1
    elif winner(gameBoard) == O:
        return -1
    else:
        return 0


def maxVal(gameBoard, alpha, beta):
    if terminal(gameBoard):
        return utility(gameBoard)

    val = -math.inf
    for i in actions(gameBoard):
        val = max(val, minVal(result(gameBoard, i), alpha, beta))
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return val

def minVal(gameBoard, alpha, beta):
    if terminal(gameBoard):
        return utility(gameBoard)

    val = math.inf
    for i in actions(gameBoard):
        val = min(val, maxVal(result(gameBoard, i), alpha, beta))
        beta = min(beta, val)
        if alpha >= beta:
            break
    return val


def AlphaBetaMiniMaxAlgo(gameBoard):
    if terminal(gameBoard):
        return
    if player(gameBoard)==X:
        val=-math.inf
        action=None
        for i in actions(gameBoard):
            newVal=minVal(result(gameBoard, i), -math.inf, math.inf)
            if newVal>val:
                val=newVal
                action=i
        return action
    elif player(gameBoard)==O:
        val=math.inf
        action=None
        for i in actions(gameBoard):
            newVal = maxVal(result(gameBoard, i), -math.inf, math.inf)
            if newVal < val:
                val = newVal
                action = i
        return action


def draw_board(gameBoard):
    for i in range(rows):
        for j in range(cols):
            if gameBoard[i][j] is None:
                print(" {} ".format(i * rows + j), end="")
            else:
                print(" {} ".format(gameBoard[i][j]), end="")
            if j < cols - 1:
                print("|", end="")
        print()
        if i < rows - 1:
            print("-" * 9)

def play():
    gameBoard = initial_state()
    print("Welcome to Tic-Tac-Toe!")

    while True:
        choice = input("Do you want to play as 'X' or 'O'? ").upper()
        if choice in ('X', 'O'):
            human_player = choice
            ai_player = 'O' if choice == 'X' else 'X'
            break
        else:
            print("Invalid choice. Please choose 'X' or 'O'.")

    print("You are playing as", human_player)
    print("To make a move, enter the number corresponding to the cell:")
    draw_board(gameBoard)

    while not terminal(gameBoard):
        current_player = player(gameBoard)

        if current_player == human_player:
            while True:
                try:
                    print(f"Your turn {human_player}\n")
                    move = int(input("Enter your move (0-8): "))
                    if 0 <= move <= 8:
                        row, col = move // cols, move % cols
                        if gameBoard[row][col] is None:  
                            break
                        else:
                            print("Invalid move. Cell is already taken.")
                    else:
                        print("Invalid move. Please enter a number between 0 and 8.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        else:
            print("Coumputer's Turn")
            move = AlphaBetaMiniMaxAlgo(gameBoard)
            row, col = move

        gameBoard = result(gameBoard, (row, col))
        draw_board(gameBoard)

    game_winner = winner(gameBoard)
    if game_winner:
        print("Player", game_winner, "wins!")
    else:
        print("It's a draw!")

play()

