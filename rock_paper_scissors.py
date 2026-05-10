"""
Create a Rock Paper Scissors game where the player inputs their choice
and plays  against a computer that randomly selects its move, 
with the game showing who won each round.
Add a score counter that tracks player and computer wins, 
and allow the game to continue until the player types “quit”.
"""

import random
import sys

#!/usr/bin/env python3
"""
Rock Paper Scissors game.
Player types rock/paper/scissors (or r/p/s) to play against a random computer move.
Type "quit" or "q" to exit. Tracks and shows scores.
"""


MOVES = {"r": "rock", "p": "paper", "s": "scissors"}
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def normalize_choice(raw: str):
    if not raw:
        return None
    token = raw.strip().lower()
    if token in ("quit", "q"):
        return "quit"
    if token in MOVES:
        return MOVES[token]
    if token in MOVES.values():
        return token
    return None


def decide_winner(player: str, computer: str) -> str:
    if player == computer:
        return "tie"
    return "player" if BEATS[player] == computer else "computer"


def main():
    player_score = 0
    computer_score = 0

    try:
        while True:
            raw = input("Enter rock/paper/scissors (r/p/s) or quit (q): ")
            choice = normalize_choice(raw)
            if choice is None:
                print("Invalid input. Please enter rock, paper, scissors, or quit.")
                continue
            if choice == "quit":
                print(f"Final score -> You: {player_score}  Computer: {computer_score}")
                break

            computer = random.choice(list(BEATS.keys()))
            result = decide_winner(choice, computer)

            if result == "tie":
                print(f"You chose {choice}. Computer chose {computer}. It's a tie.")
            elif result == "player":
                player_score += 1
                print(f"You chose {choice}. Computer chose {computer}. You win this round!")
            else:
                computer_score += 1
                print(f"You chose {choice}. Computer chose {computer}. Computer wins this round.")

            print(f"Score -> You: {player_score}  Computer: {computer_score}\n")
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted.")
        print(f"Final score -> You: {player_score}  Computer: {computer_score}")
        sys.exit(0)


if __name__ == "__main__":
    main()