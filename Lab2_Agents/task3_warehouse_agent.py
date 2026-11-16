"""Find a shortest collision-free route through the warehouse using BFS."""

from collections import deque
from typing import Dict, List, Optional, Tuple


Position = Tuple[int, int]

WAREHOUSE = (
    "#####################",
    "#S....#............G#",
    "#.##....##########..#",
    "#....##.............#",
    "#.######.###.#.###..#",
    "#........#..........#",
    "#####################",
)

# The order is fixed so the same map produces the same route every run.
MOVES = (
    (-1, 0, "Up"),
    (1, 0, "Down"),
    (0, -1, "Left"),
    (0, 1, "Right"),
)


def find_marker(grid: Tuple[str, ...], marker: str) -> Position:
    """Return the unique position of marker, raising an error if malformed."""
    matches = [
        (row_index, column_index)
        for row_index, row in enumerate(grid)
        for column_index, cell in enumerate(row)
        if cell == marker
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {marker!r}, found {len(matches)}")
    return matches[0]


def validate_grid(grid: Tuple[str, ...]) -> None:
    """Check that the map is a nonempty rectangular grid with valid cells."""
    if not grid or not grid[0]:
        raise ValueError("The warehouse grid must not be empty")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("Every warehouse row must have the same width")
    valid_cells = {"#", ".", "S", "G"}
    if any(cell not in valid_cells for row in grid for cell in row):
        raise ValueError("The map contains an unknown cell character")
    find_marker(grid, "S")
    find_marker(grid, "G")


def shortest_path(
    grid: Tuple[str, ...], start: Position, goal: Position
) -> Optional[List[Position]]:
    """Return a shortest path from start to goal, or None when unreachable.

    Breadth-first search explores cells in increasing number of moves. The
    predecessor map both prevents revisiting cells and reconstructs the route.
    """
    rows, columns = len(grid), len(grid[0])
    frontier = deque([start])
    predecessor: Dict[Position, Optional[Position]] = {start: None}

    while frontier:
        current = frontier.popleft()
        if current == goal:
            break

        for row_delta, column_delta, _ in MOVES:
            neighbor = (current[0] + row_delta, current[1] + column_delta)
            row, column = neighbor
            in_bounds = 0 <= row < rows and 0 <= column < columns
            if (
                in_bounds
                and grid[row][column] != "#"
                and neighbor not in predecessor
            ):
                predecessor[neighbor] = current
                frontier.append(neighbor)

    if goal not in predecessor:
        return None

    # Follow predecessor links backward from the goal, then reverse the route.
    path: List[Position] = []
    current: Optional[Position] = goal
    while current is not None:
        path.append(current)
        current = predecessor[current]
    path.reverse()
    return path


def directions_for(path: List[Position]) -> List[str]:
    """Convert consecutive positions into human-readable move names."""
    direction_by_delta = {
        (row_delta, column_delta): name
        for row_delta, column_delta, name in MOVES
    }
    directions = []
    for current, following in zip(path, path[1:]):
        delta = (following[0] - current[0], following[1] - current[1])
        directions.append(direction_by_delta[delta])
    return directions


def display_route(grid: Tuple[str, ...], path: List[Position]) -> None:
    """Print the warehouse with route cells marked by '*'."""
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
    """Plan a route on the warehouse map and print the result."""
    validate_grid(WAREHOUSE)
    start = find_marker(WAREHOUSE, "S")
    goal = find_marker(WAREHOUSE, "G")
    path = shortest_path(WAREHOUSE, start, goal)

    if path is None:
        print("No collision-free path exists from S to G.")
        return

    directions = directions_for(path)
    print(f"Shortest path found: {len(directions)} moves")
    print("Path coordinates (row, column):")
    print(" -> ".join(str(position) for position in path))
    print("Moves:")
    print(" -> ".join(directions) if directions else "Already at the goal")
    print("Route map (* marks the path):")
    display_route(WAREHOUSE, path)


if __name__ == "__main__":
    main()
