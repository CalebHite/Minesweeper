"""
Module: main
Description: Entry point for the command-line Minesweeper game. Initializes the
    board, places mines, and runs the main loop until win or loss.
Inputs: Keyboard input from the player (mine count and per-turn commands) via
    imported modules; no function parameters at module level.
Outputs: Printed grid, status messages, win/loss result, and mine map on loss.
External sources: None.
Author: Charlie Doherty, Caleb Hite
Date: 09/29/2026
"""

import random
from board import create_grid
from display import print_grid
from game_logic import (
    get_mine_count,
    place_mines,
    count_adjacent_mines,
    check_game_status,
    flag_cell,
    remaining_mines,
    create_first_move_handler,
    MAX_HINTS,
)
from player_input import get_player_input, show_mines

# ================= MAIN GAME LOOP =================

if __name__ == "__main__":
    grid = create_grid(10)
    uncover_action = create_first_move_handler()

    # Set up mines and their derived adjacent-mine counts before the first move.
    total_mines = get_mine_count(10, 20)
    
    place_mines(grid, total_mines)
    count_adjacent_mines(grid)

    hints_remaining = MAX_HINTS

    final_status = "Playing"

    # Main game loop
    while check_game_status(grid) == "Playing":
        print_grid(grid)
        print(f"Mines remaining: {remaining_mines(grid, total_mines)}")
        print(f"Hints remaining: {hints_remaining}")
        print(f"Status: {check_game_status(grid)}")

        hints_remaining, quit_requested = get_player_input(
            grid, uncover_action, flag_cell, hints_remaining
        )
        if quit_requested:
            final_status = "Quit"
            break

    if final_status != "Quit":
        final_status = check_game_status(grid)

    if final_status == "Victory":
        print("Congratulations! You've won the game!")
    elif final_status == "Quit":
        print("You quit the game.")

    # Display the final game state.
    print_grid(grid)
    print(f"Mines remaining: {remaining_mines(grid, total_mines)}")
    print(f"Status: {final_status}")

    if final_status == "Game Over: Loss":
        show_mines(grid)