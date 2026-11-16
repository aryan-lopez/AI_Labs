# Task 1: Construct a Plan by Hand

A valid plan that transports the package from `A` to `C` is:

```text
PickUp(A)
Move(A,B)
Move(B,C)
Drop(C)
```

The state after each action is shown below. A state lists the propositions that
are true; when the robot is holding the package, the package is not listed as
being at a location.

| Step | Action | State after the action |
|---|---|---|
| 0 | Initial state | `{RobotAt(A), PackageAt(A)}` |
| 1 | `PickUp(A)` | `{RobotAt(A), Holding(Package)}` |
| 2 | `Move(A,B)` | `{RobotAt(B), Holding(Package)}` |
| 3 | `Move(B,C)` | `{RobotAt(C), Holding(Package)}` |
| 4 | `Drop(C)` | `{RobotAt(C), PackageAt(C)}` |

Each action's preconditions hold in the state immediately before it: the robot
and package are both at `A` for pickup; the robot is at the starting endpoint
for each move and the locations are connected; and the robot is at `C` and
holding the package for the drop. The final state satisfies the goal
`PackageAt(C)`.
