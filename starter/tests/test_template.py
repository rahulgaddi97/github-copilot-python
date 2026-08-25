import pytest

import app


@pytest.fixture
def client():
    app.app.config.update(TESTING=True)
    return app.app.test_client()


def test_page_contains_timer_scoreboard_and_game_controls(client):
    response = client.get('/')
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="timer"' in html
    assert 'id="hints-used"' in html
    assert 'id="hint"' in html
    assert 'id="check-solution"' in html
    assert 'id="scoreboard"' in html
    assert 'id="scoreboard-body"' in html
    assert 'id="theme-toggle"' in html
    assert 'aria-pressed="false"' in html
    assert 'Difficulty' in html


def test_page_loads_existing_client_script(client):
    response = client.get('/')
    html = response.get_data(as_text=True)

    assert '<script src="/static/main.js"></script>' in html