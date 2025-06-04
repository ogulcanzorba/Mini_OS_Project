Mini Game Console OS
Overview
The Mini Game Console OS is a Python-based operating system simulation designed to emulate a retro game console running classic games like Snake, Tetris, and Pong. It implements core OS concepts—process management, memory management, concurrency, and file systems—while incorporating creative bonus features to enhance user interaction and visualization. Built as a modular, multi-file project, it showcases an AI-based scheduler, paging-based memory allocation, threaded input processing, real file I/O for game saves and logs, and a responsive graphical user interface (GUI) with a retro-themed dark design.
Features

Process Management: AI-based Round Robin scheduler prioritizing less-played games (based on total runtime), with options to clear the entire queue, remove the last added process, or remove a selected process.
Memory Management: Paging system with 16 pages (1024 bytes each), supporting allocation and address translation.
Concurrency: Producer-Consumer threading model for game inputs (e.g., "up", "down") and score updates with thread-safe locks.
File System: Real file operations in a games/ directory, storing scores (e.g., snake.txt), high scores (high_scores.txt), and event logs (logs.txt).
Responsive Retro GUI:
Dark theme (black background, green text) with a Courier font for a retro CRT terminal aesthetic.
Displays process queue, memory map, high scores, and scheduler logs in scrollable text areas.
Dropdown for selecting games (Snake, Tetris, Pong) and processes to remove.
Responsive layout that scales with window size, ensuring all buttons (e.g., Launch, Clear Queue) are fully visible.
Buttons for launching games, viewing queue/scores/memory, running the scheduler, clearing the queue, removing processes, and exiting.


Visualizations:
ASCII queue display in GUI (e.g., [ Snake | Tetris ]).
Memory map with a text-based progress bar and free page list.


Event Logger: Logs process events (e.g., start, termination, queue modifications) to games/logs.txt and the GUI log window with timestamps.
Sound Effects: Simulated retro sounds (e.g., "🎵 Beep-boop!") printed for key events.

Prerequisites

Python 3.6+: Ensure Python is installed (includes tkinter for the GUI).
Colorama (Optional): For colored console output during startup.pip install colorama

If not installed, the program falls back to plain text console output.

Installation

Clone or download the project to a local directory:git clone <repository-url>
cd Mini_OS_Simulation


(Optional) Install colorama for enhanced console visuals:pip install colorama


Ensure all project files are in the same directory (see Project Structure).

Running the Program

Navigate to the project directory:cd Mini_OS_Simulation


Run the main script:python main.py


Interact with the GUI:
Launch Game: Select a game from the dropdown (e.g., Snake) and enter a burst time (1–20 seconds).
View Queue: Display the current process queue.
View High Scores: Show high scores from games/high_scores.txt.
View Memory Map: Display memory usage and free pages.
Run Scheduler: Execute the scheduler to simulate game processes.
Clear Queue: Remove all processes from the queue.
Remove Last Process: Remove the most recently added process.
Remove Selected Process: Remove a specific process chosen from a dropdown.
Exit: Close the program.



Project Structure

main.py: Entry point, runs the responsive GUI with queue management.
process_management.py: Defines PCB (Process Control Block) and Scheduler for process management and queue operations.
memory_management.py: Implements MemoryManager for paging and address translation.
concurrency.py: Contains GameThreadManager for Producer-Consumer threading.
file_system.py: Manages real file operations in the games/ directory.
bonus_features.py: Handles console-based ASCII art, animations, and memory visualization.
utils.py: Utility functions for logging, sound effects, input validation, and formatting.
README.md: Project documentation.
games/: Runtime directory for game files (e.g., snake.txt, logs.txt).

Example Usage
python main.py

Sample Interaction

GUI opens with a black background, green text, and a retro Courier font.
Select "Snake" from the game dropdown, enter burst time "6," and click "Launch."
Scheduler log shows: Game 'Snake' added with burst time 6.
Click "Run Scheduler" to see logs like:Running: Snake (PID: 1, State: running, Score: 0)
Address Translation: Virtual address 1500 -> Physical address 1500 (Page 0, Offset 1500)
Snake Producer: Added 'up'
Snake Consumer: Processed 'up', Score: 1


Use "Clear Queue" or "Remove Sel." to manage the queue, with logs updating in the GUI.

Challenges Overcome

Responsive GUI: Designed a scalable layout using grid and pack to ensure all elements (e.g., "Clear Queue" button) are visible in small or large windows.
Queue Management: Added functionality to clear the queue or remove specific processes with proper memory and file cleanup.
Thread Safety: Used locks for concurrent score updates and root.after for GUI-safe logging.
Real File I/O: Implemented consistent file operations using pathlib.
User Experience: Enhanced with a dark-themed, retro GUI, dropdowns for game/process selection, and scrollable logs.

License
This project is for educational purposes and not licensed for commercial use.
Acknowledgments
Built with inspiration from retro game consoles, with a focus on OS principles and user-friendly visualization.
