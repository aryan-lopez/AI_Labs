"""Find a shortest route through the Lab 3 warehouse using BFS."""

from collections import deque
from typing import Dict, Optional

from task2_astar_agent import (
    Grid,
    Position,
    SearchResult,
    WAREHOUSE,
    find_marker,
    moves_for_path,
    reconstruct_path,
    valid_neighbors,
    validate_grid,
)


def bfs(grid: Grid) -> SearchResult:
    """Return a shortest path using breadth-first search.

    All moves cost one, so FIFO order explores states in nondecreasing path
    length. Each state is marked discovered when it is enqueued, preventing
    duplicate queue entries. Expansion counting matches the A* agent: count
    each non-goal state removed from the frontier whose neighbors are checked.
    """
    validate_grid(grid)
    start = find_marker(grid, "S")
    goal = find_marker(grid, "G")

    frontier = deque([start])
    came_from: Dict[Position, Optional[Position]] = {start: None}
    distance: Dict[Position, int] = {start: 0}
    states_expanded = 0

    while frontier:
        current = frontier.popleft()

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return SearchResult(
                found=True,
                path=path,
                moves=moves_for_path(path),
                states_expanded=states_expanded,
            )

        states_expanded += 1
        for neighbor, _ in valid_neighbors(grid, current):
            if neighbor not in distance:
                distance[neighbor] = distance[current] + 1
                came_from[neighbor] = current
                frontier.append(neighbor)

    return SearchResult(
        found=False,
        path=[],
        moves=[],
        states_expanded=states_expanded,
    )


def main() -> None:
    """Run BFS on the original warehouse map and print its measurements."""
    result = bfs(WAREHOUSE)
    print(f"Solution found: {result.found}")
    print(f"Path length: {result.path_length}")
    print(f"States expanded: {result.states_expanded}")
    if result.found:
        print("Path coordinates (row, column):")
        print(" -> ".join(str(position) for position in result.path))
        print("Moves:")
        print(" -> ".join(result.moves) if result.moves else "Already at the goal")


if __name__ == "__main__":
    main()
