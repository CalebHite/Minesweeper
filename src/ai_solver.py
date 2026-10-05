"""
Module: ai_solver
Description: AI Solver that takes a single turn on the player's behalf.
    Easy uncovers a random valid cell. Medium uses basic Minesweeper logic
    before making a random move. Hard uses the Medium rules plus the 1-2-1
    pattern before making a random move.
Inputs: Grid of Cell objects, an uncover callback, and a difficulty keyword.
Outputs: Mutated grid state through uncovering/flagging cells, console messages
    naming the AI's actions, and whether a move was made.
External sources: ChatGPT was used to help implement and explain the Medium
    and Hard AI Solver logic.
Author: Will Calhoun, Kai Barnhart
Date: 10/05/2026
"""

import random


def get_available_cells(grid):
    """Collect every cell the AI Solver is allowed to uncover."""
    return [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid))
        if not grid[row][col].is_uncovered
        and not grid[row][col].is_flagged
    ]


def get_neighbors(grid, row, col):
    """Return all valid cells surrounding a given cell."""
    neighbors = []

    for row_change in [-1, 0, 1]:
        for col_change in [-1, 0, 1]:

            if row_change == 0 and col_change == 0:
                continue

            new_row = row + row_change
            new_col = col + col_change

            if (
                0 <= new_row < len(grid)
                and 0 <= new_col < len(grid)
            ):
                neighbors.append((new_row, new_col))

    return neighbors


def cell_name(row, col):
    """Convert a row and column into Minesweeper coordinates."""
    return f"{chr(ord('A') + col)}{row + 1}"


def easy_solver_move(grid, uncover_action):
    """Uncover one random available cell."""
    available_cells = get_available_cells(grid)

    if not available_cells:
        print("AI Solver has no covered, unflagged cell left to uncover.")
        return False

    row, col = random.choice(available_cells)

    print(f"AI Solver (Easy) uncovers {cell_name(row, col)}.")
    uncover_action(grid, row, col)

    return True


def random_move(grid, uncover_action, difficulty):
    """Make a random move if no logical move can be found."""
    available_cells = get_available_cells(grid)

    if not available_cells:
        print("AI Solver has no covered, unflagged cell left to uncover.")
        return False

    row, col = random.choice(available_cells)

    print(
        f"AI Solver ({difficulty}) uncovers "
        f"{cell_name(row, col)}."
    )

    uncover_action(grid, row, col)

    return True


def medium_solver_move(grid, uncover_action, difficulty="Medium"):
    """
    Use the two basic Minesweeper rules.

    Rule 1:
    If all remaining hidden neighbors must be mines,
    flag those cells.

    Rule 2:
    If the correct number of mines are already flagged,
    uncover the remaining hidden neighbors.

    If neither rule applies, make a random move.
    """

    for row in range(len(grid)):
        for col in range(len(grid)):

            cell = grid[row][col]

            # Only revealed numbered cells give useful information.
            if not cell.is_uncovered:
                continue

            if cell.adjacent_mines == 0:
                continue

            neighbors = get_neighbors(grid, row, col)

            hidden = []
            flagged = []

            for n_row, n_col in neighbors:
                neighbor = grid[n_row][n_col]

                if neighbor.is_flagged:
                    flagged.append((n_row, n_col))

                elif not neighbor.is_uncovered:
                    hidden.append((n_row, n_col))

            # Rule 1:
            # If every remaining hidden cell must be a mine,
            # flag all of them.
            mines_left = cell.adjacent_mines - len(flagged)

            if hidden and len(hidden) == mines_left:

                for n_row, n_col in hidden:

                    if not grid[n_row][n_col].is_flagged:
                        grid[n_row][n_col].is_flagged = True

                        print(
                            f"AI Solver ({difficulty}) flags "
                            f"{cell_name(n_row, n_col)}."
                        )

                return True

            # Rule 2:
            # If all mines have already been flagged,
            # the remaining hidden cells are safe.
            if hidden and len(flagged) == cell.adjacent_mines:

                for n_row, n_col in hidden:

                    if not grid[n_row][n_col].is_flagged:

                        print(
                            f"AI Solver ({difficulty}) uncovers "
                            f"{cell_name(n_row, n_col)}."
                        )

                        uncover_action(
                            grid,
                            n_row,
                            n_col
                        )

                return True

    # No logical move was found.
    return random_move(
        grid,
        uncover_action,
        difficulty
    )


def hard_121_horizontal(grid, uncover_action):
    """Check for a horizontal 1-2-1 pattern."""

    for row in range(len(grid)):
        for col in range(len(grid) - 2):

            left = grid[row][col]
            middle = grid[row][col + 1]
            right = grid[row][col + 2]

            if not (
                left.is_uncovered
                and middle.is_uncovered
                and right.is_uncovered
            ):
                continue

            if (
                left.adjacent_mines != 1
                or middle.adjacent_mines != 2
                or right.adjacent_mines != 1
            ):
                continue

            # Check cells below the 1-2-1 pattern.
            check_row = row + 1

            if check_row < len(grid):

                outer_left = grid[check_row][col]
                inner = grid[check_row][col + 1]
                outer_right = grid[check_row][col + 2]

                if (
                    not outer_left.is_uncovered
                    and not inner.is_uncovered
                    and not outer_right.is_uncovered
                ):

                    if not outer_left.is_flagged:
                        outer_left.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(check_row, col)}."
                        )

                    if not outer_right.is_flagged:
                        outer_right.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(check_row, col + 2)}."
                        )

                    if not inner.is_flagged:

                        print(
                            f"AI Solver (Hard) uncovers "
                            f"{cell_name(check_row, col + 1)}."
                        )

                        uncover_action(
                            grid,
                            check_row,
                            col + 1
                        )

                    return True

            # Check cells above the 1-2-1 pattern.
            check_row = row - 1

            if check_row >= 0:

                outer_left = grid[check_row][col]
                inner = grid[check_row][col + 1]
                outer_right = grid[check_row][col + 2]

                if (
                    not outer_left.is_uncovered
                    and not inner.is_uncovered
                    and not outer_right.is_uncovered
                ):

                    if not outer_left.is_flagged:
                        outer_left.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(check_row, col)}."
                        )

                    if not outer_right.is_flagged:
                        outer_right.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(check_row, col + 2)}."
                        )

                    if not inner.is_flagged:

                        print(
                            f"AI Solver (Hard) uncovers "
                            f"{cell_name(check_row, col + 1)}."
                        )

                        uncover_action(
                            grid,
                            check_row,
                            col + 1
                        )

                    return True

    return False


def hard_121_vertical(grid, uncover_action):
    """Check for a vertical 1-2-1 pattern."""

    for row in range(len(grid) - 2):
        for col in range(len(grid)):

            top = grid[row][col]
            middle = grid[row + 1][col]
            bottom = grid[row + 2][col]

            if not (
                top.is_uncovered
                and middle.is_uncovered
                and bottom.is_uncovered
            ):
                continue

            if (
                top.adjacent_mines != 1
                or middle.adjacent_mines != 2
                or bottom.adjacent_mines != 1
            ):
                continue

            # Check cells to the right of the pattern.
            check_col = col + 1

            if check_col < len(grid):

                outer_top = grid[row][check_col]
                inner = grid[row + 1][check_col]
                outer_bottom = grid[row + 2][check_col]

                if (
                    not outer_top.is_uncovered
                    and not inner.is_uncovered
                    and not outer_bottom.is_uncovered
                ):

                    if not outer_top.is_flagged:
                        outer_top.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(row, check_col)}."
                        )

                    if not outer_bottom.is_flagged:
                        outer_bottom.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(row + 2, check_col)}."
                        )

                    if not inner.is_flagged:

                        print(
                            f"AI Solver (Hard) uncovers "
                            f"{cell_name(row + 1, check_col)}."
                        )

                        uncover_action(
                            grid,
                            row + 1,
                            check_col
                        )

                    return True

            # Check cells to the left of the pattern.
            check_col = col - 1

            if check_col >= 0:

                outer_top = grid[row][check_col]
                inner = grid[row + 1][check_col]
                outer_bottom = grid[row + 2][check_col]

                if (
                    not outer_top.is_uncovered
                    and not inner.is_uncovered
                    and not outer_bottom.is_uncovered
                ):

                    if not outer_top.is_flagged:
                        outer_top.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(row, check_col)}."
                        )

                    if not outer_bottom.is_flagged:
                        outer_bottom.is_flagged = True

                        print(
                            f"AI Solver (Hard) flags "
                            f"{cell_name(row + 2, check_col)}."
                        )

                    if not inner.is_flagged:

                        print(
                            f"AI Solver (Hard) uncovers "
                            f"{cell_name(row + 1, check_col)}."
                        )

                        uncover_action(
                            grid,
                            row + 1,
                            check_col
                        )

                    return True

    return False


def hard_solver_move(grid, uncover_action):
    """
    Hard first looks for the 1-2-1 pattern.

    If no 1-2-1 pattern is available, it uses the
    same logical rules as Medium.
    """

    if hard_121_horizontal(
        grid,
        uncover_action
    ):
        return True

    if hard_121_vertical(
        grid,
        uncover_action
    ):
        return True

    return medium_solver_move(
        grid,
        uncover_action,
        "Hard"
    )


# Map the command difficulty to the correct solver.
SOLVER_MOVES = {
    "EASY": easy_solver_move,
    "MEDIUM": medium_solver_move,
    "HARD": hard_solver_move,
}


def run_solver_move(grid, uncover_action, difficulty):
    """Run one AI Solver move at the requested difficulty."""

    solver_move = SOLVER_MOVES.get(
        difficulty.upper()
    )

    if solver_move is None:

        supported = ", ".join(
            sorted(SOLVER_MOVES)
        ).title()

        print(
            f"Unsupported AI Solver difficulty. "
            f"Available difficulties: {supported}."
        )

        return False

    return solver_move(
        grid,
        uncover_action
    )
