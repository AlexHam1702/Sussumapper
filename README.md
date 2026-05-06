# **📦 \TicTacTerminal**

**MVP Status:** v0.67

**Group Members:** Noa Thams, Baptiste Lhors, Eleanore Cortes-Sommaro, Alexandre Hamard


## **🎯 Project Overview**

Provide a concise (2-3 sentence) description of what your application does and the specific problem it solves. Why did you build this?

This application is a terminal-based Tic Tac Toe interface. It has multiple gamemodes and changeable difficulty and an IA powered by a Minimax Algorithm.
The goal is to provide the client with a stable, easy to use and fun tic tac toe game with an IA able to simulate next moves.


## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**\
   git clone \[your-repo-link]\
   cd \[project-folder]

2. **Setup Virtual Environment:**\
   python -m venv .venv\
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**\
   pip install -r requirements.txt

4. **Run Application:**\
   python main.py


## **🛠️ Technical Architecture**

This application is designed using **Object-Oriented Programming (OOP)** principles, ensuring a clean separation between game logic and user interaction.

* **main.py**: The entry point of the application. It handles the top-level execution flow, menu navigation, and initializes the game instance.
* **logic/**: Contains the core `TicTacToe` class. This module manages the game state, board validation, and the **Minimax Algorithm**—the decision-making engine that powers the AI.
* **ui/**: Manages the Command Line Interface (CLI). It transforms the internal data structures into a readable grid and handles terminal-based user input/output.
* **utils/**: Utilizes Python's `Enum` and `typing` modules to define shared constants (`Player`, `GameMode`) and provide type safety across the project.

---

## **🧪 Testing & Validation**

To verify the integrity of the game engine and AI performance, follow these steps:

### **Manual Validation (The "Happy Path")**

1. Run the script: `python main.py`.
2. Select **Option 4** to set difficulty to **9** (Perfect Play).
3. Select **Option 1** (Human vs AI).
4. Play a full game. **Validation Criteria:** The AI should either win or force a draw; it should be impossible to beat at this depth.

### **Automated Testing**

If using `pytest`, ensure the following cases pass:

* **Win Conditions:** Verify that 3-in-a-row (horizontal, vertical, and diagonal) triggers a win.
* **Draw Condition:** Verify that a full board with no winner returns a draw.
* **Input Guardrails:** Ensure that entering non-integer values or coordinates outside the 0-2 range does not crash the program.

---

## **📦 Dependencies**

This project is built using the **Python Standard Library** to ensure zero-overhead installation and high portability.

* **enum**: Used to define `Player` types. This prevents "magic number" bugs and makes the code self-documenting.
* **typing**: Implements static type hinting for better developer experience and code maintainability.
* **copy (deepcopy)**: Utilized for the "Winning Sequence" simulation, allowing the AI to test moves on a virtual board without affecting the live game state.
* **math/sys**: Used for handling infinite values in the Minimax algorithm and system-level operations.

---

## **🔮 Future Roadmap (v2.0)**

The next iteration of this project aims to scale the complexity and accessibility:

* **Heuristic Scaling**: Update the `evaluate()` function to support larger boards (e.g., 10x10) where deep Minimax searches become computationally expensive.
* **GUI Implementation**: Integrate `Tkinter` or `Pygame` to move beyond the terminal and provide a modern visual experience.
* **Monte Carlo Tree Search (MCTS)**: Implement MCTS as an alternative AI strategy for more "human-like" playstyles on larger grids.
* **Save/Load System**: Add JSON-based serialization to save ongoing matches and track lifetime player statistics.

__
