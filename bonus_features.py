# bonus_features.py

import time
from datetime import datetime
from colorama import init, Fore, Style
from utils import print_boxed_message, sleep_with_countdown, log_event, print_progress_bar, play_sound_effect

init(autoreset=True)

def show_ascii_title():
    title = """
                                                    
 _____ _     _    _____                  _____ _____ 
|     |_|___|_|  |   __|___ _____ ___   |     |   __|
| | | | |   | |  |  |  | .'|     | -_|  |  |  |__   |
|_|_|_|_|_|_|_|  |_____|__,|_|_|_|___|  |_____|_____|
                                                     
    """
    print(Fore.CYAN + title)

def play_startup_sound():
    play_sound_effect("🎵 Beep-boop! Console is ready.")

def show_loading_animation():
    print(Fore.YELLOW + "Loading Game", end="", flush=True)
    for _ in range(5):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(" Done!")

def log_and_display_event(message):
    timestamp = log_event(message)
    print(Fore.MAGENTA + f"[{timestamp}] {message}")

def display_memory_map(memory_manager):
    used = sum(1 for _ in range(memory_manager.total_pages) if _ not in memory_manager.free_pages)
    print_boxed_message("Memory Map")
    print_progress_bar(used, memory_manager.total_pages, prefix="Used Memory:", suffix="pages")
    print(f"{Fore.GREEN}Free Pages: {memory_manager.free_pages}")
