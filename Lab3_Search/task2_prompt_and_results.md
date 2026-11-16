# Task 2: A* Implementation and Original-Map Run

## Prompt used

> Implement the A* agent described in `task1_agent_design.md` as a documented
> Python 3 program. Use the exact warehouse map from
> `task0_problem_formulation.md`; do not change its layout or movement rules.
> Represent positions as `(row, column)` tuples. Allow only in-bounds moves to
> non-obstacle cells in the Up, Down, Left, Right order. Use a min-priority
> queue and Manhattan distance, with cost 1 per move. Track the best known
> path cost and each discovered state's predecessor, ignore outdated frontier
> entries, and reconstruct the route when the goal is reached. Report whether
> a solution was found, the coordinate path and moves, path length, and the
> number of states expanded. If the goal is unreachable, report failure
> cleanly. Include comments explaining the main search components.

## Implementation

The generated program is [`task2_astar_agent.py`](task2_astar_agent.py). It
uses `heapq` as the priority queue, Manhattan distance as `h(n)`, and computes
`f(n) = g(n) + h(n)`. The `came_from` map reconstructs the path. Its expansion
count includes each non-stale, non-goal state removed from the frontier whose
neighbors are examined; the goal state itself is not counted.

## Original warehouse run

Command: `python3 Lab3/task2_astar_agent.py`

- **Solution found:** Yes
- **Path length:** 40 moves
- **States expanded:** 63
- **Path (row, column):**

```text
(1, 1) -> (1, 2) -> (1, 3) -> (1, 4) -> (1, 5) -> (2, 5) -> (3, 5) ->
(4, 5) -> (5, 5) -> (5, 6) -> (5, 7) -> (5, 8) -> (5, 9) -> (5, 10) ->
(5, 11) -> (5, 12) -> (5, 13) -> (4, 13) -> (3, 13) -> (3, 12) ->
(3, 11) -> (3, 10) -> (3, 9) -> (3, 8) -> (3, 7) -> (2, 7) -> (1, 7) ->
(1, 8) -> (1, 9) -> (1, 10) -> (1, 11) -> (1, 12) -> (1, 13) -> (1, 14) ->
(1, 15) -> (2, 15) -> (3, 15) -> (4, 15) -> (5, 15) -> (6, 15) -> (7, 15)
```

The program also printed the move directions and the map with the route
marked. This records the required run on the supplied map; the systematic
edge-case tests are specified in Task 3.
