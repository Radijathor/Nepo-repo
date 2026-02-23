@echo off
REM Build a Windows .exe using PyInstaller
python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --onefile --windowed --name blackjack blackjack.py
echo.
echo Build complete. EXE is in the dist folder.
pause
