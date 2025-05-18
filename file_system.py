import os
from pathlib import Path

class FileSystem:
    def __init__(self):
        self.games_dir = Path("games")
        self.games_dir.mkdir(exist_ok=True)  # Create games/ directory if it doesn't exist
        self.high_scores_file = self.games_dir / "high_scores.txt"
        self.high_scores = self._load_high_scores()

    def _load_high_scores(self):
        if not self.high_scores_file.exists():
            return {}
        with open(self.high_scores_file, "r") as f:
            high_scores = {}
            for line in f:
                if ":" in line:
                    game, score = line.strip().split(":")
                    high_scores[game] = int(score)
            return high_scores

    def _save_high_scores(self):
        with open(self.high_scores_file, "w") as f:
            for game, score in self.high_scores.items():
                f.write(f"{game}:{score}\n")

    def create_file(self, path, content):
        file_path = self.games_dir / path
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created physical file {file_path}")

    def read_file(self, path):
        file_path = self.games_dir / path
        if file_path.exists():
            with open(file_path, "r") as f:
                return f.read()
        print(f"File {file_path} does not exist")
        return None

    def write_file(self, path, content):
        file_path = self.games_dir / path
        if file_path.exists():
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Wrote to file {file_path}: {content}")
        else:
            print(f"File {file_path} does not exist")

    def delete_file(self, path):
        file_path = self.games_dir / path
        if file_path.exists():
            file_path.unlink()
            print(f"Deleted file {file_path}")
        else:
            print(f"File {file_path} does not exist")

    def save_high_score(self, game_name, score):
        if game_name not in self.high_scores or score > self.high_scores[game_name]:
            self.high_scores[game_name] = score
            self._save_high_scores()
            print(f"Updated high score for {game_name}: {score}")