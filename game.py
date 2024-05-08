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


def is_game_over(board):
    if get_score_of_board(board)['B'] == 30 or get_score_of_board(board)['W'] == 30:
        return True
    for i in range(8):
        for j in range(8):
            if is_found_tiles_to_be_flipped(board, 'B', i, j) or is_found_tiles_to_be_flipped(board, 'W', i, j):
                return False
    return True


# Test
main_board = initiate_board()
print(get_score_of_board(main_board)['B'])
print(get_score_of_board(main_board)['W'])
print_board(main_board)

make_move(main_board, 'W', 5, 3)
print_board(main_board)

make_move(main_board, 'B', 5, 4)
print_board(main_board)

make_move(main_board, 'W', 3, 5)
print_board(main_board)

print(is_game_over(main_board))

print(get_score_of_board(main_board)['B'])
print(get_score_of_board(main_board)['W'])