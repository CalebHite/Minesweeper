"""
Module: ai_solver
Description: AI Solver that takes a single turn on the player's behalf. Only the
    Easy difficulty is implemented; it uncovers a random cell that is still
    covered and unflagged. Medium and Hard will be added later.
Inputs: Grid of Cell objects, an uncover callback, and a difficulty keyword.
Outputs: Mutated grid state through the uncover callback, console messages naming
    the chosen cell, and whether a move was made.
External sources: None.
Author: Will Calhoun
Date: 09/30/2026
"""

import random

def get_available_cells(grid):
    """Collect every cell the AI Solver is allowed to uncover.

    Flagged and already uncovered cells are excluded so the solver never wastes a
    turn or overrides the player's flags.
    Args:
        grid (2D list): 2D representation of the grid
    Returns:
        list: (row, col) tuples for each covered, unflagged cell.
    """
    return [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid))
        if not grid[row][col].is_uncovered and not grid[row][col].is_flagged
    ]

def easy_solver_move(grid, uncover_action):
    """Uncover one random available cell for the player.

    The solver makes no attempt to avoid mines, so an Easy move can end the game.
    Args:
        grid (2D list): 2D representation of the grid
        uncover_action (function): Function to uncover a cell
    Returns:
        bool: True if a cell was uncovered, False if no cell was available.
    """
    available_cells = get_available_cells(grid)

    if not available_cells:
        print("AI Solver has no covered, unflagged cell left to uncover.")
        return False

    row, col = random.choice(available_cells)

    # Announce the choice using the same coordinate format the player types.
    print(f"AI Solver (Easy) uncovers {chr(ord('A') + col)}{row + 1}.")
    uncover_action(grid, row, col)

    return True

# Difficulty keyword to solver function. Medium and Hard are added here later.
SOLVER_MOVES = {
    "EASY": easy_solver_move,
}

def run_solver_move(grid, uncover_action, difficulty):
    """Run one AI Solver move at the requested difficulty.
    Args:
        grid (2D list): 2D representation of the grid
        uncover_action (function): Function to uncover a cell
        difficulty (str): Difficulty keyword from the player's command
    Returns:
        bool: True if the solver uncovered a cell, False otherwise.
    """
    solver_move = SOLVER_MOVES.get(difficulty.upper())

    # Difficulties that have not been implemented yet land here.
    if solver_move is None:
        supported = ", ".join(sorted(SOLVER_MOVES)).title()
        print(f"Unsupported AI Solver difficulty. Available difficulties: {supported}.")
        return False

    return solver_move(grid, uncover_action)
