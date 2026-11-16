# LLM use and validation reflection

I used an LLM only for the parts of this lab where the assignment permits it. I treated its suggestions as drafts and checked them against the lab's model definitions and the six-sentence dataset rather than assuming they were correct.

One code example I inspected was the first-order transition-counting loop in `first_order.py`:

```python
for current_token, next_token in zip(sentence, sentence[1:]):
    self.transition_counts[current_token][next_token] += 1
```

I checked that pairing each token with the following token counts adjacent transitions, including transitions to `<END>`. For example, `the` is followed by `cat` three times in the dataset, and by `dog`, `mat`, `rug`, and `park` three, two, two, and two times respectively. Those counts total 12, matching the saved conditional probabilities for `the` (including `P(cat | the) = 3/12`).

I also checked that each observed conditional-probability row sums to 1, as required by the model, and reviewed the fixed-seed generation comparisons. The results show the expected difference: greedy first-order generation follows the same highest-probability path and hits the token limit, while sampling produces varied sequences. These checks helped me catch whether the implementation matched the intended probability model, rather than judging it only by whether it ran.
