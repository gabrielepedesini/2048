# 2048

A simple terminal implementation of the 2048 game.

## Structure

- `main.py` - game's main script.
- `dist/` - folder for platform-specific executables. 

## Compile and Run

To compile and run the project:

1. If you are on *macOS* or *Linux* you are ready to go, instead if you are on **Windows** you will need `windows-curses` for curses support:
    ```bash
    pip install windows-curses
    ```

2. Run from source
    ```bash
    python main.py
    ```

## Building executables

This project can be packaged using PyInstaller. 

Example commands:

- Windows:
    ```bash
    pyinstaller --onefile main.py --name 2048-windows
    ```
- macOS:
    ```bash
    pyinstaller --onefile main.py --name 2048-macos
    ```

- Linux:
    ```bash
    pyinstaller --onefile main.py --name 2048-linux
    ```

Place the generated binary in the correct folder into `dist/`.