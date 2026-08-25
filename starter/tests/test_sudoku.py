import sudoku_logic


def is_valid_solution(board):
    expected = set(range(1, sudoku_logic.SIZE + 1))
    rows_valid = all(set(row) == expected for row in board)
    columns_valid = all(
        {board[row][col] for row in range(sudoku_logic.SIZE)} == expected
        for col in range(sudoku_logic.SIZE)
    )
    boxes_valid = all(
        {
            board[row][col]
            for row in range(box_row, box_row + 3)
            for col in range(box_col, box_col + 3)
        }
        == expected
        for box_row in range(0, sudoku_logic.SIZE, 3)
        for box_col in range(0, sudoku_logic.SIZE, 3)
    )
    return rows_valid and columns_valid and boxes_valid


def test_create_empty_board_returns_empty_9_by_9_board():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_does_not_share_nested_rows():
    board = [[1, 2], [3, 4]]

    copied_board = sudoku_logic.deep_copy(board)
    copied_board[0][0] = 9

    assert board[0][0] == 1
    assert copied_board[0][0] == 9


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 4) is True


def test_fill_board_creates_a_valid_solution():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert is_valid_solution(board)


def test_remove_cells_removes_the_requested_number_of_cells():
    board = [[1 for _ in range(sudoku_logic.SIZE)] for _ in range(sudoku_logic.SIZE)]

    sudoku_logic.remove_cells(board, clues=30)

    filled_cells = sum(cell != sudoku_logic.EMPTY for row in board for cell in row)
    assert filled_cells == 30


def test_generate_puzzle_returns_puzzle_and_valid_solution_with_requested_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    filled_cells = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert filled_cells == 35
    assert is_valid_solution(solution)
    assert all(
        puzzle[row][col] in (sudoku_logic.EMPTY, solution[row][col])
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )
