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
    if board[row][col] != ' ' or not is_on_board(row, col):
        return False
    board[row][col] = tile
    if tile == 'B':
        other_tile = 'W'
    else:
        other_tile = 'B'
    flipped_tiles = []
    for xdir, ydir in [[0, 1],  [1, 0],  [0, -1],  [-1, 0]]:
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
    if get_score_of_board(board)['B'] == 30 or get_score_of_board(board)['W'] == 30:
        return True
    for i in range(8):
        for j in range(8):
            if is_found_tiles_to_be_flipped(board, 'B', i, j) or is_found_tiles_to_be_flipped(board, 'W', i, j):
                return False
    return True


def computer_player(board , color):
    pass

def human_player(board,color):
    while True:
        his_move=input("Your turn enter your move row and column numbers separated by space")
        x, y = map(int, his_move.split())
        if is_on_board(x, y):
           if is_found_tiles_to_be_flipped(board, color, x, y):
               return x, y
           else:
               print("Your move cannot flip any opposing disk You miss your turn :( ")
               return None
        else:
            print("Invalid move. Try again.")

def othello_game():
    board = initiate_board()
    print("Welcome In Othello Game :) ")
    while True:
        color_choice = input("Do you want to be black or white enter B or w ").upper()
        if color_choice == 'B':
            color_of_human = 'B'
            color_of_computer = 'W'
            break
        elif color_choice == 'W':
            color_of_human = 'W'
            color_of_computer = 'B'
            break
        else:
            print("Invalid Choice")
            continue

    if color_of_human == 'B':
        print_board(board)
        while not is_game_over(board):
            human_move = human_player(board, color_of_human)
            if human_move is not None:
                make_move(board, color_of_human, human_move[0], human_move[1])
                print_board(board)
            if is_game_over(board):
                break
            computer_move = computer_player(board, color_of_computer)
            if computer_move is not None:
                make_move(board, color_of_computer, computer_move[0], computer_move[1])
                print_board(board)
    else:
        print_board(board)
        while not is_game_over(board):
            computer_move = computer_player(board, color_of_computer)
            if computer_move is not None:
                make_move(board, color_of_computer, computer_move[0], computer_move[1])
                print_board(board)
            if is_game_over(board):
                break
            human_move = human_player(board, color_of_human)
            if human_move is not None:
                make_move(board, color_of_human, human_move[0], human_move[1])
                print_board(board)

    counted_disks = get_score_of_board(board)
    if counted_disks['B'] > counted_disks['W']:
        print("Black wins!")
    elif counted_disks['B'] < counted_disks['W']:
        print("White wins!")
    else:
        print("gameisover !")
# Test
othello_game()
