"""
Conway's Game of Life and Langton's Ant implementation using Rich for terminal visualization.

Author: Paul Robello
Email: probello@gmail.com
"""

import random
from enum import Enum
from time import sleep
from typing import Dict, Tuple, Optional

import typer
from keyboard import on_press
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich import print as rprint

console: Console = Console()

def_size = int(console.height / 2)

app = typer.Typer()


class NeighborhoodRules(str, Enum):
    """
    Enum class representing the neighborhood rules for the Game of Life simulation.
    """

    MOORE = "moore"
    VAN_NEUMANN = "van_neumann"


class SimulationMode(str, Enum):
    """
    Enum class representing the simulation modes.
    """

    LIFE = "life"
    ANTS = "ants"


# pylint: disable=too-many-instance-attributes
class GameOfLife:
    """
    Represents the Game of Life or Langton's Ant simulation.
    """

    def __init__(
        self,
        display_width: int,
        display_height: int,
        infinite_mode: bool = True,
        rules: NeighborhoodRules = NeighborhoodRules.MOORE,
        offset: Optional[Tuple[int, int]] = None,
        mode: SimulationMode = SimulationMode.LIFE,
        refresh_per_second: int = 10,
    ) -> None:
        """
        Initialize the simulation grid.

        Args:
            display_width (int): Width of the grid.
            display_height (int): Height of the grid.
            infinite_mode (bool): Whether the grid is infinite or not.
            rules (NeighborhoodRules): The neighborhood rules to use (for Game of Life).
            offset (Optional[Tuple[int, int]]): Offset for the displayed region. Defaults to (0, 0).
            mode (SimulationMode): The simulation mode (Life or Ants).
        """
        self.display_width: int = display_width
        self.display_height: int = display_height
        self.infinite_mode: bool = infinite_mode
        self.rules: NeighborhoodRules = rules
        self.offset: Tuple[int, int] = offset or (0, 0)
        self.mode: SimulationMode = mode
        self.generation: int = 0
        self.refresh_per_second: int = refresh_per_second

        if self.mode == SimulationMode.LIFE:
            self.grid: Dict[Tuple[int, int], int] = {
                (x + self.offset[0], y + self.offset[1]): random.choice([0, 1])
                for x in range(display_width)
                for y in range(display_height)
                if random.choice([0, 1]) == 1  # Only store living cells
            }
        else:  # Langton's Ant
            self.grid: Dict[Tuple[int, int], int] = {}
            self.ant_position: Tuple[int, int] = (
                display_width // 2 + self.offset[0],
                display_height // 2 + self.offset[1],
            )
            self.ant_direction: int = 0  # 0: North, 1: East, 2: South, 3: West

    def get_neighbors_van_neumann(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell according to the
        "Van Neumann Neighborhood" rules.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            int: Number of live neighbors.
        """
        count: int = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.infinite_mode:
                count += self.grid.get((nx, ny), 0)
            else:
                nx, ny = (nx - self.offset[0]) % self.display_width + self.offset[0], (
                    ny - self.offset[1]
                ) % self.display_height + self.offset[1]
                count += self.grid.get((nx, ny), 0)
        return count

    def get_neighbors_moore(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell according to the
        "Moore Neighborhood" rules.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            int: Number of live neighbors.
        """
        count: int = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.infinite_mode:
                    count += self.grid.get((nx, ny), 0)
                else:
                    nx, ny = (nx - self.offset[0]) % self.display_width + self.offset[
                        0
                    ], (ny - self.offset[1]) % self.display_height + self.offset[1]
                    count += self.grid.get((nx, ny), 0)
        return count

    def get_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell according to the
        "Neighborhood" rules.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            int: Number of live neighbors.
        """
        if self.rules == NeighborhoodRules.VAN_NEUMANN:
            return self.get_neighbors_van_neumann(x, y)
        return self.get_neighbors_moore(x, y)

    def next_generation(self) -> None:
        """
        Compute the next generation of the simulation.
        """
        if self.mode == SimulationMode.LIFE:
            self._next_generation_life()
        else:
            self._next_generation_ant()

    def _next_generation_life(self) -> None:
        """
        Compute the next generation of the Game of Life.
        """
        new_grid: Dict[Tuple[int, int], int] = {}

        # Check all current living cells and their neighbors
        cells_to_check = set(self.grid.keys()) | {
            (x + dx, y + dy)
            for x, y in self.grid
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
        }

        for x, y in cells_to_check:
            neighbors: int = self.get_neighbors(x, y)
            if self.grid.get((x, y), 0) == 1:
                if 2 <= neighbors <= 3:
                    new_grid[(x, y)] = 1
            elif neighbors == 3:
                new_grid[(x, y)] = 1

        self.grid = new_grid
        self.generation += 1

    def _next_generation_ant(self) -> None:
        """
        Compute the next step of Langton's Ant.
        """
        x, y = self.ant_position
        current_color = self.grid.get((x, y), 0)

        # Flip the color of the current cell
        if current_color == 0:
            self.grid[(x, y)] = 1
        else:
            del self.grid[(x, y)]

        # Turn 90° right if the square is white (0), left if black (1)
        self.ant_direction = (
            (self.ant_direction + 1) % 4
            if current_color == 0
            else (self.ant_direction - 1) % 4
        )

        # Move forward one step
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.ant_direction]
        self.ant_position = (x + dx, y + dy)

        self.generation += 1

    def print_board_ascii(self) -> None:
        """
        Print the current state of the Game of Life grid.
        """
        for y in range(self.display_height):
            for x in range(self.display_width):
                print(
                    (
                        "●"
                        if self.grid.get((x + self.offset[0], y + self.offset[1]), 0)
                        else " "
                    ),
                    end="",
                )
            print()

    def print_neighbors(self) -> None:
        """
        Print the number of live neighbors for each cell in the Game of Life grid.
        """
        for y in range(self.display_height):
            for x in range(self.display_width):
                neighbors: int = self.get_neighbors(
                    x + self.offset[0], y + self.offset[1]
                )
                print(f"{neighbors} ", end="")
            print()

    def print_neighbors_rich(self) -> None:
        """
        Print the number of live neighbors for each cell in the Game of Life grid using Rich.
        Colors: red=will die, green=will generate, white=will continue
        """
        for y in range(self.display_height):
            row = []
            for x in range(self.display_width):
                neighbors: int = self.get_neighbors(
                    x + self.offset[0], y + self.offset[1]
                )
                cell_state = self.grid.get((x + self.offset[0], y + self.offset[1]), 0)
                if cell_state == 1 and (neighbors < 2 or neighbors > 3):
                    color = "red"
                elif cell_state == 0 and neighbors == 3:
                    color = "green"
                else:
                    color = "white"
                row.append(f"[{color}]{neighbors}[/{color}]")
            rprint(" ".join(row))

    def handle_key_press(self, event) -> None:
        """
        Handle key presses and adjust the offset accordingly.
        """
        key = event.name
        if key in ["w", "up"]:
            self.offset = (self.offset[0], self.offset[1] - 1)
        elif key in ["s", "down"]:
            self.offset = (self.offset[0], self.offset[1] + 1)
        elif key in ["a", "left"]:
            self.offset = (self.offset[0] - 1, self.offset[1])
        elif key in ["d", "right"]:
            self.offset = (self.offset[0] + 1, self.offset[1])

    def run(self, generations: int = 100) -> None:
        """
        Run the simulation for a specified number of generations.

        Args:
            generations (int): Number of generations to simulate. Defaults to 100.
        """

        # Set up the keyboard listener
        on_press(self.handle_key_press)

        with Live(console=console, refresh_per_second=self.refresh_per_second) as live:
            for _ in range(generations):
                if self.mode == SimulationMode.LIFE:
                    title = Text(
                        f"Conway's Game of Life: {self.display_width}x{self.display_height} - Rules: {self.rules.name} - Offset: {self.offset} - Infinite: {self.infinite_mode} - Gen: {self.generation} / {generations}",  # pylint: disable=line-too-long
                        style="bold magenta",
                    )
                else:
                    title = Text(
                        f"Langton's Ant: {self.display_width}x{self.display_height} - Offset: {self.offset} - Infinite: {self.infinite_mode} - Gen: {self.generation} / {generations}",  # pylint: disable=line-too-long
                        style="bold magenta",
                    )

                table: Table = Table(title=title, show_header=False, show_lines=True)
                for y in range(self.display_height):
                    row = []
                    for x in range(self.display_width):
                        cell_x, cell_y = x + self.offset[0], y + self.offset[1]
                        if self.mode == SimulationMode.LIFE:
                            cell = "●" if self.grid.get((cell_x, cell_y), 0) else " "
                        else:
                            if (cell_x, cell_y) == self.ant_position:
                                cell = "▲▶▼◀"[self.ant_direction]
                            else:
                                cell = (
                                    "■" if self.grid.get((cell_x, cell_y), 0) else " "
                                )
                        row.append(cell)
                    table.add_row(*row)

                self.next_generation()
                live.update(table)
                sleep(1 / self.refresh_per_second)


@app.command()
def main(
    display_width: int = typer.Option(
        def_size, "--width", "-w", help="Width of the grid"
    ),
    display_height: int = typer.Option(
        def_size - 2, "--height", "-h", help="Height of the grid"
    ),
    infinite_mode: bool = typer.Option(
        False, "--infinite", "-i", help="Enable infinite mode"
    ),
    generations: int = typer.Option(
        100, "--generations", "-g", help="Number of generations to simulate"
    ),
    rules: NeighborhoodRules = typer.Option(
        NeighborhoodRules.MOORE, "--rules", "-r", help="Neighborhood rules to use"
    ),
    offset_x: int = typer.Option(0, "--offset-x", "-x", help="X-coordinate offset"),
    offset_y: int = typer.Option(0, "--offset-y", "-y", help="Y-coordinate offset"),
    mode: SimulationMode = typer.Option(
        SimulationMode.LIFE, "--mode", "-m", help="Simulation mode (life or ants)"
    ),
    refresh_per_second: int = typer.Option(
        10, "--rps", "-r", help="Refresh rate per second"
    ),
):
    """
    Run Conway's Game of Life or Langton's Ant simulation with specified parameters.
    """
    game: GameOfLife = GameOfLife(
        display_width=display_width,
        display_height=display_height,
        infinite_mode=infinite_mode,
        rules=rules,
        offset=(offset_x, offset_y),
        mode=mode,
        refresh_per_second=refresh_per_second,
    )
    game.run(generations=generations)


if __name__ == "__main__":
    typer.run(main)
else:
    # When imported as a module, make sure GameOfLife is available
    __all__ = ["GameOfLife"]
