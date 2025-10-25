from rich_life.__main__ import GameOfLife, NeighborhoodRules, SimulationMode


def test_game_of_life_initialization():
    game = GameOfLife(10, 10)
    assert game.display_width == 10
    assert game.display_height == 10
    assert isinstance(game.grid, dict)
    assert game.generation == 0
    assert game.infinite_mode
    assert game.rules == NeighborhoodRules.MOORE
    assert game.offset == (0, 0)
    assert game.mode == SimulationMode.LIFE


def test_get_neighbors():
    game = GameOfLife(3, 3, infinite_mode=False)
    game.grid = {
        (0, 0): 1,
        (1, 0): 1,
        (2, 0): 1,
        (0, 1): 1,
        (2, 1): 1,
        (0, 2): 1,
        (1, 2): 1,
        (2, 2): 1,
    }
    game.print_neighbors()
    assert game.get_neighbors(1, 1) == 8
    assert game.get_neighbors(0, 0) == 7
    assert game.get_neighbors(1, 0) == 7


def test_next_generation():
    game = GameOfLife(5, 5, infinite_mode=False)
    game.grid = {(2, 1): 1, (2, 2): 1, (2, 3): 1}
    game.next_generation()
    assert game.grid == {(1, 2): 1, (2, 2): 1, (3, 2): 1}
    assert game.generation == 1


def test_langtons_ant():
    game = GameOfLife(5, 5, mode=SimulationMode.ANTS)
    assert game.ant_position == (2, 2)
    assert game.ant_direction == 0
    game.next_generation()
    assert (2, 2) in game.grid
    assert game.ant_position != (2, 2)
