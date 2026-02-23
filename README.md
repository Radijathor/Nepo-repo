# Blackjack in C++

A simple terminal Blackjack game written in modern C++.

## Build and run (Linux/macOS)

```bash
g++ -std=c++17 -O2 blackjack.cpp -o blackjack
./blackjack
```

## Build Windows `.exe`

Use MinGW-w64 g++:

```bat
build_exe.bat
```

This generates:

- `blackjack.exe`

## How to play

- You and the dealer each receive 2 cards.
- Dealer shows one card and keeps one hidden until your turn ends.
- Type `y` to **Hit** (take another card), or `n` to **Stand**.
- Dealer draws until reaching at least 17.
- Closest to 21 without going over wins.
- Aces automatically count as 11 or 1 to avoid busting.
