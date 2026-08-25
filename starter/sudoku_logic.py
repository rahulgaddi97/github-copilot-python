import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board):
    working_board = deep_copy(board)
    full_mask = (1 << SIZE) - 1
    row_masks = [0] * SIZE
    column_masks = [0] * SIZE
    box_masks = [0] * SIZE

    for row in range(SIZE):
        for col in range(SIZE):
            value = working_board[row][col]
            if value == EMPTY:
                continue
            if value < 1 or value > SIZE:
                return 0
            value_mask = 1 << (value - 1)
            box = (row // 3) * 3 + col // 3
            if (
                row_masks[row] & value_mask
                or column_masks[col] & value_mask
                or box_masks[box] & value_mask
            ):
                return 0
            row_masks[row] |= value_mask
            column_masks[col] |= value_mask
            box_masks[box] |= value_mask

    def search():
        best_cell = None
        best_candidates = 0
        best_count = SIZE + 1

        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] != EMPTY:
                    continue
                box = (row // 3) * 3 + col // 3
                candidates = full_mask & ~(
                    row_masks[row] | column_masks[col] | box_masks[box]
                )
                candidate_count = candidates.bit_count()
                if candidate_count == 0:
                    return 0
                if candidate_count < best_count:
                    best_cell = (row, col, box)
                    best_candidates = candidates
                    best_count = candidate_count
                    if candidate_count == 1:
                        break
            if best_count == 1:
                break

        if best_cell is None:
            return 1

        row, col, box = best_cell
        solutions = 0
        while best_candidates:
            value_mask = best_candidates & -best_candidates
            best_candidates &= best_candidates - 1
            row_masks[row] |= value_mask
            column_masks[col] |= value_mask
            box_masks[box] |= value_mask
            working_board[row][col] = value_mask.bit_length()
            solutions += search()
            working_board[row][col] = EMPTY
            row_masks[row] &= ~value_mask
            column_masks[col] &= ~value_mask
            box_masks[box] &= ~value_mask
            if solutions >= 2:
                return 2
        return solutions

    return search()

def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1

def generate_puzzle(clues=35):
    while True:
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
        random.shuffle(cells)
        filled_cells = SIZE * SIZE

        for row, col in cells:
            if filled_cells <= clues:
                break
            value = board[row][col]
            board[row][col] = EMPTY
            if count_solutions(board) != 1:
                board[row][col] = value
            else:
                filled_cells -= 1

        if filled_cells == clues:
            return deep_copy(board), solution
