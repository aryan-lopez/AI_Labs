"""Task 3 checks for the Lab 3 A* warehouse agent."""

import unittest

from task2_astar_agent import Grid, Position, SearchResult, WAREHOUSE, astar


TRIVIAL_MAP: Grid = (
    "#####",
    "#SG##",
    "#####",
)

NO_SOLUTION_MAP: Grid = (
    "#######",
    "#S....#",
    "###.###",
    "#...#G#",
    "#######",
)

ALTERNATIVE_PATHS_MAP: Grid = (
    "########",
    "#S....G#",
    "#.#.##.#",
    "#......#",
    "########",
)


def marker_position(grid: Grid, marker: str) -> Position:
    """Find a marker in a test map."""
    return next(
        (row_index, column_index)
        for row_index, row in enumerate(grid)
        for column_index, cell in enumerate(row)
        if cell == marker
    )


def is_legal_path(grid: Grid, path: list[Position]) -> bool:
    """Check that a coordinate sequence is a valid route on the map."""
    if not path:
        return False
    rows, columns = len(grid), len(grid[0])
    for row, column in path:
        if not (0 <= row < rows and 0 <= column < columns):
            return False
        if grid[row][column] == "#":
            return False
    return all(
        abs(first[0] - second[0]) + abs(first[1] - second[1]) == 1
        for first, second in zip(path, path[1:])
    )


class AStarTask3Tests(unittest.TestCase):
    def assert_valid_solution(
        self, grid: Grid, result: SearchResult, expected_length: int
    ) -> None:
        self.assertTrue(result.found)
        self.assertEqual(result.path[0], marker_position(grid, "S"))
        self.assertEqual(result.path[-1], marker_position(grid, "G"))
        self.assertTrue(is_legal_path(grid, result.path))
        self.assertEqual(result.path_length, expected_length)
        self.assertEqual(len(result.moves), expected_length)

    def test_original_warehouse(self) -> None:
        result = astar(WAREHOUSE)
        self.assert_valid_solution(WAREHOUSE, result, expected_length=40)
        self.assertEqual(result.states_expanded, 63)

    def test_adjacent_goal_is_one_move_away(self) -> None:
        result = astar(TRIVIAL_MAP)
        self.assert_valid_solution(TRIVIAL_MAP, result, expected_length=1)

    def test_unreachable_goal_reports_failure(self) -> None:
        result = astar(NO_SOLUTION_MAP)
        self.assertFalse(result.found)
        self.assertEqual(result.path, [])
        self.assertEqual(result.moves, [])
        self.assertIsNone(result.path_length)

    def test_shortest_route_among_alternatives(self) -> None:
        result = astar(ALTERNATIVE_PATHS_MAP)
        self.assert_valid_solution(ALTERNATIVE_PATHS_MAP, result, expected_length=5)

        # This second, valid route goes around the lower corridor and is longer.
        detour = [
            (1, 1), (2, 1), (3, 1), (3, 2), (3, 3),
            (3, 4), (3, 5), (3, 6), (2, 6), (1, 6),
        ]
        self.assertTrue(is_legal_path(ALTERNATIVE_PATHS_MAP, detour))
        self.assertEqual(len(detour) - 1, 9)
        self.assertLess(result.path_length, len(detour) - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
