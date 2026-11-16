# Final Reflection

### 1. Why is it important to formulate the search problem before writing the search algorithm?

Formulating the problem first makes clear what a state represents, which actions are valid, how actions change the state, where the search begins, what counts as a goal, and how path cost is measured. These choices determine what the algorithm must search over and what a correct solution means. In this warehouse, defining a state as a grid position and each legal move as unit cost made it possible to choose an appropriate representation and verify that the returned path reaches the goal without crossing obstacles. Without that formulation, an implementation could solve a different problem or appear to work while producing invalid results.

### 2. In what sense is A* an “informed” search algorithm?

A* is informed because it uses a heuristic estimate of the remaining cost to the goal when deciding which state to explore next. It combines that estimate, `h(n)`, with the actual cost from the start, `g(n)`, as `f(n) = g(n) + h(n)`. The heuristic gives the search direction based on knowledge about the problem; for this grid, Manhattan distance estimates how many orthogonal moves remain. A* still accounts for the cost already paid, so it balances progress so far with estimated distance to the goal.

### 3. Why does the choice of heuristic matter?

The heuristic affects which states A* prioritizes, so it can change how much of the search space is explored and whether the shortest-path guarantee holds. A useful admissible heuristic, such as Manhattan distance for four-direction unit-cost movement, guides the search without overestimating the remaining cost. A weaker heuristic such as zero provides less direction and behaves like uniform-cost search, while an overestimate such as twice Manhattan can be more aggressive but may sacrifice optimality. The experiments showed that different heuristics can produce different expansion counts even when they return the same path length on this particular map.

### 4. What did the LLM contribute to the engineering process?

The LLM translated the design into a documented Python A* implementation and provided a starting point for the engineering work. The recorded prompt specified the map, movement rules, Manhattan heuristic, frontier, path reconstruction, and required output. The implementation then served as a hypothesis to inspect and test. Additional work extended A* to accept heuristic variants and added BFS for comparison. The LLM helped with implementation, while the problem formulation, review of the code, interpretation of results, and validation remained part of the engineering process.

### 5. What could go wrong if an engineer simply accepted LLM-generated code without testing it?

The code could contain errors that are not obvious from a plausible-looking output: it might allow invalid moves, fail to terminate when the goal is unreachable, report the wrong path length, or return a non-shortest route. It could also implement assumptions that differ from the actual problem. In this lab, the separate trivial, unreachable, and alternative-path tests checked behaviors that the original warehouse run alone could not establish. Testing is necessary to find such problems and to determine whether the program's behavior matches its requirements before relying on it.
