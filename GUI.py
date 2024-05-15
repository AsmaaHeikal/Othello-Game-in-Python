import tkinter as tk
import math
import random

boardSize = 8


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


def get_possible_moves(board, tile):
    possible_moves = []
    for i in range(8):
        for j in range(8):
            if is_found_tiles_to_be_flipped(board, tile, i, j):
                possible_moves.append([i, j])
    return possible_moves


class OthelloGUI:
    def __init__(self, master):
        self.human_discs = 0
        self.computer_discs = 0
        self.master = master
        self.master.title("Othello")
        self.master.geometry("600x600")
        self.difficulty_var = tk.StringVar(self.master)
        self.difficulty_var.set("Medium")  # Default difficulty is medium
        self.difficulty_options = ["Easy", "Medium", "Hard"]

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.title_label = tk.Label(self.main_frame, text="Welcome to Othello!", font=("Helvetica", 25))
        self.title_label.pack(pady=(25, 20))

        self.difficulty_frame = tk.Frame(self.main_frame)
        self.difficulty_frame.pack()

        self.difficulty_label = tk.Label(
            self.difficulty_frame, text="Choose difficulty:", font=("Helvetica", 16))
        self.difficulty_label.pack(side=tk.LEFT, padx=(20, 10))

        self.difficulty_menu = tk.OptionMenu(
            self.difficulty_frame, self.difficulty_var, *self.difficulty_options)
        self.difficulty_menu.config(font=("Helvetica", 15))
        self.difficulty_menu.pack(side=tk.LEFT, padx=(15, 15))

        self.start_button = tk.Button(
            self.main_frame, text="Start Game", command=self.start_game)
        self.start_button.config(font=("Helvetica", 18))
        self.start_button.pack(pady=(60, 40))

    def start_game(self):
        self.main_frame.destroy()

        self.board = initiate_board()
        self.current_turn = 'B'

        self.canvas = tk.Canvas(self.master, width=500, height=500, bg='green')
        self.canvas.pack()

        self.black_label = tk.Label(
            self.master, text="Black: 2", font=("Helvetica", 16))
        self.black_label.pack()

        self.white_label = tk.Label(
            self.master, text="White: 2", font=("Helvetica", 16))
        self.white_label.pack()
        self.draw_board()
        self.highlight_possible_moves()
        self.Controller()

    def draw_board(self):
        for i in range(boardSize):
            for j in range(boardSize):
                self.canvas.create_rectangle(j * 62.5, i * 62.5, (j + 1) * 62.5, (i + 1) * 62.5, fill='green',
                                             outline='black')
                if self.board[i][j] == 'W':
                    self.canvas.create_oval(j * 62.5 + 6.25, i * 62.5 + 6.25, (j + 1) * 62.5 - 6.25,
                                            (i + 1) * 62.5 - 6.25, fill='white', outline='black')
                elif self.board[i][j] == 'B':
                    self.canvas.create_oval(j * 62.5 + 6.25, i * 62.5 + 6.25, (j + 1) * 62.5 - 6.25,
                                            (i + 1) * 62.5 - 6.25, fill='black', outline='black')

    def update_scores(self):
        scores = get_score_of_board(self.board)
        black_score_text = "Black: " + str(scores['B'])
        white_score_text = "White: " + str(scores['W'])
        self.black_label.config(text=black_score_text, font=("Helvetica", 16))
        self.white_label.config(text=white_score_text, font=("Helvetica", 16))

    def highlight_possible_moves(self):
        if not self.is_game_over(self.board):
            possible_moves = get_possible_moves(self.board, self.current_turn)
            for move in possible_moves:
                x, y = move
                self.canvas.create_oval(y * 62.5 + 15, x * 62.5 + 15, (y + 1) * 62.5 - 15, (x + 1) * 62.5 - 15,
                                        fill='gray', outline='gray')

    def is_game_over(self, board):
        if self.human_discs == 30 or self.computer_discs == 30:
            return True
        for i in range(8):
            for j in range(8):
                if is_found_tiles_to_be_flipped(board, 'B', i, j) or is_found_tiles_to_be_flipped(board, 'W', i, j):
                    return False
        return True

    def boardEvaluation(self, board):
        score = get_score_of_board(board)["W"] - get_score_of_board(board)["B"]
        return score

    def Controller(self):
        if self.is_game_over(self.board):
            # Determine the winner and display the result
            winner_text = ""
            compScore = get_score_of_board(self.board)['W']
            humanScore = get_score_of_board(self.board)['B']

            if humanScore > compScore:
                winner_text = "Human wins"
            elif humanScore < compScore:
                winner_text = "Computer wins"
            else:
                winner_text = "It's a tie"

            self.winner_label = tk.Label(
                self.master, text=winner_text, font=("Helvetica", 20), fg="red")
            self.winner_label.pack()
            return

        if self.current_turn == "B":
            self.canvas.bind('<Button-1>', self.human_turn)
        else:
            self.master.update_idletasks()
            self.master.update()
            self.canvas.after(1000)

            computer_move = self.get_computer_move()
            if computer_move:
                make_move(self.board, "W", computer_move[0], computer_move[1])
                self.canvas.delete('all')
                self.draw_board()
                self.update_scores()
                self.computer_discs += 1
                # Check if human player has valid moves
                if get_possible_moves(self.board, "B"):
                    self.current_turn = "B"
                    self.highlight_possible_moves()
                    self.Controller()
                else:
                    # Human has no valid moves, end the game
                    self.current_turn = "W"
                    self.Controller()
                    

    def human_turn(self, event):
        if self.is_game_over(self.board):
            return
        if self.current_turn == "B":
            possible_moves = get_possible_moves(self.board, "B")
            if not possible_moves:
                self.current_turn = 'W'
                self.Controller()
                return
            else:
                x, y = int(event.y // 62.5), int(event.x // 62.5)
                if [x, y] in possible_moves:
                    make_move(self.board, "B", x, y)
                    self.canvas.delete('all')
                    self.draw_board()
                    self.human_discs += 1
                    self.update_scores()
                    self.current_turn = 'W'
                    self.Controller()
                    return

    def get_computer_move(self):
        difficulty = self.difficulty_var.get()

        if difficulty == "Easy":
            return self.getCompMove(self.board, 1)
        elif difficulty == "Medium":
            return self.getCompMove(self.board, 5)
        elif difficulty == "Hard":
            return self.getCompMove(self.board, 9)

    def getCompMove(self, board, diffLevel):
        moves = []
        myboard = [row[:] for row in board]
        self.alpha_beta(myboard, 'W', diffLevel, moves)
        maxiScore = -1000
        if len(moves) <= 0:
            return [-1, -1]

        for i in range(len(moves)):
            if isinstance(moves[i], int):
                maxiScore = max(maxiScore, moves[i])
                index = i

        result = []
        temp = []

        for item in moves:
            if item == '_':
                result.append(temp)
                temp = []
            else:
                temp.append(item)

        result.append(temp)

        cnt = -1
        index = 0
        for lst in result:
            cnt += 1
            if len(lst) > 1:
                size = len(lst)
                if maxiScore < lst[size - 1]:
                    maxiScore = lst[size - 1]
                    index = cnt

        return result[index][0]

    def alpha_beta(self, board, color, depth, compMove=[[-1, -1]], compScore=-math.inf, move=[-1, -1], alpha=-math.inf,
                   beta=math.inf, isComputer=1):
        validMoves = get_possible_moves(board, 'W')
        if make_move(board, color, move[0], move[1]) == False and move != [-1, -1]:
            return -math.inf

        if depth <= 0 or self.is_game_over(board):
            return self.boardEvaluation(board)

        if isComputer == 1:
            for i in validMoves:
                myboard = [row[:] for row in board]
                tempBoard = [row[:] for row in board]
                if make_move(tempBoard, 'W', i[0], i[1]) != False:
                    compMove.extend([i])
                ev = self.alpha_beta(
                    myboard, 'W', depth - 1, compMove, compScore, [i[0], i[1]], alpha, beta, 0)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
                compScore = max(ev, compScore)
                compMove.append(ev)
                compMove.append("_")

        elif isComputer == 0:
            for i in validMoves:
                myboard = [row[:] for row in board]
                ev = self.alpha_beta(
                    myboard, 'B', depth - 1, compMove, compScore, [i[0], i[1]], alpha, beta, 1)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
        return 0


def main():
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
