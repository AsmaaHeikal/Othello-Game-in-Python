import math

boardSize = 8
human_discs = 0
computer_discs = 0


def initiate_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    return board


def print_board(board):
    print('-' * 30)
    for row in board:
        print(' | '.join(row))
        print('-' * 30)


def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def is_found_tiles_to_be_flipped(board, tile, row, col):
    if board[row][col] == 'B' or board[row][col] == 'W' or not is_on_board(row, col):
        return False
    board[row][col] = tile
    if tile == 'B':
        other_tile = 'W'
    else:
        other_tile = 'B'

    flipped_tiles = []
    for xdir, ydir in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        x, y = row, col
        x += xdir
        y += ydir
        if is_on_board(x, y) and board[x][y] == other_tile:
            x += xdir
            y += ydir
            if not is_on_board(x, y):
                continue
            while board[x][y] == other_tile:
                x += xdir
                y += ydir
                if not is_on_board(x, y):
                    break
            if not is_on_board(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdir
                    y -= ydir
                    if x == row and y == col:
                        break
                    flipped_tiles.append([x, y])
    board[row][col] = ' '
    if len(flipped_tiles) == 0:
        return False
    return flipped_tiles


def make_move(board, tile, xstart, ystart):
    flipped_tiles = is_found_tiles_to_be_flipped(board, tile, xstart, ystart)
    if not flipped_tiles:
        return False
    board[xstart][ystart] = tile
    for x, y in flipped_tiles:
        board[x][y] = tile
    return True


def get_score_of_board(board):
    b_score = 0
    w_score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'B':
                b_score += 1
            if board[i][j] == 'W':
                w_score += 1
    return {'B': b_score, 'W': w_score}


# return array with all possible moves
def get_possible_moves(board, tile):
    possible_moves = []
    for i in range(8):
        for j in range(8):
            if is_found_tiles_to_be_flipped(board, tile, i, j):
                possible_moves.append([i, j])
    return possible_moves


# print a copy of the board with all possible moves
def print_possible_moves(board, tile):
    possible_moves = get_possible_moves(board, tile)
    board_copy = [row[:] for row in board]
    for i, j in possible_moves:
        board_copy[i][j] = '.'
    print_board(board_copy)


def is_game_over(board):
    if human_discs == 30 or computer_discs == 30:
        return True
    for i in range(8):
        for j in range(8):
            if is_found_tiles_to_be_flipped(board, 'B', i, j) or is_found_tiles_to_be_flipped(board, 'W', i, j):
                return False
    return True


def ScoredBoard(board, color):
    myboard = board
    for i in range(boardSize):
        for j in range(boardSize):
            if is_found_tiles_to_be_flipped(board, color, i, j):
                myboard[i][j] = len(is_found_tiles_to_be_flipped(board, color, i, j)) + len(
                    get_possible_moves(board, color))

    return myboard


def get_color(isComputer):
    if isComputer == 1:
        return 'W'
    else:
        return 'B'


def opposite_color(color):
    if color == 'B':
        return 'W'
    elif color == 'W':
        return 'B'


def boardEvaluation(board, color):
    score = get_score_of_board(board)[color] - get_score_of_board(board)[opposite_color(color)]
    return score



def alpha_beta(board, color, depth, move, alpha=-math.inf, beta=math.inf, isComputer=0):
    if move != [-1, -1] and not make_move(board, color, move[0], move[1]):
        return -math.inf
    
    validMoves = get_possible_moves(board, get_color(isComputer))
    if depth <= 0 or is_game_over(board):
        return boardEvaluation(board, color)
    
    if isComputer == 1:
        maxEval = -math.inf
        for i in validMoves:
            myboard = [row[:] for row in board]
            eval = alpha_beta(myboard, 'W', depth - 1, i, alpha, beta, 0)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = math.inf
        for i in validMoves:
            myboard = [row[:] for row in board]
            eval = alpha_beta(myboard, 'B', depth - 1, i, alpha, beta, 1)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
    
    
def getCompMove(board, diffLevel):
    myboard = [row[:] for row in board]
    moves = get_possible_moves(myboard, 'W')
    
    if not moves:
        return [-1, -1]

    bestScore = -math.inf
    bestMove = None
    
    for move in moves:
        score = alpha_beta(myboard, 'W', diffLevel, move, isComputer=1)
        if score > bestScore:
            bestScore = score
            bestMove = move
        myboard = [row[:] for row in board]
    
    return bestMove if bestMove else [-1, -1]

def human_player(board, color):
    while True:
        possible_moves = get_possible_moves(board, color)
        print_possible_moves(board, color)
        print("Possible moves:", possible_moves)

        his_move = input("Your turn, enter your move (row and column numbers separated by space): ")

        try:
            x, y = map(int, his_move.split())
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")
            continue

        if (x, y) in [tuple(move) for move in possible_moves]:
            return x, y
        else:
            print("Invalid move. Your move cannot flip any opposing disk. Try again.")
            continue

def othello_game():
    global human_discs
    global computer_discs
    board = initiate_board()
    print("Welcome In Othello Game :) ")
    diff_level = input("Enter Difficulty Level (1,3,5) : ")
    if diff_level != '1' and diff_level != '3' and diff_level != '5':
        print("Invalid Difficulty Level")
        return
    color_of_human = 'B'
    color_of_computer = 'W'
    while not is_game_over(board):
        human_move = human_player(board, color_of_human)
        if human_move is not None:
            make_move(board, color_of_human, human_move[0], human_move[1])
            human_discs += 1
        if is_game_over(board):
            continue
        if diff_level == '1':
            computer_move = getCompMove(board, 1)
        elif diff_level == '3':
            computer_move = getCompMove(board, 3)
        elif diff_level == '5':
            computer_move = getCompMove(board, 5)
        if computer_move != [-1, -1]:
            print("Computer Move : ", computer_move)
            make_move(board, color_of_computer, computer_move[0], computer_move[1])
            computer_discs += 1
        else:
            print("No moves for computer")
            continue
            # no computer valid moves
    else:
        compScore = get_score_of_board(board)['W']
        humanScore = get_score_of_board(board)['B']
        if compScore > humanScore:
            winner = "Computer "
        else:
            winner = "Human"
        print("Game over :( ")
        print("Computer Score : ", compScore)
        print("Human Score : ", humanScore)
        print(winner, "is the winner :D")


# Test
othello_game()
