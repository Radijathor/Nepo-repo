#include <algorithm>
#include <iostream>
#include <random>
#include <string>
#include <vector>

struct Card {
    std::string rank;
    std::string suit;

    int value() const {
        if (rank == "A") return 11;
        if (rank == "K" || rank == "Q" || rank == "J" || rank == "10") return 10;
        return std::stoi(rank);
    }

    std::string to_string() const { return rank + suit; }
};

class Deck {
  public:
    Deck() {
        const std::vector<std::string> suits = {"\u2660", "\u2665", "\u2666", "\u2663"};
        const std::vector<std::string> ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};

        for (const auto &suit : suits) {
            for (const auto &rank : ranks) {
                cards.push_back(Card{rank, suit});
            }
        }

        std::random_device rd;
        std::mt19937 gen(rd());
        std::shuffle(cards.begin(), cards.end(), gen);
    }

    Card draw() {
        Card card = cards.back();
        cards.pop_back();
        return card;
    }

  private:
    std::vector<Card> cards;
};

int hand_value(const std::vector<Card> &hand) {
    int total = 0;
    int aces = 0;

    for (const auto &card : hand) {
        total += card.value();
        if (card.rank == "A") ++aces;
    }

    while (total > 21 && aces > 0) {
        total -= 10;
        --aces;
    }

    return total;
}

std::string hand_to_text(const std::vector<Card> &hand) {
    std::string out;
    for (size_t i = 0; i < hand.size(); ++i) {
        out += hand[i].to_string();
        if (i + 1 < hand.size()) out += ", ";
    }
    return out;
}

void show_hands(const std::vector<Card> &player, const std::vector<Card> &dealer, bool hide_dealer) {
    std::cout << "\n=== TABLE ===\n";
    if (hide_dealer) {
        std::cout << "Dealer: " << dealer.front().to_string() << ", [hidden]\n";
    } else {
        std::cout << "Dealer: " << hand_to_text(dealer) << " (" << hand_value(dealer) << ")\n";
    }
    std::cout << "Player: " << hand_to_text(player) << " (" << hand_value(player) << ")\n";
}

bool ask_yes_no(const std::string &prompt) {
    while (true) {
        std::cout << prompt;
        std::string choice;
        if (!std::getline(std::cin, choice)) return false;

        for (auto &ch : choice) ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
        if (choice == "y" || choice == "yes") return true;
        if (choice == "n" || choice == "no") return false;

        std::cout << "Please type y/yes or n/no.\n";
    }
}

void play_round() {
    Deck deck;
    std::vector<Card> player{deck.draw(), deck.draw()};
    std::vector<Card> dealer{deck.draw(), deck.draw()};

    show_hands(player, dealer, true);

    while (hand_value(player) < 21) {
        if (!ask_yes_no("Hit? (y/n): ")) break;
        player.push_back(deck.draw());
        show_hands(player, dealer, true);
    }

    int player_total = hand_value(player);
    if (player_total > 21) {
        std::cout << "\nYou busted. Dealer wins.\n";
        return;
    }

    std::cout << "\nDealer's turn...\n";
    show_hands(player, dealer, false);

    while (hand_value(dealer) < 17) {
        dealer.push_back(deck.draw());
        std::cout << "Dealer hits.\n";
        show_hands(player, dealer, false);
    }

    int dealer_total = hand_value(dealer);

    std::cout << "\n=== RESULT ===\n";
    if (dealer_total > 21) {
        std::cout << "Dealer busted. You win!\n";
    } else if (player_total > dealer_total) {
        std::cout << "You win!\n";
    } else if (player_total < dealer_total) {
        std::cout << "Dealer wins.\n";
    } else {
        std::cout << "Push (tie).\n";
    }
}

int main() {
    std::cout << "Welcome to Blackjack (C++)!\n";

    do {
        play_round();
    } while (ask_yes_no("\nPlay again? (y/n): "));

    std::cout << "Thanks for playing!\n";
    return 0;
}
