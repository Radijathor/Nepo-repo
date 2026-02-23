#!/usr/bin/env python3
"""Simple Blackjack game with a Tkinter UI."""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_VALUES = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def value(self) -> int:
        return CARD_VALUES[self.rank]

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self) -> None:
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise RuntimeError("Deck is empty")
        return self.cards.pop()


def hand_value(hand: list[Card]) -> int:
    total = sum(card.value() for card in hand)
    aces = sum(1 for card in hand if card.rank == "A")

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


class BlackjackApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("560x380")
        self.root.configure(bg="#0f5132")

        self.deck: Deck
        self.player_hand: list[Card]
        self.dealer_hand: list[Card]
        self.round_over = False

        title = tk.Label(
            root,
            text="BLACKJACK",
            bg="#0f5132",
            fg="white",
            font=("Arial", 22, "bold"),
        )
        title.pack(pady=(12, 4))

        self.dealer_label = tk.Label(
            root,
            text="",
            bg="#0f5132",
            fg="#ffefb0",
            font=("Consolas", 14),
            justify="left",
        )
        self.dealer_label.pack(pady=8)

        self.player_label = tk.Label(
            root,
            text="",
            bg="#0f5132",
            fg="#d2f4ff",
            font=("Consolas", 14),
            justify="left",
        )
        self.player_label.pack(pady=8)

        self.result_label = tk.Label(
            root,
            text="",
            bg="#0f5132",
            fg="white",
            font=("Arial", 14, "bold"),
        )
        self.result_label.pack(pady=12)

        button_frame = tk.Frame(root, bg="#0f5132")
        button_frame.pack(pady=10)

        self.hit_button = tk.Button(
            button_frame,
            text="Hit",
            width=12,
            font=("Arial", 11, "bold"),
            bg="#1e90ff",
            fg="white",
            command=self.hit,
        )
        self.hit_button.grid(row=0, column=0, padx=8)

        self.stand_button = tk.Button(
            button_frame,
            text="Stand",
            width=12,
            font=("Arial", 11, "bold"),
            bg="#6c757d",
            fg="white",
            command=self.stand,
        )
        self.stand_button.grid(row=0, column=1, padx=8)

        self.new_round_button = tk.Button(
            button_frame,
            text="New Round",
            width=12,
            font=("Arial", 11, "bold"),
            bg="#28a745",
            fg="white",
            command=self.new_round,
        )
        self.new_round_button.grid(row=0, column=2, padx=8)

        self.new_round()

    def hand_text(self, hand: list[Card]) -> str:
        return "  ".join(str(card) for card in hand)

    def update_view(self, reveal_dealer: bool = False) -> None:
        if reveal_dealer:
            dealer_cards = self.hand_text(self.dealer_hand)
            dealer_value = hand_value(self.dealer_hand)
            dealer_text = f"Dealer: {dealer_cards}   (value: {dealer_value})"
        else:
            dealer_text = f"Dealer: {self.dealer_hand[0]}  [?]"

        player_cards = self.hand_text(self.player_hand)
        player_value = hand_value(self.player_hand)
        player_text = f"Player: {player_cards}   (value: {player_value})"

        self.dealer_label.config(text=dealer_text)
        self.player_label.config(text=player_text)

    def set_round_over(self) -> None:
        self.round_over = True
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

    def new_round(self) -> None:
        self.deck = Deck()
        self.player_hand = [self.deck.draw(), self.deck.draw()]
        self.dealer_hand = [self.deck.draw(), self.deck.draw()]
        self.round_over = False

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

        self.result_label.config(text="Your move: Hit or Stand?")
        self.update_view(reveal_dealer=False)

        if hand_value(self.player_hand) == 21:
            self.stand()

    def hit(self) -> None:
        if self.round_over:
            return

        self.player_hand.append(self.deck.draw())
        self.update_view(reveal_dealer=False)
        total = hand_value(self.player_hand)

        if total > 21:
            self.result_label.config(text="You busted! Dealer wins.")
            self.update_view(reveal_dealer=True)
            self.set_round_over()
        elif total == 21:
            self.stand()

    def stand(self) -> None:
        if self.round_over:
            return

        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw())

        player_total = hand_value(self.player_hand)
        dealer_total = hand_value(self.dealer_hand)

        if dealer_total > 21:
            message = "Dealer busted! You win!"
        elif dealer_total > player_total:
            message = "Dealer wins."
        elif dealer_total < player_total:
            message = "You win!"
        else:
            message = "Push (tie)."

        self.result_label.config(text=message)
        self.update_view(reveal_dealer=True)
        self.set_round_over()


def main() -> None:
    root = tk.Tk()
    BlackjackApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
