# Task 4: Inspect the A* Algorithm

The references below point to the implementation in
[`task2_astar_agent.py`](task2_astar_agent.py).

## Where each concept appears

| Concept | Where it appears in the code |
|---|---|
| **State** | `Position = Tuple[int, int]` at line 9; a state is a `(row, column)` coordinate. |
| **Action** | The four named movement deltas in `MOVES`, lines 25–30. |
| **Transition** | `valid_neighbors`, lines 81–92, applies each movement delta and yields only in-bounds, non-obstacle neighbors. |
| **Goal test** | `if current == goal` at line 152. |
| **`g(n)`** | `g_score` stores the best known start-to-state cost (line 141 onward); `candidate_g = current_g + 1` adds the cost of a move at line 164. |
| **`h(n)`** | `manhattan_distance` at lines 76–78 computes the Manhattan estimate to the goal. |
| **`f(n)`** | The start priority is computed as `start_g + manhattan_distance(...)` at lines 136–139. For neighbors, `estimated_total = candidate_g + manhattan_distance(...)` at lines 165–171. Both are `g + h`. |
| **Frontier** | `frontier` is the heap-backed priority queue at lines 133–139; `heappop` selects entries at line 146 and `heappush` adds improved candidates at lines 169–172. |
| **Visited-state bookkeeping** | There is no separate closed/visited set. `g_score` at line 141 records each discovered state's best known cost. The comparison at line 165 rejects routes that do not improve it; lines 148–150 skip outdated heap entries. |
| **Path reconstruction** | `came_from` records predecessors at lines 142 and 166–167. `reconstruct_path`, lines 95–105, follows those links back to the start and reverses the result. |

## Questions

### (a) What data structure is used for the A* frontier?

The program uses a Python list as a min-heap, managed by `heapq`'s
`heappush` and `heappop` functions. Each entry contains `(f, sequence, g,
state)`. The sequence number provides stable tie-breaking when two entries
have equal `f` priorities.

### (b) How does the program select the next state to expand?

It removes the heap entry with the smallest `f(n) = g(n) + h(n)`. If that
entry's stored `g` no longer equals the best `g_score` for the state, it is
outdated and skipped. Otherwise, the state is checked for the goal and, if it
is not the goal, its valid neighbors are examined.

### (c) Where is the heuristic calculated?

`manhattan_distance` at lines 76–78 returns the sum of the absolute row and
column differences from the goal. A* calls it when assigning priorities to
the start and to each improved neighbor.

### (d) Does the program explicitly calculate `f(n) = g(n) + h(n)`?

Yes. It adds the path cost and heuristic when inserting the start and each
neighbor into the frontier. For neighbors, the sum is assigned to
`estimated_total`; the code does not use a variable literally named `f`.

### (e) How does the program prevent unnecessary repeated exploration?

`g_score` stores the best route cost found for each position. A newly
discovered route is queued only when its cost is strictly lower than the
recorded cost. If an older, worse queue entry remains, the comparison after
`heappop` detects it and skips it. The implementation has no separate closed
set; it can accept a genuinely improved route if one is found.
