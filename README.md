Mini Game Console OS
Overview
The Mini Game Console OS is a Python-based operating system simulation designed to emulate a retro game console running classic games like Snake, Tetris, and Pong. It implements core OS concepts—process management, memory management, concurrency, and file systems—while incorporating creative bonus features to enhance user interaction and visualization. Built as a modular, multi-file project, it showcases an AI-based scheduler, paging-based memory allocation, threaded input processing, and real file I/O for game saves and logs, all wrapped in a retro-themed terminal UI.
Features

Process Management: AI-based Round Robin scheduler prioritizing less-played games (based on total runtime).
Memory Management: Paging system with 16 pages (1024 bytes each), supporting allocation and address translation.
Concurrency: Producer-Consumer threading model for game inputs (e.g., "up", "down") and score updates.
File System: Real file operations in a games/ directory, storing scores (e.g., snake.txt), high scores (high_scores.txt), and event logs (log.txt).
Retro Terminal UI:
ASCII art title and logo for a nostalgic console feel.
Colored menu (using colorama) with boxed messages.
Loading animations and countdown timers for game launches.

Visualizations:
ASCII queue display (e.g., [ Snake | Tetris ]).
Memory map with progress bar and allocated pages (e.g., [████----]).

Event Logger: Logs process events (e.g., start, termination) to games/log.txt with timestamps.
Sound Effects: Simulated retro sounds (e.g., "🎵 Key press!") printed for key events.

Prerequisites

Python 3.6+: Ensure Python is installed.
Colorama (Optional): For colored terminal output.pip install colorama

If not installed, the program falls back to plain text output.

Installation

Clone or download the project to a local directory:git clone <repository-url>
cd Mini_OS_Simulation

(Optional) Install colorama for enhanced visuals:pip install colorama

Ensure all project files are in the same directory (see Project Structure).

Running the Program

Navigate to the project directory:cd Mini_OS_Simulation

Run the main script:python main.py

Interact with the terminal UI:
Launch Game: Add a game process (e.g., Snake) with a specified burst time (1–20 seconds).
View Queue: See the current process queue in ASCII format.
View High Scores: Display high scores from games/high_scores.txt.
View Memory Map: Show allocated/free memory pages.
View Event Log: Read event logs from games/log.txt.
Run Scheduler: Execute the scheduler to simulate game processes.
Exit: Close the program.

Project Structure

main.py: Entry point, runs the retro UI and initializes components.
process_management.py: Defines PCB (Process Control Block) and Scheduler for process management and AI-based scheduling.
memory_management.py: Implements MemoryManager for paging and address translation.
concurrency.py: Contains GameThreadManager for Producer-Consumer threading.
file_system.py: Manages real file operations (create, read, write, delete) in the games/ directory.
bonus_features.py: Handles retro UI, memory map, progress bar, and loading animations.
utils.py: Utility functions for event logging, sound effects, input validation, and boxed messages.
README.md: Project documentation.
games/: Runtime directory for game files (e.g., snake.txt, log.txt).

Example Usage
python main.py

Sample Interaction:

---

| |\_|**_|_| | **|**\_ \_\_\_** **\_ | | **|
| | | | | | | | | | .'| | -_| | | |\_\_ |
|_|_|_|_|_|_|_| |**\_**|**,|_|_|_|_**| |**\_**|**\_**|

[Sound Effect] 🎵 Beep-boop! Console is ready.

+--------+
| Menu |
+--------+

1. Launch Game
2. View Queue
3. View High Scores
4. View Memory Map
5. View Event Log
6. Run Scheduler
7. Exit
   Enter choice (1-7): 1
   Available games: ['Snake', 'Tetris', 'Pong']
   Enter game name: Snake
   Enter burst time (seconds, 1-20): 6
   Loading Game..... Done!
   Starting in 3...
   Starting in 2...
   Starting in 1...

Created physical file games/snake.txt
[Sound Effect] 🎵 Game loaded!

Challenges Overcome

Circular Imports: Resolved by moving utility functions to utils.py and refactoring dependencies.
Thread Safety: Used locks (score_lock) for concurrent score updates and file writes.
Real File I/O: Implemented consistent file operations in games/ using pathlib.
User Experience: Added retro UI elements, animations, and input validation to enhance interactivity.

License
This project is for educational purposes and not licensed for commercial use.
Acknowledgments
Built with inspiration from retro game consoles.
