# Project Instructions

## Project Architecture

- This is a Flask Sudoku application located under `starter/`.
- Keep Flask route handling in `starter/app.py`.
- Keep Sudoku board generation, solving, validation, and uniqueness logic in `starter/sudoku_logic.py`.
- Keep HTML templates in `starter/templates/`.
- Keep browser behavior in `starter/static/main.js`.
- Keep presentation and responsive layout rules in `starter/static/styles.css`.
- Keep pytest tests in `starter/tests/`.
- Do not move responsibilities between these layers without a clear need.

## Python Coding Standards

- Follow readable, idiomatic Python.
- Use descriptive variable and function names.
- Preserve existing public functions and route contracts where possible.
- Keep functions focused on one responsibility.
- Validate external input at route boundaries.
- Return clear, consistent error responses for invalid requests.
- Avoid broad exception handling that hides real errors.
- Do not add unnecessary dependencies.
- Keep formatting and naming consistent with the existing code.

## Modularity and Maintainability

- Prefer small, focused changes over broad refactors.
- Reuse existing helpers and abstractions before adding new ones.
- Keep configuration centralized rather than scattering magic numbers.
- Avoid duplicating logic across routes, Python helpers, and JavaScript handlers.
- Add comments only where behavior is non-obvious.
- Do not change unrelated code while implementing a feature.

## Sudoku Generation and Uniqueness

- Every generated puzzle must have exactly one valid solution.
- Never weaken, skip, or bypass uniqueness checking.
- Preserve the existing 9x9 Sudoku structure.
- `count_solutions()` must distinguish no solution, one solution, and multiple solutions.
- Solution counting should stop after detecting more than one solution when possible.
- The solution returned with a puzzle must match that puzzle's unique solution.
- Any generator optimization must preserve the exact uniqueness guarantee.

## Difficulty Levels

- Support the existing Easy, Medium, and Hard difficulty levels.
- Difficulty must control the number of prefilled cells.
- Easy must have more prefilled cells than Medium.
- Medium must have more prefilled cells than Hard.
- Keep difficulty-to-clue configuration centralized.
- Do not introduce difficulty-specific behavior that bypasses unique-solution generation.

## Hint and Check Functionality

- A Hint action may fill exactly one currently empty cell.
- Hints must use the correct solution value and must not overwrite player-entered values.
- Prefilled and hinted cells must remain locked.
- Track hints used for the current game and reset the count for a new game.
- Check must identify incorrect entered values without revealing solution values.
- Empty cells must not be treated as incorrect.
- Preserve immediate invalid-move feedback for row, column, and 3x3-box conflicts.
- Reject or sanitize values outside the range 1-9.
- Preserve completion behavior: only a full and correct board is complete.

## Timer and Top 10 Scoreboard

- The timer starts when a new game successfully begins.
- Reset the timer for every new game.
- Ensure only one timer interval runs at a time.
- Stop the timer after successful completion.
- Ask for the player's name only after successful completion.
- Store completed scores in browser `localStorage`.
- Each score must include the player's name, elapsed time, difficulty, and hints used.
- Sort scores by fastest elapsed time.
- Retain only the 10 fastest completed games.
- Render persisted scores after page load.
- Keep scoreboard storage separate from unrelated localStorage data.
- Handle missing or malformed stored score data without breaking the game.

## Frontend JavaScript Organization

- Keep frontend state explicit and scoped to the current game.
- Use small helpers for board reading, validation, timer updates, theme changes, score loading, score saving, and rendering.
- Keep event wiring centralized during page initialization.
- Do not duplicate DOM lookup and board parsing logic unnecessarily.
- Preserve locked-cell behavior when rendering puzzles and applying hints.
- Use DOM APIs safely when rendering user-controlled score names.
- Keep completion handling idempotent so one completed game cannot create duplicate scores.

## Responsive and Accessible UI

- Keep the 9x9 board usable on desktop and mobile viewports.
- Avoid horizontal overflow on narrow screens where practical.
- Preserve clear 3x3 square boundaries in every layout.
- Ensure text, controls, cells, messages, timers, and scoreboards remain readable.
- Provide visible keyboard focus states.
- Use accessible labels and state attributes for controls.
- Use semantic HTML for controls, status messages, and scoreboard content.
- Preserve both light and dark modes.
- Theme colors must maintain adequate contrast for editable cells, prefilled cells, conflicts, buttons, messages, timer text, and scoreboard content.
- Persist an explicit light/dark theme preference when appropriate.
- Do not let theme changes alter game logic or scoreboard data.

## Testing

- Use pytest for Python and Flask tests.
- Add tests for new backend behavior and meaningful template integration.
- Test difficulty mappings, hints, checks, invalid input, completion conditions, and Sudoku uniqueness as applicable.
- Preserve the existing test suite.
- Never remove, skip, weaken, or rewrite an existing test merely to make a change pass.
- If an existing behavior intentionally changes, explain the reason and add coverage for the new contract.
- Do not claim JavaScript runtime behavior is tested by merely inspecting JavaScript source text.
- Use browser testing only when an existing browser-testing framework is available or when a new dependency is explicitly justified and approved.
- Manually verify browser-only behavior such as timer intervals, localStorage persistence, theme switching, and responsive layout when no browser test framework exists.

## Validation Workflow

- Run the complete pytest suite after every production change.
- Report the test command, number of tests passed, failures, and relevant execution time.
- Investigate and fix failures caused by the change before completing the task.
- Run focused checks first when useful, then run the complete suite.
- Check diagnostics and review the final diff for unintended changes.
- Do not commit or push changes unless explicitly requested.

## Scope Control

- Preserve all existing functionality unless a requested requirement explicitly changes it.
- Make the smallest change that satisfies the request.
- Use clear error handling for invalid input and unavailable game state.
- Do not implement unrelated features.
- Styling changes are allowed when required by an explicitly requested UI requirement such as responsive design or light/dark mode.
- Do not add timers, scoreboards, hints, notes mode, solver animation, or other functionality unless specifically requested.
- Avoid speculative refactoring and metadata churn.
