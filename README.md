# Macro Bot 

A robust, thread-safe task automation tool (Mouse and Keyboard) built with **Python 3**.

## Key Features

* **Precise Recording:** Captures clicks, keystrokes, and timing intervals accurately.
* **Thread-Safe Engine:** Runs on a separate daemon thread to prevent UI freezing.
* **Interactive CLI:** Configure loops, delays, and file management via a command-line interface.
* **Persistence:** Save and load macros using JSON.
* **Panic Switch:** Immediate execution kill-switch using `ESC` for safety.

## Requirements

* Python 3.8+
* **Dependencies:** `pynput`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NahtanDevFS/macro_bot.git
    cd macro_bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install pynput
    ```

## Quick Start

### 1. Launch the Application
* **Windows:** Double-click `start_macro_bot.bat`.
* **Terminal:** Run `python main.py`.

### 2. Global Hotkeys
These shortcuts work globally (even when the window is minimized).

| Key | Function | Description |
| :--- | :--- | :--- |
| **F8** | `RECORD / STOP` | Starts a new recording or stops the current one. |
| **F9** | `PLAY / PAUSE` | Plays the loaded macro or pauses execution. |
| **ESC** | `PANIC SWITCH` | **Immediately stops all threads** and exits the program. |

### 3. Console Commands
Use the interactive terminal to configure the bot when it is idle.

* **Configure Loops:**
    Set repetition count and delay (in seconds) between loops.
    ```text
    # Syntax: config <count> <delay>
    
    config 5 0      # Run 5 times, no delay
    config -1 2.5   # Run INFINITELY, waiting 2.5s between loops
    ```

* **Save Macro:**
    ```text
    save farming_xp  # Creates farming_xp.json
    ```

* **Load Macro:**
    ```text
    load farming_xp  # Loads actions from the file
    ```

* **Check Status:**
    ```text
    status
    ```

## Disclaimer
This software controls your mouse and keyboard.
1. Always keep the ESC key in mind when testing new macros.
2. Use responsibly. Automating actions in certain games or services may violate their Terms of Service.

## License
This project is licensed under the MIT License. Feel free to use or modify this software for any purpose. Contributions and improvements are welcome!
