# Custom Feature: Limited Hint System (UML)

The hint system lets the player request help for one hidden cell per hint. Each game starts with **3 hints**. A hint flags the cell if it contains a mine; otherwise it uncovers the cell safely.

## Class Diagram

```mermaid
classDiagram
    direction TB

    class Cell {
        +bool is_mine
        +bool is_uncovered
        +bool is_flagged
        +int adjacent_mines
    }

    class main {
        +run game loop
        -hints_remaining: int
    }

    class player_input {
        +get_player_input(grid, uncover_action, flag_action, hints_remaining) int
        +show_mines(grid)
    }

    class game_logic {
        +MAX_HINTS: int = 3
        +hint_cell(grid, row, col, uncover_action, flag_action) bool
        +flag_cell(grid, row, col)
        +create_first_move_handler() function
        +uncover_cell(grid, row, col)
    }

    class board {
        +create_grid(size) list
    }

    main --> board : create_grid
    main --> game_logic : MAX_HINTS, game rules
    main --> player_input : parse commands
    player_input --> game_logic : hint_cell, flag_cell
    game_logic ..> Cell : reads and updates cell state
    board ..> Cell : creates grid of cells
```

## Sequence Diagram (successful hint)

```mermaid
sequenceDiagram
    actor Player
    participant Main
    participant PlayerInput as player_input
    participant GameLogic as game_logic
    participant Cell

    Player->>Main: play turn
    Main->>PlayerInput: get_player_input(..., hints_remaining)
    PlayerInput->>Player: prompt (shows hints remaining)
    Player->>PlayerInput: "B3, Hint"
    PlayerInput->>PlayerInput: parse row, col
    alt hints_remaining > 0
        PlayerInput->>GameLogic: hint_cell(grid, row, col, ...)
        GameLogic->>Cell: read is_mine, is_uncovered, is_flagged
        alt cell is mine
            GameLogic->>GameLogic: flag_cell(grid, row, col)
        else cell is safe
            GameLogic->>GameLogic: uncover_action(grid, row, col)
        end
        GameLogic-->>PlayerInput: True
        PlayerInput->>PlayerInput: hints_remaining -= 1
    else no hints left
        PlayerInput->>Player: "No hints remaining."
    end
    PlayerInput-->>Main: hints_remaining
```

## Use Case (summary)

| Actor | Use case | Precondition | Postcondition |
| --- | --- | --- | --- |
| Player | Request hint on cell | Game in progress; cell hidden and not flagged; hints remaining > 0 | One hint consumed; cell flagged (mine) or uncovered (safe) |
| Player | Request hint with none left | hints remaining = 0 | Message shown; board unchanged |
