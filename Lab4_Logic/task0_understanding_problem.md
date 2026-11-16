# Task 0: Understanding the Planning Problem

## Warehouse and state representation

The warehouse has three locations arranged in a line:

```text
A --- B --- C
```

The robot and package both start at `A`. The robot can move between directly
connected locations in either direction. Represent a state with propositions:

- `RobotAt(x)`: the robot is at location `x`.
- `PackageAt(x)`: the package is at location `x`.
- `Holding(Package)`: the robot is carrying the package.

The package is represented as either being at one location or being held. The
robot can carry it while moving, and dropping it places it at the robot's
current location.

## Planning-problem specification

| Component | Specification |
|---|---|
| **Initial state** | `{RobotAt(A), PackageAt(A)}` |
| **Goal** | `PackageAt(C)` |
| **Locations and connections** | Locations `A`, `B`, and `C`; undirected connections `A—B` and `B—C` |
| **Actions** | `Move(x,y)` for each directed traversal of a connection; `PickUp(x)` and `Drop(x)` for each location `x` |

### Action preconditions and effects

Effects prefixed with `+` are added to the state; effects prefixed with `−`
are removed.

| Action | Preconditions | Effects |
|---|---|---|
| `Move(x,y)` where `x` and `y` are connected | `RobotAt(x)`, `Connected(x,y)` | `− RobotAt(x)`, `+ RobotAt(y)` |
| `PickUp(x)` | `RobotAt(x)`, `PackageAt(x)` | `− PackageAt(x)`, `+ Holding(Package)` |
| `Drop(x)` | `RobotAt(x)`, `Holding(Package)` | `− Holding(Package)`, `+ PackageAt(x)` |

The available directed move actions are `Move(A,B)`, `Move(B,A)`,
`Move(B,C)`, and `Move(C,B)`. Pickup and drop actions are available at `A`,
`B`, and `C`, subject to their preconditions.

## Think About It: Check the action preconditions

Starting from `{RobotAt(A), PackageAt(A)}`, is `PickUp(A)` applicable? What
about `Drop(C)`?

`PickUp(A)` is applicable: both `RobotAt(A)` and `PackageAt(A)` are true in the
initial state, so all its preconditions are satisfied.

`Drop(C)` is not applicable: the initial state does not contain `RobotAt(C)` or
`Holding(Package)`. An action being listed as available does not mean its
preconditions hold in the current state.
