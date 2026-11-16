# Task 1: Understanding the Warehouse Navigation Problem

## Problem specification

An autonomous warehouse vehicle must travel from a loading bay to a dispatch
area through a fixed warehouse map. Shelving units are obstacles and cannot be
crossed. The map is a discrete grid: `S` is the start, `G` is the goal, `#` is
an obstacle, and `.` is traversable space. Rows and columns below are indexed
from zero, starting at the top left.

```text
#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################
```

The start is at `(1, 1)` and the goal is at `(1, 19)`. The outer border is
blocked, like the shelving units shown inside the warehouse.

### 1. What is the environment?

The environment is the warehouse represented by the fixed, two-dimensional
grid above. Each cell is either traversable or blocked. For this problem, the
map is known and does not change while the vehicle is planning or moving. It is
a discrete, single-agent, deterministic environment: an action moves the
vehicle one cell in the selected direction, unless that cell is blocked.

### 2. What is the agent's goal?

Reach the dispatch area at `G` from the loading bay at `S` without entering an
obstacle. A shortest valid route is a useful objective because every move has
the same cost; if only reaching the destination matters, any collision-free
route is sufficient.

### 3. What actions are available?

The vehicle may move one grid square **Up**, **Down**, **Left**, or **Right**.
Diagonal movement is not allowed. Moves into obstacles or outside the map are
invalid.

### 4. What information must the agent maintain to choose its next action?

The agent needs its current grid position, the map of traversable and blocked
cells, and the goal position. To plan a route, it also needs search bookkeeping
such as which positions have been visited and which positions remain to be
explored. With this static, known map, the agent can plan the route before
moving; it can update its current position after each move.

### 5. Why is this a goal-based agent rather than a simple reflex agent?

A goal-based agent considers whether actions lead toward the specified
destination and uses the map to plan around obstacles. A simple reflex agent
selects an action from the current percept alone, without reasoning about a
future route or the goal. Here the best move depends on the destination and
the layout of obstacles, so planning is needed.

## Think about it: a warehouse twice as large

Breadth-first search remains appropriate when every move has equal cost: it is
complete on this finite grid and finds a shortest path. As the grid grows, it
may need to visit and store many more positions; in a grid with `V` traversable
cells and at most four neighbors per cell, its time and space use are
`O(V + E)`, which is `O(V)` here. A larger map can therefore increase memory
and planning time substantially. A* search with Manhattan distance as its
heuristic would often explore fewer cells for a single start-to-goal query,
while retaining an optimal path on this four-direction, equal-cost grid.
Dynamic obstacles or an initially unknown map would also require the agent to
update its map and replan as it moves.
