"""Run the Task 6 heuristic variants on the original warehouse map."""

from math import hypot
from typing import Callable, List, Tuple

from task2_astar_agent import Position, SearchResult, WAREHOUSE, astar, manhattan_distance


HeuristicCase = Tuple[str, Callable[[Position, Position], float]]


def zero_heuristic(_position: Position, _goal: Position) -> float:
    """Return zero everywhere, removing goal-distance guidance."""
    return 0.0


def euclidean_distance(position: Position, goal: Position) -> float:
    """Return straight-line distance between two grid positions."""
    return hypot(position[0] - goal[0], position[1] - goal[1])


def twice_manhattan(position: Position, goal: Position) -> float:
    """Return twice the standard Manhattan estimate."""
    return 2 * manhattan_distance(position, goal)


def run_experiment() -> List[Tuple[str, SearchResult]]:
    """Run the baseline and all required heuristic variants."""
    cases: List[HeuristicCase] = [
        ("Manhattan (baseline)", manhattan_distance),
        ("h(n) = 0", zero_heuristic),
        ("Euclidean distance", euclidean_distance),
        ("2 x Manhattan", twice_manhattan),
    ]
    return [(name, astar(WAREHOUSE, heuristic)) for name, heuristic in cases]


def main() -> None:
    """Print the measurements requested in Task 6."""
    print(f"{'Heuristic':<24} {'Found':<8} {'Path length':<14} States expanded")
    for name, result in run_experiment():
        length = str(result.path_length) if result.path_length is not None else "None"
        print(
            f"{name:<24} {str(result.found):<8} {length:<14} "
            f"{result.states_expanded}"
        )


if __name__ == "__main__":
    main()
