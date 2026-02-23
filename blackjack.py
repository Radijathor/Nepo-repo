#!/usr/bin/env python3
"""Simple terminal blackjack game."""

from __future__ import annotations

import random
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


def hand_to_string(hand: list[Card]) -> str:
    return ", ".join(str(card) for card in hand)


def show_hands(player: list[Card], dealer: list[Card], hide_dealer: bool = True) -> None:
    print("\n--- Table ---")
    if hide_dealer:
        print(f"Dealer: {dealer[0]}, [hidden]")
    else:
        print(f"Dealer: {hand_to_string(dealer)} (value: {hand_value(dealer)})")
    print(f"Player: {hand_to_string(player)} (value: {hand_value(player)})")


def ask_yes_no(prompt: str) -> bool:
    while True:
        choice = input(prompt).strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Please type 'y' or 'n'.")


def play_round() -> None:
    deck = Deck()
    player = [deck.draw(), deck.draw()]
    dealer = [deck.draw(), deck.draw()]

    show_hands(player, dealer, hide_dealer=True)

    if hand_value(player) == 21:
        print("Blackjack! Let's reveal the dealer hand.")
    else:
        while hand_value(player) < 21:
            if ask_yes_no("Hit? (y/n): "):
                player.append(deck.draw())
                show_hands(player, dealer, hide_dealer=True)
            else:
                break

    player_total = hand_value(player)
    if player_total > 21:
        print("\nYou busted. Dealer wins.")
        return

    print("\nDealer's turn...")
    show_hands(player, dealer, hide_dealer=False)
    while hand_value(dealer) < 17:
        dealer.append(deck.draw())
        print("Dealer hits.")
        show_hands(player, dealer, hide_dealer=False)

    dealer_total = hand_value(dealer)
    player_total = hand_value(player)

    print("\n--- Result ---")
    if dealer_total > 21:
        print("Dealer busted. You win!")
    elif dealer_total > player_total:
        print("Dealer wins.")
    elif dealer_total < player_total:
        print("You win!")
    else:
        print("Push (tie).")


def main() -> None:
    print("Welcome to Blackjack!")
    while True:
        play_round()
        if not ask_yes_no("\nPlay again? (y/n): "):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
