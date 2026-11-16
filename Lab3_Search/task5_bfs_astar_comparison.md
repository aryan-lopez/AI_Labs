# Task 5: Compare A* with Blind Search

The BFS implementation is [`task5_bfs_agent.py`](task5_bfs_agent.py). It uses
the original warehouse and shared movement, grid-validation, and path helpers
from [`task2_astar_agent.py`](task2_astar_agent.py). Both algorithms use the
same neighbor order and the same expansion-count convention: count each
non-goal state removed from the frontier whose neighbors are examined.

## Results on the original warehouse

| Measure | BFS | A* |
|---|---:|---:|
| Solution found | Yes | Yes |
| Path length | 40 moves | 40 moves |
| States expanded | 63 | 63 |

Both algorithms returned the same 40-move coordinate path. They were run on
the unchanged warehouse map.

## Questions

### (a) Did both algorithms find a solution?

Yes. Both reached the goal.

### (b) Did they find paths of the same length?

Yes. Each returned a path of 40 moves, so both found a shortest path for this
unit-cost map.

### (c) Which algorithm expanded fewer states?

Neither. Both expanded 63 states under the same counting convention.

### (d) Why might A* expand fewer states?

A* ranks the frontier using both the cost already paid, `g(n)`, and an estimate
of the remaining cost, `h(n)`. With a useful heuristic, it can prioritize
states that appear to lead toward the goal and avoid exploring as many
off-route states as BFS, which orders states only by distance from the start.
On this particular map, the corridors and obstacles constrain the useful
routes enough that the Manhattan heuristic did not reduce the measured
expansion count compared with BFS.
