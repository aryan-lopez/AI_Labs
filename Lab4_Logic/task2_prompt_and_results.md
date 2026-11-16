# Task 2: Ask an LLM to Implement the Planner

## Prompt used

> Implement a simple planning agent in Python 3. Represent a dynamic state as
> a set of logical propositions (tuples). Represent each ground action with a
> name, positive preconditions, negative preconditions, positive effects, and
> negative effects. An action is applicable when all positive preconditions
> are present and all negative preconditions are absent. Applying it removes
> its negative effects and adds its positive effects. Implement breadth-first
> search to find a sequence of applicable actions that satisfies a specified
> goal; return no plan when the goal is unreachable. Reconstruct and print the
> action sequence and the state reached after every action. Keep static
> warehouse connectivity facts separate from the changing state, but allow
> them to satisfy action preconditions. Instantiate the warehouse with
> locations A, B, and C; bidirectional connections A-B and B-C; initial state
> `{RobotAt(A), PackageAt(A)}`; and goal `PackageAt(C)`. Include Move, PickUp,
> and Drop actions with their correct preconditions and effects. Explain the
> implementation and its assumptions.

## Implementation

The generated program is [task2_planner.py](task2_planner.py). `Action` stores
the action name and all four condition/effect sets. `is_applicable` checks
positive and negative preconditions against the dynamic state plus the static
connection facts. `apply_action` removes delete effects and adds positive
effects. `breadth_first_plan` queues states in increasing action-count order,
marks states when enqueuing them, and stores parent/action links so it can
reconstruct both the plan and its state trace. If the queue empties before a
goal state is reached, it returns `None` and the program reports `No plan
found`.

The program treats the warehouse connections as static facts and keeps them
out of the changing state. Each move action includes the matching
`Connected(source,destination)` fact as a precondition. It assumes the package
is either at one location or being held, and that the robot can move while
holding it. The domain actions preserve those assumptions for this problem.

## Think About It: Locate the planning ideas in the code

The specification's ideas appear in these parts of the program:

| Idea | Implementation |
|---|---|
| Preconditions | `is_applicable` checks positive facts are present and negative facts absent. |
| Effects | `apply_action` removes negative effects and adds positive effects. |
| Goal | The goal check in `breadth_first_plan` checks the required positive facts and any forbidden negative facts. |
| BFS | A FIFO `deque` expands states in increasing number of actions. |

For each state, BFS tries every action in the action list that is applicable
there and enqueues each newly reached state. The queue explores all plans of
one action before plans of two actions, then all plans of two actions before
longer ones. This lets the search compare alternative sequences and ensures
the first goal state it finds uses the fewest actions.

The prompt and Python implementation were produced with LLM assistance. The
warehouse action definitions and the baseline run were reviewed against the
hand-built plan from Task 1.

## Original warehouse run

Command: `python3 Lab4_Logic/task2_planner.py`

```text
Plan found:
1. PickUp(A)
2. Move(A,B)
3. Move(B,C)
4. Drop(C)
States:
Initial: {(PackageAt, A), (RobotAt, A)}
After PickUp(A): {(Holding, Package), (RobotAt, A)}
After Move(A,B): {(Holding, Package), (RobotAt, B)}
After Move(B,C): {(Holding, Package), (RobotAt, C)}
After Drop(C): {(PackageAt, C), (RobotAt, C)}
```
