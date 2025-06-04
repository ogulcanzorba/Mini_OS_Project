import tkinter as tk
from tkinter import ttk, messagebox
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
import threading
import time
from colorama import init

class GameConsoleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Game Console OS")
        self.root.geometry("600x650")
        self.root.minsize(400, 500)  # Minimum window size
        self.root.configure(bg="#000000")
        self.games = ["Snake", "Tetris", "Pong"]
        init(autoreset=True)
        show_ascii_title()
        play_startup_sound()
        self.memory_manager = MemoryManager(total_pages=16, page_size=1024)
        self.file_system = FileSystem()
        self.scheduler = Scheduler(time_quantum=2, memory_manager=self.memory_manager, file_system=self.file_system, log_callback=self.log_to_gui)
        self.setup_gui()

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("T.Label", background="#000000", foreground="#00FF00", font=("Courier", 12))
        style.configure("T.Button", background="#333333", foreground="#00FF00", font=("Courier", 10))
        style.configure("T.Entry", fieldbackground="#333333", foreground="#00FF00", font=("Courier", 10))
        style.configure("T.Combobox", fieldbackground="#333333", foreground="#00FF00", font=("Courier", 10))

        # Title
        tk.Label(self.root, text="Mini Game Console OS", font=("Courier", 16, "bold"), bg="#000000", fg="#00FF00").pack(pady=10, fill="x")

        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Process Queue Display
        ttk.Label(self.main_frame, text="Process Queue:").pack(anchor="w")
        self.queue_text = tk.Text(self.main_frame, height=2, width=50, font=("Courier", 10), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
        self.queue_text.pack(pady=5, fill="x")
        self.queue_text.config(state="disabled")

        # Memory Map Display
        ttk.Label(self.main_frame, text="Memory Map:").pack(anchor="w")
        self.memory_text = tk.Text(self.main_frame, height=2, width=50, font=("Courier", 10), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
        self.memory_text.pack(pady=5, fill="x")
        self.memory_text.config(state="disabled")

        # High Scores Display
        ttk.Label(self.main_frame, text="High Scores:").pack(anchor="w")
        self.scores_text = tk.Text(self.main_frame, height=4, width=50, font=("Courier", 10), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
        self.scores_text.pack(pady=5, fill="x")
        self.scores_text.config(state="disabled")

        # Scheduler Log Display
        ttk.Label(self.main_frame, text="Scheduler Log:").pack(anchor="w")
        log_frame = ttk.Frame(self.main_frame)
        log_frame.pack(pady=5, fill="both", expand=True)
        self.log_text = tk.Text(log_frame, height=6, width=50, font=("Courier", 10), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
        self.log_text.pack(side="left", fill="both", expand=True)
        self.log_text.config(state="disabled")
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Input Frame for Launching Games
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(pady=10, fill="x")
        ttk.Label(input_frame, text="Select Game:").pack(side="left")
        self.game_combo = ttk.Combobox(input_frame, values=["Select a game"] + self.games, state="readonly", width=15)
        self.game_combo.set("Select a game")
        self.game_combo.pack(side="left", padx=5, fill="x", expand=True)
        ttk.Label(input_frame, text="Burst Time:").pack(side="left")  # Shortened label
        self.burst_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Remove Process Frame
        remove_frame = ttk.Frame(self.main_frame)
        remove_frame.pack(pady=5, fill="x")
        ttk.Label(remove_frame, text="Remove Process:").pack(side="left")
        self.remove_combo = ttk.Combobox(remove_frame, values=["Select a process"], state="readonly", width=15)
        self.remove_combo.set("Select a process")
        self.remove_combo.pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(remove_frame, text="Remove Sel.", command=self.remove_selected_process).pack(side="left", padx=5)  # Shortened button text

        # Buttons Frame with Grid Layout
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10, fill="x")
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)  # Equal column weights
        ttk.Button(button_frame, text="Launch", command=self.launch_game).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(button_frame, text="View Queue", command=self.view_queue).grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(button_frame, text="High Scores", command=self.view_scores).grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(button_frame, text="Scheduler", command=self.run_scheduler).grid(row=0, column=3, padx=5, sticky="ew")
        ttk.Button(button_frame, text="Memory Map", command=self.view_memory).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Clear Queue", command=self.clear_queue).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Remove Last", command=self.remove_last_process).grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Exit", command=self.exit).grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def log_to_gui(self, message):
        self.root.after(0, lambda: self._update_log(message))

    def _update_log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_remove_combo(self):
        process_names = [pcb.name for pcb in self.scheduler.ready_queue]
        self.remove_combo.configure(values=["Select a process"] + process_names)
        self.remove_combo.set("Select a process")

    def launch_game(self):
        game_name = self.game_combo.get()
        burst_time = self.burst_entry.get()
        
        if game_name == "Select a game" or game_name not in self.games:
            messagebox.showerror("Error", f"Please select a valid game: {', '.join(self.games)}")
            return
        
        try:
            burst_time = int(burst_time)
            if burst_time <= 0:
                raise ValueError
            self.scheduler.add_process(game_name, burst_time)
            log_and_display_event(f"Game '{game_name}' added with burst time {burst_time}.")
            self.log_to_gui(f"Game '{game_name}' added with burst time {burst_time}.")
            messagebox.showinfo("Success", f"Game '{game_name}' added to queue!")
            self.view_queue()
            self.update_remove_combo()
        except ValueError:
            messagebox.showerror("Error", "Invalid burst time. Enter a positive integer.")

    def view_queue(self):
        self.queue_text.config(state="normal")
        self.queue_text.delete("1.0", tk.END)
        if not self.scheduler.ready_queue:
            self.queue_text.insert(tk.END, "Ready Queue: Empty")
        else:
            queue_str = "Ready Queue: [" + " | ".join(pcb.name for pcb in self.scheduler.ready_queue) + "]"
            self.queue_text.insert(tk.END, queue_str)
        self.queue_text.config(state="disabled")
        self.update_remove_combo()

    def view_scores(self):
        self.scores_text.config(state="normal")
        self.scores_text.delete("1.0", tk.END)
        if not self.scheduler.file_system.high_scores:
            self.scores_text.insert(tk.END, "No high scores yet.")
        else:
            for game, score in self.scheduler.file_system.high_scores.items():
                self.scores_text.insert(tk.END, f"{game}: {score}\n")
        self.scores_text.config(state="disabled")

    def view_memory(self):
        self.memory_text.config(state="normal")
        self.memory_text.delete("1.0", tk.END)
        used = sum(1 for _ in range(self.memory_manager.total_pages) if _ not in self.memory_manager.free_pages)
        bar = '█' * (used * 30 // self.memory_manager.total_pages) + '-' * ((self.memory_manager.total_pages - used) * 30 // self.memory_manager.total_pages)
        percent = int(100 * (used / self.memory_manager.total_pages))
        memory_str = f"Used Memory: |{bar}| {percent}% pages\nFree Pages: {self.memory_manager.free_pages}"
        self.memory_text.insert(tk.END, memory_str)
        self.memory_text.config(state="disabled")

    def clear_queue(self):
        self.scheduler.clear_queue()
        self.log_to_gui("Cleared entire process queue.")
        messagebox.showinfo("Success", "Process queue cleared!")
        self.view_queue()
        self.view_memory()

    def remove_last_process(self):
        if self.scheduler.remove_last_process():
            self.log_to_gui("Removed last added process.")
            messagebox.showinfo("Success", "Last process removed!")
        else:
            messagebox.showerror("Error", "No processes in queue to remove.")
        self.view_queue()
        self.view_memory()

    def remove_selected_process(self):
        process_name = self.remove_combo.get()
        if process_name == "Select a process" or not self.scheduler.remove_process_by_name(process_name):
            messagebox.showerror("Error", "Please select a valid process to remove.")
        else:
            self.log_to_gui(f"Removed process '{process_name}' from queue.")
            messagebox.showinfo("Success", f"Process '{process_name}' removed!")
        self.view_queue()
        self.view_memory()

    def run_scheduler(self):
        def scheduler_task():
            show_loading_animation()
            self.scheduler.run()
            self.root.after(0, self.view_queue)
            self.root.after(0, self.view_scores)
            self.root.after(0, self.view_memory)
            self.root.after(0, lambda: messagebox.showinfo("Scheduler", "Scheduler run complete!"))
        
        threading.Thread(target=scheduler_task, daemon=True).start()

    def exit(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameConsoleGUI(root)
    root.mainloop()