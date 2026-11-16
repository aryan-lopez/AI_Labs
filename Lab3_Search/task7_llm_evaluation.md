# Task 7: Evaluate the LLM-Generated Agent

This reflection is based on the design in Tasks 0–1, the implementation
prompt and run recorded in Task 2, and the tests and experiments recorded in
Tasks 3, 5, and 6.

## Reflection questions

### 1. What parts of the generated code were correct immediately?

The implementation followed the warehouse rules in my design: it represented
states as `(row, column)` tuples, allowed only in-bounds orthogonal moves into
non-obstacle cells, and used a priority queue ordered by `g(n) + h(n)`. It
tracked the best known path cost and predecessor for each position, skipped
outdated queue entries, and reconstructed the route when the goal was reached.
The recorded run found a legal 40-move route on the original map. The later
tests also confirmed the one-move case and a shortest route on a map with
alternatives.

### 2. Did you find any bugs or design problems?

The recorded tests did not expose a functional bug in the A* agent: the
original, trivial, no-solution, and alternative-route cases all passed. The
heuristic experiment did highlight an important limitation: multiplying
Manhattan distance by two can make the heuristic inadmissible, so shortest-path
behavior is no longer guaranteed in general. It happened to return a
40-move path on this warehouse, which does not prove that it will always
return an optimal path. This is a limitation of that experimental heuristic,
not a failure of the default Manhattan configuration.

### 3. How did you discover those problems?

I checked the implementation against the design and ran tests with known
expected behavior. The adjacent-goal map checked the one-step result; the
unreachable map checked that the search terminates with failure; and the map
with two routes checked that the returned path is shorter than a known valid
detour. In Task 6, I compared path lengths and expansion counts after changing
the heuristic. These checks showed both the default agent's tested behavior
and why a successful run with an over-aggressive heuristic is not an
optimality guarantee.

### 4. Did the LLM use terminology or data structures that you did not understand?

The implementation uses terms such as *frontier*, *heuristic*, *priority
queue*, and *stale entry*. The Task 1 design and Task 4 code inspection connect
these terms to the program: the frontier is the heap of candidate states,
`g_score` stores the best known cost, and an outdated entry is skipped when
its stored cost no longer matches that best cost. This made the implementation
readable in terms of the search problem rather than treating the code as a
black box.

### 5. Did you modify the LLM-generated code?

Yes. The A* agent accepts an optional heuristic so Task 6 can compare
Manhattan distance with zero, Euclidean distance, and twice Manhattan
distance; Manhattan remains the default. A separate BFS agent was also added
for Task 5, reusing the warehouse and path helpers so the comparison uses the
same movement rules and expansion-count convention.

### 6. Which tests were most useful?

The no-solution test was useful because it checked termination and explicit
failure reporting. The alternative-path test was useful because it checked
shortest-path behavior against a known longer route, rather than merely
checking that some route was returned. The adjacent-goal case was a quick
check of the basic path length and goal handling. Together with the original
warehouse run, these tests covered both simple and less obvious behavior.

### 7. Could you have trusted the program without testing it?

No. A route that looks plausible does not establish that every move is legal,
that an unreachable goal is handled, or that a returned route is shortest.
The tests checked those properties using cases where the expected behavior
was known. The heuristic experiment also showed that changing one part of the
algorithm can remove the general optimality guarantee even when the result on
one map still looks correct.

### 8. What did you understand about A* that you did not understand before
implementing it?

I learned how A* combines the cost already paid, `g(n)`, with an estimate of
the remaining cost, `h(n)`, to order the frontier by `f(n) = g(n) + h(n)`.
For this four-direction, unit-cost grid, Manhattan distance is a lower bound
on the remaining number of moves, so it guides the search while preserving
shortest paths. The experiments made the role of the heuristic concrete:
`h(n) = 0` removes goal-directed guidance, while an overestimate such as
`2 × Manhattan` can make A* more aggressive without guaranteeing an optimal
route.

## What I designed, accepted, changed, and tested

| Stage | Record |
|---|---|
| **Designed** | Tasks 0–1 specify the state, actions, transitions, costs, Manhattan heuristic, priority-queue frontier, bookkeeping, path reconstruction, and reported measures before the implementation prompt. |
| **Suggested by the LLM** | The Task 2 prompt asks for a Python implementation of that design. The recorded implementation uses `heapq`, `g_score`, `came_from`, Manhattan distance, and stale-entry checks. |
| **Accepted** | I used that implementation as the baseline A* agent after its original-map result and the systematic tests matched the expected behavior. |
| **Changed or extended** | I made the heuristic selectable for Task 6 while keeping Manhattan as the default, and added a separate BFS implementation for Task 5. |
| **Tested** | Task 3 records the original, adjacent-goal, unreachable-goal, and alternative-route tests. Tasks 5–6 record the BFS comparison and heuristic experiments on the unchanged warehouse. |

The LLM helped translate a design into working code, but the design choices,
interpretation of the results, and decision to rely on the implementation
were checked against the problem requirements and recorded tests.

