# Tic-Tac-Toe Game with Pygame

## Description

This is an OOP implementation of the Tic-Tac-Toe game using Python's Pygame library.

### Features
- 2-player gameplay (locally on the same machine).
- Graphical user interface (GUI) built with Pygame.
- Highlights the winning line (horizontal, vertical, or diagonal).
- Includes draw checking mechanism.
- Basic input validation and reset functionality.

## Prerequisites

- Python 3.x (preferably 3.6 or higher)
- Pygame library
- GNU Wget

To install the required libraries, run the following command:

```bash
pip3 install pygame wget
```

### Troubleshooting:

```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try 'pacman -S
    python-xyz', where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Arch-packaged Python package,
    create a virtual environment using 'python -m venv path/to/venv'.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip.
    
    If you wish to install a non-Arch packaged Python application,
    it may be easiest to use 'pipx install xyz', which will manage a
    virtual environment for you. Make sure you have python-pipx
    installed via pacman.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

If you encounter this error, just pass `--break-system-packages` to pip3.
```bash
pip3 install pygame wget --break-system-packages
```

If "pip3" does not work for you, use "pip".

## How to run the game

```bash
git clone https://github.com/Tashar02/tic-tac-toe
cd tic-tac-toe
python3 tictactoe.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
