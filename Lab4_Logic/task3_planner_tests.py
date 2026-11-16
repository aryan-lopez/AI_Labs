"""Required Task 3 checks for the Lab 4 breadth-first planner."""

from task2_planner import (
    State,
    apply_action,
    breadth_first_plan,
    is_applicable,
    warehouse_actions,
)


INITIAL = frozenset({("RobotAt", "A"), ("PackageAt", "A")})
STATIC_FACTS = frozenset(
    {
        ("Connected", "A", "B"),
        ("Connected", "B", "A"),
        ("Connected", "B", "C"),
        ("Connected", "C", "B"),
    }
)
GOAL = frozenset({("PackageAt", "C")})


def verify_plan(initial: State, actions, states, static_facts: State) -> None:
    """Independently replay every returned action and compare each state."""
    assert states[0] == initial, "The trace does not start at the supplied state"
    assert len(states) == len(actions) + 1, "There must be a state per action step"
    state = initial
    for index, action in enumerate(actions):
        assert is_applicable(action, state, static_facts), (
            f"Action {action.name} is inapplicable at step {index + 1}"
        )
        state = apply_action(action, state)
        assert state == states[index + 1], (
            f"Reported state is wrong after action {action.name}"
        )
    assert GOAL <= state | static_facts, "The final state does not satisfy the goal"


def test_solvable_problem() -> None:
    result = breadth_first_plan(
        initial_state=INITIAL,
        goal_positive=GOAL,
        actions=warehouse_actions(),
        static_facts=STATIC_FACTS,
    )
    assert result is not None, "Expected a plan for the original warehouse"
    verify_plan(INITIAL, result.actions, result.states, STATIC_FACTS)
    print("Test A — solvable warehouse: plan found and every transition is valid")
    print("  " + " -> ".join(action.name for action in result.actions))


def test_no_pickup_action() -> None:
    actions = tuple(
        action for action in warehouse_actions() if not action.name.startswith("PickUp(")
    )
    result = breadth_first_plan(
        initial_state=INITIAL,
        goal_positive=GOAL,
        actions=actions,
        static_facts=STATIC_FACTS,
    )
    assert result is None, "Expected no plan when pickup is impossible"
    print("Test B — pickup actions removed: no plan found")


def test_robot_at_goal_is_not_package_at_goal() -> None:
    # The robot can walk from B to C, but no pickup or drop action is available.
    initial = frozenset({("RobotAt", "B"), ("PackageAt", "B")})
    move_b_c = next(
        action for action in warehouse_actions() if action.name == "Move(B,C)"
    )
    reachable_state = apply_action(move_b_c, initial)
    assert ("RobotAt", "C") in reachable_state
    assert ("PackageAt", "B") in reachable_state
    assert GOAL.isdisjoint(reachable_state)

    move_only_actions = tuple(
        action for action in warehouse_actions() if action.name.startswith("Move(")
    )
    result = breadth_first_plan(
        initial_state=initial,
        goal_positive=GOAL,
        actions=move_only_actions,
        static_facts=STATIC_FACTS,
    )
    assert result is None, "RobotAt(C) must not satisfy the PackageAt(C) goal"
    print("Test C — robot reaches C while package stays at B: no plan found")


def main() -> None:
    test_solvable_problem()
    test_no_pickup_action()
    test_robot_at_goal_is_not_package_at_goal()
    print("All three required checks passed.")


if __name__ == "__main__":
    main()
