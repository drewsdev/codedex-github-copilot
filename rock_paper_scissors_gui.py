#!/usr/bin/env python3
"""Simple Tkinter GUI for Rock Paper Scissors.

Uses game logic from rock_paper_scissors.py (imports `BEATS` and `decide_winner`).
"""

import random
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

from rock_paper_scissors import BEATS, decide_winner


class RPSGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors")

        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.HIGHSCORES_FILE = "highscores.json"
        self.MAX_HIGH_SCORES = 10

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack()

        tk.Label(frame, text="Choose your move:", font=(None, 12)).grid(row=0, column=0, columnspan=3)

        btn_rock = tk.Button(frame, text="Rock", width=10, command=lambda: self.play('rock'))
        btn_paper = tk.Button(frame, text="Paper", width=10, command=lambda: self.play('paper'))
        btn_scissors = tk.Button(frame, text="Scissors", width=10, command=lambda: self.play('scissors'))

        btn_rock.grid(row=1, column=0, padx=4, pady=8)
        btn_paper.grid(row=1, column=1, padx=4, pady=8)
        btn_scissors.grid(row=1, column=2, padx=4, pady=8)

        self.result_label = tk.Label(frame, text="Make a move to start.", font=(None, 11))
        self.result_label.grid(row=2, column=0, columnspan=3, pady=(6, 0))

        self.computer_label = tk.Label(frame, text="Computer chose: -")
        self.computer_label.grid(row=3, column=0, columnspan=3)

        self.score_label = tk.Label(frame, text=self._score_text())
        self.score_label.grid(row=4, column=0, columnspan=3, pady=(6, 0))

        btn_save = tk.Button(frame, text="Save Score", width=12, command=self._on_save_score)
        btn_high = tk.Button(frame, text="High Scores", width=12, command=self.show_high_scores)
        btn_quit = tk.Button(frame, text="Quit", command=self.root.quit)

        btn_save.grid(row=5, column=0, padx=4, pady=(10, 0))
        btn_high.grid(row=5, column=1, padx=4, pady=(10, 0))
        btn_quit.grid(row=5, column=2, padx=4, pady=(10, 0))

    def _score_text(self):
        return f"Score -> You: {self.player_score}  Computer: {self.computer_score}  Ties: {self.ties}"

    def play(self, player_choice: str):
        computer = random.choice(list(BEATS.keys()))
        result = decide_winner(player_choice, computer)

        self.computer_label.config(text=f"Computer chose: {computer}")

        if result == 'tie':
            self.ties += 1
            self.result_label.config(text=f"It's a tie. Both chose {player_choice}.")
        elif result == 'player':
            self.player_score += 1
            self.result_label.config(text=f"You win this round! {player_choice} beats {computer}.")
        else:
            self.computer_score += 1
            self.result_label.config(text=f"Computer wins this round. {computer} beats {player_choice}.")

        self.score_label.config(text=self._score_text())

    # High scores persistence
    def _load_high_scores(self):
        if not os.path.exists(self.HIGHSCORES_FILE):
            return []
        try:
            with open(self.HIGHSCORES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_high_scores(self, scores):
        try:
            with open(self.HIGHSCORES_FILE, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except Exception:
            messagebox.showerror("Error", "Unable to save high scores.")

    def add_high_score(self, name: str, score: int):
        scores = self._load_high_scores()
        entry = {"name": name, "score": score, "date": datetime.utcnow().isoformat()}
        scores.append(entry)
        # sort descending by score
        scores.sort(key=lambda e: e.get("score", 0), reverse=True)
        scores = scores[: self.MAX_HIGH_SCORES]
        self._save_high_scores(scores)

    def show_high_scores(self):
        scores = self._load_high_scores()
        win = tk.Toplevel(self.root)
        win.title("High Scores")
        win.transient(self.root)
        win.resizable(False, False)

        if not scores:
            tk.Label(win, text="No high scores yet.", padx=12, pady=12).pack()
            return

        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack()

        tk.Label(frame, text="Rank", width=6, anchor="w", font=(None, 10, "bold")).grid(row=0, column=0)
        tk.Label(frame, text="Name", width=20, anchor="w", font=(None, 10, "bold")).grid(row=0, column=1)
        tk.Label(frame, text="Score", width=8, anchor="w", font=(None, 10, "bold")).grid(row=0, column=2)
        tk.Label(frame, text="Date (UTC)", width=24, anchor="w", font=(None, 10, "bold")).grid(row=0, column=3)

        for i, e in enumerate(scores, start=1):
            name = e.get("name", "<unknown>")
            score = e.get("score", 0)
            date = e.get("date", "")
            tk.Label(frame, text=f"{i}.", anchor="w").grid(row=i, column=0, sticky="w")
            tk.Label(frame, text=name, anchor="w", width=20).grid(row=i, column=1, sticky="w")
            tk.Label(frame, text=str(score), anchor="w", width=8).grid(row=i, column=2, sticky="w")
            tk.Label(frame, text=date.split("T")[0] if date else "", anchor="w", width=24).grid(row=i, column=3, sticky="w")

    def _on_save_score(self):
        if self.player_score <= 0:
            if not messagebox.askyesno("Confirm", "Your score is zero. Save anyway?"):
                return
        name = simpledialog.askstring("Save Score", "Enter your name:", parent=self.root)
        if not name:
            return
        self.add_high_score(name.strip(), self.player_score)
        messagebox.showinfo("Saved", "Score saved to high scores.")

    def run(self):
        self.root.mainloop()


def main():
    app = RPSGUI()
    app.run()


if __name__ == '__main__':
    main()
