# Task 3: Test the Generated Planner

The planner was checked on the required solvable, impossible, and irrelevant
action cases. The checks are in [task3_planner_tests.py](task3_planner_tests.py).
For the solvable case, the test replays the returned actions independently,
checking each action's preconditions and comparing each computed successor
with the reported state trace.

## Test A: Solvable warehouse

- **Initial state:** `{RobotAt(A), PackageAt(A)}`
- **Goal:** `PackageAt(C)`
- **Plan found:** Yes
- **Plan:** `PickUp(A) -> Move(A,B) -> Move(B,C) -> Drop(C)`
- **Plan valid:** Yes. Every action is applicable in its preceding state, the
  reported transitions match the action effects, and the final state contains
  `PackageAt(C)`.

## Test B: Impossible problem

All `PickUp` actions were removed from the original action set.

- **Initial state:** `{RobotAt(A), PackageAt(A)}`
- **Goal:** `PackageAt(C)`
- **Plan found:** No
- **Result:** Correct. Without pickup, the package cannot be held and carried
  to `C`; the planner reports no plan.

## Test C: Irrelevant robot movement

The initial state is `{RobotAt(B), PackageAt(B)}` and only movement actions are
available. `Move(B,C)` can take the robot to `C` while leaving the package at
`B`. The goal remains `PackageAt(C)`.

- **Initial state:** `{RobotAt(B), PackageAt(B)}`
- **Goal:** `PackageAt(C)`
- **Robot can reach C:** Yes; after `Move(B,C)`, the state has `RobotAt(C)` and
  `PackageAt(B)`.
- **Plan found:** No
- **Result:** Correct. Reaching the goal location with the robot does not
  satisfy the package-location goal.

## Run results

Command: `python3 Lab4_Logic/task3_planner_tests.py`

```text
Test A — solvable warehouse: plan found and every transition is valid
  PickUp(A) -> Move(A,B) -> Move(B,C) -> Drop(C)
Test B — pickup actions removed: no plan found
Test C — robot reaches C while package stays at B: no plan found
All three required checks passed.
```
