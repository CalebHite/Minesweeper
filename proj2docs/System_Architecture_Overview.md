# Project 2 Minesweeper System Architecture Overview

Course: EECS 581 Software Engineering II, Fall 2026

Overview

This document describes the architecture for the updated Minesweeper project. The project keeps the original 10x10 Minesweeper game and adds three AI levels.

These are logical names. Match them to the actual file or class names before submitting.

Components

| Component      | Purpose                                                                        |
| -------------- | ------------------------------------------------------------------------------ |
| User Interface | Shows the board, status, mine count, and AI controls.                          |
| Game Logic     | Handles uncovering, flagging, zero expansion, win checking, and loss checking. |
| Board State    | Stores cells, mines, flags, clue numbers, and current game status.             |
| AI Solver      | Chooses a move based on Easy, Medium, or Hard difficulty.                      |

Architecture Diagram

```text
User Interface
      |
      v
Game Logic <----> AI Solver
      |
      v
Board State

Game Logic sends the updated board back to the User Interface.
```

Data Flow

Player input goes from the user interface to the game logic. The game logic updates the board state, checks for a win or loss, and sends the updated board back to the user interface.

AI moves use the visible board state. The AI solver chooses either a flag or uncover action. The game logic applies that action the same way it applies a normal player move.

AI Requirements

Easy AI uncovers a random covered, unflagged cell.

Medium AI uses basic Minesweeper rules. If a revealed number already has the correct number of flagged neighbors, the remaining covered neighbors are safe. If the number of covered neighbors equals the number of mines still needed around that clue, those covered cells are flagged. If no rule works, it makes a random move.

Hard AI uses the Medium rules and also checks for a valid 1-2-1 pattern in a row or column. When the pattern is valid, it flags the two outside hidden cells and uncovers the middle hidden cell. If no rule works, it makes a random move.

Key Data Structures

| Structure  | Data Stored                                                      |
| ---------- | ---------------------------------------------------------------- |
| Board      | 10x10 grid of cells.                                             |
| Cell       | Mine, revealed, flagged, and adjacent mine count.                |
| Game State | Mines, flags, status, and AI difficulty.                         |
| Action     | Action type and row/column location. |
