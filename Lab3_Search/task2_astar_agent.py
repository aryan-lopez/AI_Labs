"""Find a shortest route through the Lab 3 warehouse with A* search."""

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from typing import Callable, Dict, List, Optional, Tuple


Position = Tuple[int, int]
Grid = Tuple[str, ...]
Heuristic = Callable[[Position, Position], float]

WAREHOUSE: Grid = (
    "#################",
    "#S....#.........#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#.............#G#",
    "#################",
)

# This fixed order and a sequence number make equal-priority choices stable.
MOVES = (
    (-1, 0, "Up"),
    (1, 0, "Down"),
    (0, -1, "Left"),
    (0, 1, "Right"),
)


@dataclass
class SearchResult:
    """A* outcome, including its path and expansion count."""

    found: bool
    path: List[Position]
    moves: List[str]
    states_expanded: int

    @property
    def path_length(self) -> Optional[int]:
        """Return the number of moves, or None when no route exists."""
        if not self.found:
            return None
        return len(self.path) - 1


def validate_grid(grid: Grid) -> None:
    """Reject empty, ragged, or malformed warehouse maps."""
    if not grid or not grid[0]:
        raise ValueError("The warehouse grid must not be empty")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("Every warehouse row must have the same width")
    if any(cell not in {"#", ".", "S", "G"} for row in grid for cell in row):
        raise ValueError("The map contains an unknown cell character")
    find_marker(grid, "S")
    find_marker(grid, "G")


def find_marker(grid: Grid, marker: str) -> Position:
    """Return the unique position of a marker, or raise ValueError."""
    matches = [
        (row_index, column_index)
        for row_index, row in enumerate(grid)
        for column_index, cell in enumerate(row)
        if cell == marker
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {marker!r}, found {len(matches)}")
    return matches[0]


def manhattan_distance(position: Position, goal: Position) -> int:
    """Estimate remaining moves for four-direction movement."""
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def valid_neighbors(grid: Grid, position: Position):
    """Yield traversable in-bounds neighbors and the moves leading to them."""
    rows, columns = len(grid), len(grid[0])
    for row_delta, column_delta, move_name in MOVES:
        neighbor = (position[0] + row_delta, position[1] + column_delta)
        row, column = neighbor
        if (
            0 <= row < rows
            and 0 <= column < columns
            and grid[row][column] != "#"
        ):
            yield neighbor, move_name


def reconstruct_path(
    came_from: Dict[Position, Optional[Position]], goal: Position
) -> List[Position]:
    """Follow predecessor links from goal to start and reverse the result."""
    path = []
    current: Optional[Position] = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def moves_for_path(path: List[Position]) -> List[str]:
    """Convert neighboring coordinate pairs to move names."""
    names_by_delta = {
        (row_delta, column_delta): name
        for row_delta, column_delta, name in MOVES
    }
    moves = []
    for current, following in zip(path, path[1:]):
        delta = (following[0] - current[0], following[1] - current[1])
        moves.append(names_by_delta[delta])
    return moves


def astar(grid: Grid, heuristic: Optional[Heuristic] = None) -> SearchResult:
    """Search for a path using A*, with Manhattan distance as the default.

    An optional heuristic can be supplied for controlled experiments; when
    omitted, the standard Manhattan heuristic is used.
    Every move costs one. The default Manhattan distance is admissible for
    four-direction movement, so the default search returns a shortest path
    when one exists. The best known g-score and predecessor are recorded for
    each discovered position. Old queue entries are ignored if a better route
    to their state was found later.
    """
    validate_grid(grid)
    estimate = heuristic if heuristic is not None else manhattan_distance
    start = find_marker(grid, "S")
    goal = find_marker(grid, "G")

    sequence = count()
    frontier = []
    start_g = 0
    heappush(
        frontier,
        (start_g + estimate(start, goal), next(sequence), start_g, start),
    )

    g_score: Dict[Position, int] = {start: start_g}
    came_from: Dict[Position, Optional[Position]] = {start: None}
    states_expanded = 0

    while frontier:
        _, _, current_g, current = heappop(frontier)

        # A better route may have been queued after this entry was added.
        if current_g != g_score.get(current):
            continue

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return SearchResult(
                found=True,
                path=path,
                moves=moves_for_path(path),
                states_expanded=states_expanded,
            )

        # Count a state when its valid successors are about to be examined.
        states_expanded += 1
        for neighbor, _ in valid_neighbors(grid, current):
            candidate_g = current_g + 1
            if candidate_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = candidate_g
                came_from[neighbor] = current
                estimated_total = candidate_g + estimate(neighbor, goal)
                heappush(
                    frontier,
                    (estimated_total, next(sequence), candidate_g, neighbor),
                )

    return SearchResult(
        found=False,
        path=[],
        moves=[],
        states_expanded=states_expanded,
    )


def display_path(grid: Grid, path: List[Position]) -> None:
    """Print the map with intermediate route cells marked by '*'."""
    route_cells = set(path)
    start = find_marker(grid, "S")
    goal = find_marker(grid, "G")
    for row_index, row in enumerate(grid):
        rendered = list(row)
        for column_index in range(len(row)):
            position = (row_index, column_index)
            if position in route_cells and position not in {start, goal}:
                rendered[column_index] = "*"
        print("".join(rendered))


def main() -> None:
    """Run A* on the assignment's original warehouse and report its result."""
    result = astar(WAREHOUSE)
    print(f"Solution found: {result.found}")
    if result.found:
        print(f"Path length: {result.path_length} moves")
        print("Path coordinates (row, column):")
        print(" -> ".join(str(position) for position in result.path))
        print("Moves:")
        print(" -> ".join(result.moves) if result.moves else "Already at the goal")
        print("Route map (* marks intermediate path cells):")
        display_path(WAREHOUSE, result.path)
    else:
        print("Path: none")
        print("Path length: unavailable")
    print(f"States expanded: {result.states_expanded}")


if __name__ == "__main__":
    main()
