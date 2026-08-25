// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const SCORE_STORAGE_KEY = 'sudokuTopScores';
const THEME_STORAGE_KEY = 'sudokuTheme';
let puzzle = [];
let hintsUsed = 0;
let timerInterval = null;
let timerStartedAt = null;
let elapsedSeconds = 0;
let gameCompleted = false;

function getStoredTheme() {
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  return storedTheme === 'dark' || storedTheme === 'light' ? storedTheme : null;
}

function getSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function getInitialTheme() {
  return getStoredTheme() || getSystemTheme();
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const toggle = document.getElementById('theme-toggle');
  const isDark = theme === 'dark';
  toggle.setAttribute('aria-pressed', String(isDark));
  toggle.innerText = isDark ? 'Light mode' : 'Dark mode';
}

function toggleTheme() {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  applyTheme(nextTheme);
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainingSeconds = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainingSeconds}`;
}

function updateTimerDisplay() {
  document.getElementById('timer').innerText = `Time: ${formatTime(elapsedSeconds)}`;
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  if (timerStartedAt !== null) {
    elapsedSeconds = Math.floor((Date.now() - timerStartedAt) / 1000);
  }
  updateTimerDisplay();
  timerStartedAt = null;
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  timerStartedAt = Date.now();
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds = Math.floor((Date.now() - timerStartedAt) / 1000);
    updateTimerDisplay();
  }, 1000);
}

function loadScores() {
  try {
    const storedScores = JSON.parse(localStorage.getItem(SCORE_STORAGE_KEY) || '[]');
    return Array.isArray(storedScores) ? storedScores : [];
  } catch (error) {
    return [];
  }
}

function saveScore(score) {
  const scores = [...loadScores(), score]
    .sort((first, second) => first.time - second.time)
    .slice(0, 10);
  localStorage.setItem(SCORE_STORAGE_KEY, JSON.stringify(scores));
  renderScores(scores);
}

function renderScores(scores = loadScores()) {
  const scoreboardBody = document.getElementById('scoreboard-body');
  scoreboardBody.innerHTML = '';
  scores.forEach((score, index) => {
    const row = document.createElement('tr');
    [index + 1, score.name, formatTime(score.time), score.difficulty, score.hintsUsed].forEach(value => {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.appendChild(cell);
    });
    scoreboardBody.appendChild(row);
  });
}

function readBoard() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const value = inputs[i * SIZE + j].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function hasConflict(board, row, col, value) {
  for (let index = 0; index < SIZE; index++) {
    if (index !== col && board[row][index] === value) return true;
    if (index !== row && board[index][col] === value) return true;
  }
  const startRow = row - row % 3;
  const startCol = col - col % 3;
  for (let boxRow = startRow; boxRow < startRow + 3; boxRow++) {
    for (let boxCol = startCol; boxCol < startCol + 3; boxCol++) {
      if ((boxRow !== row || boxCol !== col) && board[boxRow][boxCol] === value) {
        return true;
      }
    }
  }
  return false;
}

function refreshConflicts() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = readBoard();
  for (const input of inputs) {
    if (input.disabled) continue;
    const value = input.value;
    input.classList.remove('incorrect');
    if (value && hasConflict(board, Number(input.dataset.row), Number(input.dataset.col), Number(value))) {
      input.classList.add('incorrect');
    }
  }
}

function validateCell(input) {
  if (input.disabled) return;
  const value = input.value.replace(/[^1-9]/g, '');
  input.value = value;
  refreshConflicts();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}`);
      input.addEventListener('input', (e) => validateCell(e.target));
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  stopTimer();
  gameCompleted = false;
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  hintsUsed = 0;
  document.getElementById('hints-used').innerText = 'Hints used: 0';
  document.getElementById('message').innerText = '';
  startTimer();
}

async function requestHint() {
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board: readBoard()})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.innerText = data.error;
    return;
  }
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const input = inputs[data.row * SIZE + data.col];
  if (!input.disabled && !input.value) {
    input.value = data.value;
    input.disabled = true;
    input.className = 'sudoku-cell prefilled';
    hintsUsed = data.hints_used;
    document.getElementById('hints-used').innerText = `Hints used: ${hintsUsed}`;
  }
}

function completeGame(difficulty) {
  if (gameCompleted) return;
  gameCompleted = true;
  stopTimer();
  const name = window.prompt('Enter your name for the Top 10 scoreboard:');
  if (!name || !name.trim()) return;
  saveScore({
    name: name.trim(),
    time: elapsedSeconds,
    difficulty,
    hintsUsed,
  });
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board: readBoard()})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.className = 'message-error';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  const complete = Array.from(inputs).every(input => input.value);
  if (incorrect.size === 0 && complete) {
    msg.className = 'message-success';
    msg.innerText = 'Congratulations! You solved it!';
    completeGame(document.getElementById('difficulty').value);
  } else {
    msg.className = 'message-error';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  applyTheme(getInitialTheme());
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  renderScores();
  // initialize
  newGame();
});