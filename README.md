# Conway's Game of Life and Langton's Ant


[![PyPI](https://img.shields.io/pypi/v/rich_life)](https://pypi.org/project/rich_life/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rich_life.svg)](https://pypi.org/project/rich_life/)  
![Runs on Linux | MacOS | Windows](https://img.shields.io/badge/runs%20on-Linux%20%7C%20MacOS%20%7C%20Windows-blue)
![Arch x86-63 | ARM | AppleSilicon](https://img.shields.io/badge/arch-x86--64%20%7C%20ARM%20%7C%20AppleSilicon-blue)  
![PyPI - License](https://img.shields.io/pypi/l/rich_life)

## About
This project implements Conway's Game of Life and Langton's Ant.  
Both are cellular automaton simulations.
Uses Rich for terminal visualization.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/probello3)

## Screenshots
![Game of Life Screenshot](https://raw.githubusercontent.com/paulrobello/rich_life/main/life-screenshot.png)
![Langton's Ant Screenshot](https://raw.githubusercontent.com/paulrobello/rich_life/main/ants-screenshot.png)

## Installation

To install make sure you have Python 3.11 or higher and [uv](https://pypi.org/project/uv/) installed.

### Installation From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/paulrobello/rich_life.git
   cd rich_life
   ```

2. Install the required dependencies:
   ```bash
   uv sync
   ```

### Installation From PyPI

To install from PyPI, run any of the following commands:

```bash
uv tool install rich-life
```

```bash
pipx install rich-life
```

## Usage

### Running if installed from PyPI
```bash
rich_life
```

### Running from source
Run the Game of Life simulation using the following command:

```bash
uv run rich_life
```

You can customize the grid size, number of generations, and neighborhood rules using command-line options:

```bash
uv run rich_life --width 50 --height 30 --generations 300 --rules moore
```

Run the Langton's Ant simulation using the following command:

```bash
uv run rich_life --mode ants
```


Available options:
- `--width` or `-w`: Width of the grid (default: half of console height)
- `--height` or `-h`: Height of the grid (default: half of console height minus 2)
- `--infinite` or `-i`: Enable infinite mode. Simulation grid has no bounds (default: False)
- `--generations` or `-g`: Number of generations to simulate (default: 100)
- `--mode` or `-m`: Simulation mode (options: 'life' or 'ants', default: 'ants')
- `--rules` or `-r`: Neighborhood rules for game of life (options: 'moore' or 'van_neumann', default: 'moore')
- `--offset-x` or `-x`: Bord display X-coordinate offset for infinite mode (default: 0)
- `--offset-y` or `-y`: Bord display Y-coordinate offset for infinite mode (default: 0)
- `--rps` or `-r`: Refresh / generations per second (default: 10)


Keys:
- 'Arrows' / 'WSAD': Pan the grid

## Running Tests

To run the tests, use the following command:

```bash
uv run pytest tests/test_game_of_life.py
```

## What's New

- Version 0.2.0: Better keyboard handling
- Version 0.1.0: Initial release

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Paul Robello (probello@gmail.com)
