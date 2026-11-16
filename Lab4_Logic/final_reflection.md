# Final Reflection

### 1. Why is it useful to specify action preconditions and effects before asking an LLM to write the planner?

Preconditions and effects define what each action is allowed to do and how it
changes the world. Specifying them first gives the LLM a precise model to
implement, helps prevent it from inventing behavior, and makes the code easier
to review. In this warehouse, stating that pickup requires the robot and
package to share a location makes it clear why `PickUp(A)` is initially valid
and `Drop(C)` is not.

### 2. Give an example of an error that could occur if the planner failed to check an action's preconditions.

If the planner applied `Drop(C)` while the robot was still at `A`, it could add
`PackageAt(C)` to the state even though the robot had never carried the
package to `C`. The planner might then report success for an impossible plan.

### 3. Why is a plan that “looks reasonable” not necessarily a valid plan?

A sequence of action names can sound plausible while violating a precondition
or producing an incorrect state transition. For example, moving the robot to
`C` does not deliver a package left at `B`. A plan is valid only when each
action is applicable in the state where it is used, its effects are applied
correctly, and the resulting final state satisfies the goal. Task 3's tests
checked these properties explicitly.

### 4. What did the LLM contribute to the implementation?

The LLM translated the planning specification into a Python implementation:
an action representation, precondition and effect handling, breadth-first
search, path reconstruction, and readable plan/state output. The prompt and
resulting program are recorded in Task 2. The LLM provided the implementation
starting point; the warehouse model and requirements were specified in the
earlier tasks.

### 5. What did you have to verify independently?

I needed to check that the action definitions match the warehouse, that
preconditions are checked before effects are applied, and that the goal means
`PackageAt(C)` rather than simply `RobotAt(C)`. The returned sequence and
state trace should also be checked against the specified action preconditions
and effects. Task 3 exercised the original problem, a version without pickup,
and a movement-only case; it confirmed that the original has a valid plan,
removing pickup makes the goal unreachable, and robot movement alone does not
satisfy the package goal.

### 6. In this laboratory, where is logical reasoning being used?

Logical reasoning is used when the planner checks whether an action's
preconditions are true in the current state and when it applies the action's
effects to infer the successor state. For example, `PickUp(A)` follows from
`RobotAt(A)` and `PackageAt(A)`. The `Connected` facts also determine which
movement actions are allowed.

### 7. How is planning related to the search algorithms studied in the previous module?

Planning can be formulated as search over states. Here, each state is a set of
facts, applicable actions generate successor states, and BFS explores those
states until it finds one satisfying the goal. Since each action has equal
cost, BFS finds a plan with the fewest actions. The search algorithms from the
previous module provide the strategy for exploring alternatives; the logical
action model defines the states and transitions being searched.
