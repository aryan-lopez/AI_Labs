"""Breadth-first planner for the Lab 4 warehouse planning problem."""

from collections import deque
from dataclasses import dataclass
from typing import FrozenSet, Iterable, Optional, Tuple


Fact = Tuple[str, ...]
State = FrozenSet[Fact]


@dataclass(frozen=True)
class Action:
    """A ground action with positive/negative conditions and effects."""

    name: str
    positive_preconditions: FrozenSet[Fact]
    negative_preconditions: FrozenSet[Fact]
    positive_effects: FrozenSet[Fact]
    negative_effects: FrozenSet[Fact]


@dataclass
class PlanResult:
    """A plan and the states reached after its actions, if one exists."""

    actions: Tuple[Action, ...]
    states: Tuple[State, ...]


def make_action(
    name: str,
    positive_preconditions: Iterable[Fact] = (),
    negative_preconditions: Iterable[Fact] = (),
    positive_effects: Iterable[Fact] = (),
    negative_effects: Iterable[Fact] = (),
) -> Action:
    """Create an action while storing all conditions/effects immutably."""
    return Action(
        name=name,
        positive_preconditions=frozenset(positive_preconditions),
        negative_preconditions=frozenset(negative_preconditions),
        positive_effects=frozenset(positive_effects),
        negative_effects=frozenset(negative_effects),
    )


def is_applicable(action: Action, state: State, static_facts: State) -> bool:
    """Check that every required fact is present and every forbidden fact absent."""
    known_facts = state | static_facts
    return (
        action.positive_preconditions <= known_facts
        and action.negative_preconditions.isdisjoint(known_facts)
    )


def apply_action(action: Action, state: State) -> State:
    """Return the successor state after applying the action's add/delete effects."""
    return (state - action.negative_effects) | action.positive_effects


def breadth_first_plan(
    initial_state: State,
    goal_positive: State,
    actions: Tuple[Action, ...],
    static_facts: State = frozenset(),
    goal_negative: State = frozenset(),
) -> Optional[PlanResult]:
    """Return a shortest plan, or None if the finite state space has no plan."""

    def is_goal(state: State) -> bool:
        known_facts = state | static_facts
        return goal_positive <= known_facts and goal_negative.isdisjoint(known_facts)

    frontier = deque([initial_state])
    # Each discovered state is enqueued once; its parent/action reconstruct a plan.
    parent = {initial_state: None}
    action_used = {}

    while frontier:
        state = frontier.popleft()
        if is_goal(state):
            plan = []
            states = [state]
            current = state
            while parent[current] is not None:
                previous = parent[current]
                plan.append(action_used[current])
                current = previous
                states.append(current)
            plan.reverse()
            states.reverse()
            return PlanResult(tuple(plan), tuple(states))

        for action in actions:
            if not is_applicable(action, state, static_facts):
                continue
            successor = apply_action(action, state)
            if successor in parent:
                continue
            parent[successor] = state
            action_used[successor] = action
            frontier.append(successor)

    return None


def warehouse_actions() -> Tuple[Action, ...]:
    """Instantiate the legal moves, pickups, and drops for locations A, B, C."""
    connections = (("A", "B"), ("B", "A"), ("B", "C"), ("C", "B"))
    actions = []

    for source, destination in connections:
        actions.append(
            make_action(
                f"Move({source},{destination})",
                positive_preconditions={
                    ("RobotAt", source),
                    ("Connected", source, destination),
                },
                positive_effects={("RobotAt", destination)},
                negative_effects={("RobotAt", source)},
            )
        )

    for location in ("A", "B", "C"):
        actions.append(
            make_action(
                f"PickUp({location})",
                positive_preconditions={
                    ("RobotAt", location),
                    ("PackageAt", location),
                },
                positive_effects={("Holding", "Package")},
                negative_effects={("PackageAt", location)},
            )
        )
        actions.append(
            make_action(
                f"Drop({location})",
                positive_preconditions={
                    ("RobotAt", location),
                    ("Holding", "Package"),
                },
                positive_effects={("PackageAt", location)},
                negative_effects={("Holding", "Package")},
            )
        )

    return tuple(actions)


def format_state(state: State) -> str:
    """Render the dynamic propositions in a stable, readable order."""
    facts = sorted(state)
    return "{" + ", ".join("(" + ", ".join(fact) + ")" for fact in facts) + "}"


def main() -> None:
    """Solve the supplied warehouse problem and print the plan and state trace."""
    initial_state = frozenset({("RobotAt", "A"), ("PackageAt", "A")})
    static_facts = frozenset(
        {
            ("Connected", "A", "B"),
            ("Connected", "B", "A"),
            ("Connected", "B", "C"),
            ("Connected", "C", "B"),
        }
    )
    goal = frozenset({("PackageAt", "C")})

    result = breadth_first_plan(
        initial_state=initial_state,
        goal_positive=goal,
        actions=warehouse_actions(),
        static_facts=static_facts,
    )

    if result is None:
        print("No plan found")
        return

    print("Plan found:")
    for index, action in enumerate(result.actions, start=1):
        print(f"{index}. {action.name}")
    print("States:")
    for index, state in enumerate(result.states):
        label = "Initial" if index == 0 else f"After {result.actions[index - 1].name}"
        print(f"{label}: {format_state(state)}")


if __name__ == "__main__":
    main()
