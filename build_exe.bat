@echo off
REM Build Windows executable using g++ (MinGW-w64)
REM Ensure g++ is available in PATH

g++ -std=c++17 -O2 -static -s blackjack.cpp -o blackjack.exe
if %errorlevel% neq 0 (
  echo Build failed. Make sure MinGW-w64 g++ is installed and in PATH.
  pause
  exit /b 1
)

echo Build complete: blackjack.exe
pause
