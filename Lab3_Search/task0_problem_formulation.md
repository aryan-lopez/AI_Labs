# Task 0: Understanding the Search Problem

## Warehouse map

The warehouse is a fixed 9-row by 17-column grid. Rows and columns are indexed
from zero, starting at the top-left corner. The robot starts at `(1, 1)` and
the goal is at `(7, 15)`.

```text
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################
```

## Search-problem formulation

| Component | Specification |
|---|---|
| **State `S`** | The robot's current grid position `(row, column)`. The map is fixed and known, so the position is enough to identify the robot's state during search. |
| **Actions `A`** | Move one cell **Up**, **Down**, **Left**, or **Right**. An action is available in a state only when its destination is inside the grid and is not an obstacle (`#`). |
| **Transition `T`** | Applying a valid action changes the position by one cell in that direction. The destination cell becomes the new state. The transition is undefined for an invalid move. |
| **Initial state `s₀`** | `(1, 1)`, the cell marked `S`. |
| **Goal `G`** | Reach `(7, 15)`, the cell marked `G`. Equivalently, a state is a goal state when the robot's position equals `(7, 15)`. |
| **Cost `c`** | Each valid movement costs `1`. The cost of a path is its number of moves. |

## Questions

### (a) What information is necessary to specify a state?

The robot's current row and column are sufficient: `(row, column)`. The
warehouse layout and movement rules are fixed parts of the problem definition,
not information that changes from state to state.

### (b) What makes an action invalid?

An action is invalid if it would move the robot outside the grid or into a
blocked cell marked `#`. Only the four orthogonal moves are allowed; diagonal
movement is not an action.

### (c) Is this a deterministic search problem?

Yes. Given a position and a valid action, the next position is uniquely
determined. The map does not change, and movement has no random outcome.

### (d) What would constitute a solution?

A solution is a sequence of valid moves from the initial state `(1, 1)` to the
goal `(7, 15)`, with every visited cell traversable. Its path cost is the
number of moves; a lowest-cost solution is a shortest path.
