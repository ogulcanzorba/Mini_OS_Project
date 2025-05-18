# utils.py

import time
from datetime import datetime
from colorama import Fore

def print_boxed_message(message):
    print("\n" + "+" + "-"*(len(message)+4) + "+")
    print(f"|  {message}  |")
    print("+" + "-"*(len(message)+4) + "+\n")

def sleep_with_countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.YELLOW}Starting in {i}...", end="\r")
        time.sleep(1)
    print(" " * 30, end="\r")  # Clear line after countdown

def validate_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print(Fore.RED + f"Value must be between {min_val} and {max_val}.")
                continue
            return value
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid integer.")

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    with open("logs.txt", "a") as log_file:
        log_file.write(line + "\n")
    return timestamp

def print_progress_bar(current, total, prefix="", suffix="", length=30):
    percent = int(100 * (current / float(total)))
    filled_len = int(length * current // total)
    bar = '█' * filled_len + '-' * (length - filled_len)
    print(f"{prefix} |{bar}| {percent}% {suffix}")

def play_sound_effect(text="🎵 Sound played!"):
    print(Fore.LIGHTBLUE_EX + f"[Sound Effect] {text}")
