from process_management import Scheduler, PCB
from memory_management import MemoryManager
from file_system import FileSystem
from bonus_features import (
    show_ascii_title,
    show_loading_animation,
    display_memory_map,
    play_startup_sound,
    log_and_display_event
)
from utils import print_boxed_message
from colorama import init, Fore, Style

def run_ui(scheduler):
    games = ["Snake", "Tetris", "Pong"]
    while True:
        print(Fore.CYAN + "\nMini Game Console OS" + Style.RESET_ALL)
        print("1. Launch Game")
        print("2. View Queue")
        print("3. View High Scores")
        print("4. Run Scheduler")
        print("5. View Memory Map")
        print("6. Exit")

        choice = input(Fore.YELLOW + "Enter choice (1-6): " + Style.RESET_ALL)
        if choice == "1":
            print(Fore.GREEN + "Available games: " + ", ".join(games) + Style.RESET_ALL)
            game_name = input("Enter game name: ").lower().capitalize()
            if game_name in games:
                try:
                    burst_time = int(input("Enter burst time (seconds): "))
                    scheduler.add_process(game_name, burst_time)
                    log_and_display_event(f"Game '{game_name}' added with burst time {burst_time}.")
                except ValueError:
                    print(Fore.RED + "Invalid burst time" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid game name" + Style.RESET_ALL)
        elif choice == "2":
            scheduler.show_queue()
        elif choice == "3":
            print_boxed_message("HIGH SCORES")
            for game, score in scheduler.file_system.high_scores.items():
                print(f"{game}: {score}")
        elif choice == "4":
            print(Fore.MAGENTA + "\nRunning scheduler..." + Style.RESET_ALL)
            show_loading_animation()
            scheduler.run()
        elif choice == "5":
            display_memory_map(scheduler.memory_manager)
        elif choice == "6":
            print(Fore.CYAN + "Exiting Mini Game Console OS..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice" + Style.RESET_ALL)

if __name__ == "__main__":
    init(autoreset=True)  # Initialize colorama
    show_ascii_title()
    play_startup_sound()
    memory_manager = MemoryManager(total_pages=16, page_size=1024)
    file_system = FileSystem()
    scheduler = Scheduler(time_quantum=2, memory_manager=memory_manager, file_system=file_system)
    run_ui(scheduler)
