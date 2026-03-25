# Mini Game Hub

#### A secure,password protected multi-user game hub built using **Bash**, **Python**, and **Pygame**, where two authenticated players can choose from multiple board games, play via a GUI, and track results on a leaderboard.

## Contributors
- Ritwik Khandelwal
- Shreyas Lohiya

## ⚙️ System Design
### Week 1 : Designed main.sh
- Easy to use interface with option for each player to login/signup
- Passwords stored securely using SHA-256 hashing
- Elegant looking User Screen enchanced using ASCII and Art Colored text for better UX
- Proper user login avoiding duplicate users

## 👥 User System
### Signup & login functionality
#### Username validation:

- 4–12 characters
- Starts with letter
- Alphanumeric + underscore <br>


#### Password validation:

- 8–20 characters
- Must include uppercase, lowercase, digit, special character
- Passwords stored securely using SHA-256 hashing

## 📂 File Structure

```bash
Mini-Game-Hub/
│
├── main.sh
├── game.py
├── leaderboard.sh
├── games/
│   ├── tictactoe.py
│   ├── othello.py
│   └── connect4.py
├── users.tsv
├── history.csv
└── README.md
```
## Implementation Plan
### Week 1 — Design, Planning & Authentication (March 25 – March 31)
The README will be finalised and committed. The repository will be scaffolded and main.sh will be committed with the full authentication system in place. By end of week, two players will be able to sign up or log in and reach the game handoff point.

### Week 2 — Game Engine Skeleton & First Two Games (April 1 – April 7)
game.py will be built to receive both usernames as arguments and display a game selection menu. The first two fully playable turn-based games will be implemented, each with turn order, move validation, win/draw detection, and clear board rendering in the terminal. By end of week the full flow from login to playing a game will work end to end.

### Week 3 — Remaining Two Games (April 8 – April 14)
The third and fourth games will be implemented to the same standard as Week 2 — turn order, move validation, win/draw detection, and clean board display. The game selection menu will be refined to handle all four options cleanly and ensure smooth navigation between games.

### Week 4 — Leaderboard, Polish, Testing & Submission (April 15 – April 21)
Leaderboard and statistics for the games will be implemented. All authentication edge cases and game logic across all four games will be thoroughly tested. Final Submission will be processed and refined.
