import copy

import pytest

import app


@pytest.fixture
def client():
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    app.app.config.update(TESTING=True)

    with app.app.test_client() as test_client:
        yield test_client

    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None


def test_index_returns_rendered_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_new_game_uses_default_clues_and_returns_puzzle(client, monkeypatch):
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[1 for _ in range(9)] for _ in range(9)]
    calls = []

    def fake_generate_puzzle(clues):
        calls.append(clues)
        return puzzle, solution

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new')

    assert response.status_code == 200
    assert response.get_json() == {'puzzle': puzzle}
    assert calls == [35]
    assert app.CURRENT == {'puzzle': puzzle, 'solution': solution}


def test_new_game_passes_requested_clues(client, monkeypatch):
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[1 for _ in range(9)] for _ in range(9)]
    calls = []

    def fake_generate_puzzle(clues):
        calls.append(clues)
        return puzzle, solution

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?clues=40')

    assert response.status_code == 200
    assert calls == [40]
    assert response.get_json() == {'puzzle': puzzle}


@pytest.mark.parametrize('difficulty, expected_clues', [
    ('easy', 40),
    ('medium', 32),
    ('hard', 24),
])
def test_new_game_maps_difficulty_to_clues(client, monkeypatch, difficulty, expected_clues):
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[1 for _ in range(9)] for _ in range(9)]
    calls = []

    def fake_generate_puzzle(clues):
        calls.append(clues)
        return puzzle, solution

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get(f'/new?difficulty={difficulty}')

    assert response.status_code == 200
    assert response.get_json() == {'puzzle': puzzle}
    assert calls == [expected_clues]


def test_new_game_rejects_unknown_difficulty(client, monkeypatch):
    generate_called = False

    def fake_generate_puzzle(clues):
        nonlocal generate_called
        generate_called = True
        return [], []

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?difficulty=expert')

    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid difficulty'}
    assert generate_called is False


def test_check_solution_returns_error_before_new_game(client):
    response = client.post('/check', json={'board': []})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_returns_no_incorrect_cells_for_solution(client):
    solution = [[number for number in range(1, 10)] for _ in range(9)]
    app.CURRENT['solution'] = solution

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_solution_reports_incorrect_coordinates(client):
    solution = [[number for number in range(1, 10)] for _ in range(9)]
    board = copy.deepcopy(solution)
    board[2][4] = 0
    app.CURRENT['solution'] = solution

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[2, 4]]}
