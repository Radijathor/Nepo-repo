# Blackjack (Simple Visuals)

A simple Blackjack game built with Python + Tkinter (desktop GUI).

## Run locally

```bash
python3 blackjack.py
```

## How to play

- Click **Hit** to draw a card.
- Click **Stand** to end your turn and let the dealer play.
- Dealer draws until value is at least 17.
- Closest to 21 without busting wins.
- Click **New Round** to start again.

## Build a Windows `.exe`

On Windows, run:

```bat
build_exe.bat
```

Or manually:

```bash
python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --onefile --windowed --name blackjack blackjack.py
```

The executable will be generated at:

- `dist/blackjack.exe`
