# Task 6: Investigate the Heuristic

The repeatable experiment is in
[`task6_heuristic_experiment.py`](task6_heuristic_experiment.py). It runs each
heuristic on the unchanged original warehouse. The A* implementation accepts
an optional heuristic for these experiments; its default remains Manhattan
distance.

## Why Manhattan distance fits this warehouse

For a position `(row, column)` and goal `(goal_row, goal_column)`, Manhattan
distance is

`h(n) = |row - goal_row| + |column - goal_column|`.

Each move changes only one coordinate by one. Reaching the goal therefore
requires at least the row difference in vertical moves and the column
difference in horizontal moves. Their sum is a lower bound on the true route
cost. Obstacles can force a longer route, but cannot make a route shorter than
this bound. Manhattan distance is thus admissible for four-direction,
unit-cost movement and lets A* retain shortest-path behavior.

## Experimental results

Command: `python3 Lab3/task6_heuristic_experiment.py`

| Heuristic | Solution found | Path length | States expanded |
|---|---:|---:|---:|
| Manhattan (baseline) | Yes | 40 | 63 |
| `h(n) = 0` | Yes | 40 | 63 |
| Euclidean distance | Yes | 40 | 63 |
| `2 × Manhattan` | Yes | 40 | 66 |

All four runs found a path of 40 moves on this map. Zero and Euclidean distance
expanded the same number of states as the Manhattan baseline. Doubling
Manhattan expanded three more states here; it did not shorten the returned
path.

## What the variants show

- With `h(n) = 0`, the frontier priority is just `g(n)`. Since every move
  costs one, this behaves like uniform-cost search, which visits states in
  increasing path length as BFS does. It supplies no information about which
  direction leads to the goal. Its expansion count happened to match the
  baseline on this constrained map.
- Euclidean distance is also a lower bound on the number of orthogonal moves
  needed, so it remains admissible. It is less informative than Manhattan
  distance for this movement model, but the measured expansion count happened
  to be the same on this map.
- `2 × Manhattan` can overestimate the remaining cost, so it is not admissible
  in general. It pushes the search more aggressively toward states that
  appear close to the goal. That can change which states are expanded and can
  produce a non-shortest path on other maps. In this experiment it still
  returned a 40-move path, but that single result does not establish an
  optimality guarantee.
