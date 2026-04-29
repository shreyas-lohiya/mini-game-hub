# Mini Game Hub

A final project for the CS108 course (Spr 2026).

> A secure,password protected multi-user game hub built using Bash, Python, and Pygame.
> 
> Two authenticated players can choose from multiple board games, and multiple themes, play via a GUI.
> 
> Track results on a leaderboard and also plots graph using Matplotlib.
>
> The system integrates **Bash (authentication & control flow)** with **Pygame (GUI & gameplay)** to provide a seamless multi-user gaming experience.


## Contributors
- Ritwik Khandelwal
- Shreyas Lohiya



## Usage

The mini game hub starts from a single entry-point script `main.sh`. run as
```bash
bash main.sh
```
## Directory Structure

```
mini-game-hub/
|-- main.sh              # Shell entry point
|-- leaderboard.sh       # Terminal leaderboard renderer
|-- game.py              # Python entry point: GameEngine, stat plots
|-- history.csv          # Append-only game result log
|-- users.tsv            # Username and SHA-256 password hash store
|-- games/
|   |-- game_template.py # Abstract base class; owns the main pygame loop
|   |-- tictactoe.py     # 10x10 five-in-a-row Tic-Tac-Toe
|   |-- othello.py       # 8x8 Othello 
|   |-- connect4.py      # 7x7 Connect4 with physics drop animation
|   `-- chainreaction.py # 9x6 Chain Reaction with cascade explosions
|-- ui/
|   |-- button.py        # Hover-animated Button widget
|   |-- menu.py          # Reusable option-menu screen
|   |-- welcome.py       # Welcome splash screen
|   `-- thankyou.py      # Exit / thank-you screen
|-- images/              # Background PNGs per theme; X/O/board token images; jpegs for report
|-- audio/               # .ogg background music tracks (one per theme)
|-- fonts/               # BlackgothRegular.otf display font
|-- Makefile             # Makefile for pdflatex
|-- report.tex           # Latex report code
`-- report.pdf           # Latex report pdf
```
