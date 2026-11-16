# Task 1: Plan the Agent

This design uses A* to find a lowest-cost path on the fixed warehouse grid
formulated in [Task 0](task0_problem_formulation.md). The robot moves only in
four orthogonal directions, and each move costs 1, so Manhattan distance to
the goal is the heuristic:

`h((row, column)) = |row - goal_row| + |column - goal_column|`.

## Agent design

| Design question | Specification |
|---|---|
| **State representation** | A state is a Python tuple `(row, column)` of integers, such as `(1, 1)`. The tuple is hashable, so it can be used as a key in dictionaries and sets. |
| **Warehouse representation** | Store the nine map rows as an immutable tuple of strings. A cell is blocked exactly when its character is `#`; `S`, `G`, and `.` are traversable. The fixed start is `(1, 1)` and the goal is `(7, 15)`. |
| **Valid actions** | Consider Up, Down, Left, and Right in a fixed order. For each action, calculate its neighboring position and allow it only if the position is inside the grid and its cell is not `#`. |
| **Goal test** | The current state is the goal when it equals `(7, 15)`. |
| **Frontier** | Use a min-priority queue. Each entry stores the state's priority `f = g + h`, a tie-breaker for deterministic ordering, the path cost `g`, and the state. The lowest-`f` entry is selected next. |
| **Search bookkeeping** | Keep `g_score[state]`, the lowest known cost from the start, and `came_from[state]`, the predecessor state used to reach it. When a cheaper route to a state is found, update both maps and add a new queue entry. Skip a popped entry if its stored `g` no longer matches `g_score`; this discards outdated entries. |
| **Path reconstruction** | When the goal is selected from the frontier, follow `came_from` links from the goal back to the start, then reverse the collected states. Consecutive coordinates show the route; their differences determine the move names. |

Manhattan distance never overestimates the remaining number of moves in this
four-direction, unit-cost grid. It therefore gives A* a useful estimate while
preserving shortest-path solutions.

## Termination report

Return or print these fields when the search finishes:

| Field | Meaning |
|---|---|
| **Solution found** | `True` if the goal was reached; otherwise `False`. |
| **Solution path** | The coordinate sequence from start through goal, inclusive. If no route exists, report that no path was found. |
| **Path length** | Number of moves, equal to the number of coordinate transitions (`len(path) - 1`). If no route exists, report that it is unavailable. |
| **States expanded** | Number of non-stale, non-goal states removed from the frontier whose valid neighboring cells were examined. The goal is tested when removed from the frontier and is not counted as expanded. |

## Execution outline

1. Put the start state in the priority queue with `g = 0` and `f = h(start)`;
   initialize its `g_score` to zero.
2. Repeatedly remove the lowest-priority entry. Skip it if it is outdated.
3. If its state is the goal, reconstruct the path and return the report.
4. Otherwise, count the state as expanded. For each valid neighboring state,
   calculate `candidate_g = g_score[current] + 1`. If this is lower than its
   recorded cost, update `g_score` and `came_from`, calculate `f = candidate_g
   + h(neighbor)`, and push the neighbor onto the frontier.
5. If the frontier becomes empty before the goal is reached, return a
   no-solution report with the number of states expanded.
