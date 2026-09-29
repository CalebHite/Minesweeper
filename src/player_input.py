"""
Module: player_input
Description: Parses player commands (uncover, flag, hint, quit) and reveals all mine
    locations after a loss.
Inputs: Grid, uncover/flag callbacks, hints remaining; interactive command strings.
Outputs: Updated hints remaining; side effects on the grid via callbacks;
    console prompts and error messages; mine map on loss.
External sources: None.
Author: Charlie Doherty, Caleb Hite
Date: 09/29/2026
"""

from game_logic import hint_cell

def get_player_input(grid, uncover_action, flag_action, hints_remaining):
    """Get input from the player and execute the corresponding action.

    Accepted commands are `A4` to uncover,
    `A4, Flag` and `Flag, A4` to flag,
    and `A4, Hint` and `Hint, A4` (or `H` in place of `Hint`) to get a hint.
    A hint flags the cell if it's a mine, or uncovers it if it's safe.
    Each game allows a limited number of hints. Enter `Q` or `Quit` to exit.

    Args:
        grid (2D list): 2D representation of the grid
        uncover_action (function): Function to uncover a cell
        flag_action (function): Function to flag a cell
        hints_remaining (int): Number of hints the player can still use this game
    Returns:
        tuple: (hints_remaining, quit_requested) where quit_requested is True if
            the player chose to quit.
    """

    print(
        "\nEnter a command in the format 'A4' to uncover a cell, 'A4, Flag' to flag a cell, "
        "or 'A4, Hint' (or 'A4, H') for a hint. Enter 'Q' or 'Quit' to leave the game."
    )
    print(f"Hints remaining: {hints_remaining}")
    command = input("Enter command: ").strip()

    # separate the cell and action using the comma
    parts = [part.strip() for part in command.split(",")]

    if len(parts) == 1:
        cell_name = parts[0].upper() # convert to uppercase

        if cell_name in ("Q", "QUIT"):
            return hints_remaining, True

        try:
            col = ord(cell_name[0]) - ord('A') # convert letter to column index
            row = int(cell_name[1:]) - 1 # convert number to row index

        except (IndexError, ValueError):
            print("Invalid command")
            return hints_remaining, False

        if 0 <= row < len(grid) and 0 <= col < len(grid):
            uncover_action(grid, row, col)
        else:
            print("Invalid cell.")
        return hints_remaining, False

    # handle flagging and hint commands
    elif len(parts) == 2:
        first_part = parts[0].upper()
        second_part = parts[1].upper()

        # figure out which part is the cell and which is the action keyword
        if first_part == "FLAG":
            cell_name, action = second_part, "FLAG"
        elif second_part == "FLAG":
            cell_name, action = first_part, "FLAG"
        elif first_part in ("HINT", "H"):
            cell_name, action = second_part, "HINT"
        elif second_part in ("HINT", "H"):
            cell_name, action = first_part, "HINT"
        else:
            print("Invalid command.")
            return hints_remaining, False

        try:
            col = ord(cell_name[0]) - ord('A')
            row = int(cell_name[1:]) - 1
        except (IndexError, ValueError):
            print("Invalid command")
            return hints_remaining, False

        if 0 <= row < len(grid) and 0 <= col < len(grid):
            if action == "FLAG":
                flag_action(grid, row, col)
            elif hints_remaining <= 0:
                print("No hints remaining.")
            elif hint_cell(grid, row, col, uncover_action, flag_action):
                hints_remaining -= 1
        else:
            print("Invalid cell.")
        return hints_remaining, False
    else:
        print("Invalid command.")

    return hints_remaining, False

def show_mines(grid): # show location of mines after loss
    """Show the locations of all mines on the grid.
    Args:
        grid (2D list): 2D representation of the grid
    """
    print("\nMine locations:")
    size = len(grid)

    col_labels = [chr(ord('A') + i) for i in range(size)]
    print('   ' + ' '.join(col_labels))

    for row_index, row in enumerate(grid):
        print(f'{row_index + 1:2} ', end = '')

        for cell in row:
            if cell.is_mine:
                print('*', end = ' ')
            else:
                print('.', end = ' ')
        print()
