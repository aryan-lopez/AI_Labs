# Task 3: Prompt Engineering and Program Run

## Prompt used

> Write a well-documented Python 3 program implementing a goal-based agent for
> the warehouse navigation problem in `task1_problem_specification.md`. Use
> its exact grid, where `S` is the start, `G` is the goal, `#` is an obstacle,
> and `.` is free space. The vehicle can move one cell Up, Down, Left, or
> Right. Find a collision-free route from `S` to `G`, avoiding every obstacle.
> Print either the route and its moves or a suitable message if no route
> exists. Explain in the program comments which search algorithm you use and
> why it fits this equal-cost grid. Keep the environment and movement rules
> unchanged.

## Implementation and run

The program is [`task3_warehouse_agent.py`](task3_warehouse_agent.py). It uses
breadth-first search (BFS), stores each discovered cell's predecessor, and
reconstructs a shortest route after reaching the goal. It prints the route as
coordinates and directions, and marks the route on the map with `*`.

The program ran successfully on the first attempt. It found a collision-free
route from `(1, 1)` to `(1, 19)` in 20 moves. No prompt revision was needed.

## Follow-up questions

1. **Did the LLM generate a working program on the first attempt?** Yes. The
   first run completed and printed a collision-free path from start to goal.

2. **If not, how could the prompt be improved?** This did not apply because
   the first attempt worked. If it had failed, I would include the exact error
   and ask for a correction while restating the required grid, movement rules,
   and expected output, then run the revised program again.

3. **What search algorithm did the program use?** Breadth-first search (BFS).

4. **Why do you think the LLM selected this algorithm?** The prompt specifies
   a finite grid with four-direction movement and equal-cost steps. BFS is a
   standard fit for this setting: it explores in increasing path length, is
   complete on the finite map, and returns a shortest route when one exists.
   It is also easy to explain and implement for this small warehouse.
