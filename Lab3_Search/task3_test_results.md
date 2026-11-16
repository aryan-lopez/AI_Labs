# Task 3: Test the Generated Program

The repeatable tests are in [`task3_astar_tests.py`](task3_astar_tests.py) and
run with `python3 Lab3/task3_astar_tests.py`. They check that returned
coordinates begin at `S`, end at `G`, remain in traversable cells, move only
between orthogonal neighbors, and have the expected length.

## Results

| Case | Expected behavior | Result | Path length | States expanded |
|---|---|---:|---:|---:|
| Original warehouse | Find a valid route | Passed | 40 | 63 |
| Adjacent goal (`##### / #SG## / #####`) | Find the one-move route | Passed | 1 | 1 |
| Unreachable goal (the lab's no-solution example) | Report failure and terminate | Passed | None | 9 |
| Multiple routes | Return a shortest route | Passed | 5 | 5 |

For the multiple-route case, the program chose the direct top corridor, a
valid five-move path. The map also has a valid nine-move detour through the
lower corridor, so this case confirms that the returned route is shorter
than an available alternative.

All four tests passed. The unreachable case returned `found=False`, an empty
path, and no path length instead of looping. The original-map result matches
the run recorded for Task 2. These checks cover the minimum cases requested
in the lab; the later tasks separately examine the algorithm's components
and compare it with BFS.
