#!/usr/bin/env python3
"""Simple Tkinter GUI for Rock Paper Scissors.

Uses game logic from rock_paper_scissors.py (imports `BEATS` and `decide_winner`).
"""

import random
import tkinter as tk

from rock_paper_scissors import BEATS, decide_winner


class RPSGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors")

        self.player_score = 0
        self.computer_score = 0

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

        btn_quit = tk.Button(frame, text="Quit", command=self.root.quit)
        btn_quit.grid(row=5, column=0, columnspan=3, pady=(10, 0))

    def _score_text(self):
        return f"Score -> You: {self.player_score}  Computer: {self.computer_score}"

    def play(self, player_choice: str):
        computer = random.choice(list(BEATS.keys()))
        result = decide_winner(player_choice, computer)

        self.computer_label.config(text=f"Computer chose: {computer}")

        if result == 'tie':
            self.result_label.config(text=f"It's a tie. Both chose {player_choice}.")
        elif result == 'player':
            self.player_score += 1
            self.result_label.config(text=f"You win this round! {player_choice} beats {computer}.")
        else:
            self.computer_score += 1
            self.result_label.config(text=f"Computer wins this round. {computer} beats {player_choice}.")

        self.score_label.config(text=self._score_text())

    def run(self):
        self.root.mainloop()


def main():
    app = RPSGUI()
    app.run()


if __name__ == '__main__':
    main()
