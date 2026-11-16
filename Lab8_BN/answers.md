# BN Lab: Answers to Questions 1–14

These answers follow the questions in `BN_lab.pdf` and use the six-sentence dataset in `dataset.py`. The implementation-specific answers refer to `first_order.py` and `second_order.py`.

## Question 1

**Why is this decomposition useful for generating text?**

The chain rule writes the probability of a complete sentence as a sequence of next-token probabilities. A generator can therefore start with the beginning token, choose one token at a time from the relevant conditional distribution, and stop when it generates `<END>`. It does not need to score or enumerate every possible complete sentence before generating one.

## Question 2

**What independence assumption is being made by this network? Express your answer using probability notation.**

The first-order network assumes that once the immediately preceding token is known, earlier tokens add no information about the next token:

\[
P(X_t \mid X_1,\ldots,X_{t-1}) = P(X_t \mid X_{t-1}), \qquad t \ge 2.
\]

Equivalently, \(X_t\) is conditionally independent of \(X_1,\ldots,X_{t-2}\) given \(X_{t-1}\).

## Question 3

**Construct the conditional probability distribution \(P(\text{next word} \mid \text{current word})\) for at least the following words: `the`, `cat`, `dog`, `sat`, `ran`. Identify any zero-probability transitions.**

Using the six lab sentences, the distributions are:

| Current word | Next word probabilities |
|---|---|
| `the` | `cat`: \(3/12=0.25\); `dog`: \(3/12=0.25\); `mat`: \(2/12=1/6\); `rug`: \(2/12=1/6\); `park`: \(2/12=1/6\) |
| `cat` | `sat`: \(2/3\); `ran`: \(1/3\) |
| `dog` | `sat`: \(2/3\); `ran`: \(1/3\) |
| `sat` | `on`: \(1\) |
| `ran` | `to`: \(1\) |

Every other vocabulary token has probability zero after each listed context. For example, `the` is never followed by `<END>`, and `sat` is never followed by `mat` in this dataset. The nonzero values for each row sum to 1.

## Question 4

**Where in the program are the transition counts stored?**

In `first_order.py`, `self.transition_counts` is a nested mapping: the current token maps to a `Counter` of next-token counts. For example, the entry for `the` counts how often it is followed by `cat`, `dog`, `mat`, `rug`, or `park`.

## Question 5

**Where is \(P(X_t \mid X_{t-1})\) computed?**

In `FirstOrderModel.__init__`, the code sums the outgoing counts for each current token and divides each next-token count by that total. The resulting conditional distributions are stored in `self.probabilities`.

## Question 6

**How does the program choose the next word? Is it always choosing the most probable word, or sampling from the probability distribution? Explain the difference.**

`generate()` samples using `random.choices`, weighted by the conditional probabilities. Sampling can choose a less probable next word, with a chance proportional to its probability. `most_probable_next()` returns an argmax choice instead; `generate_greedy()` repeatedly uses that choice. Greedy generation is deterministic for this implementation, including its tie behavior, while sampling can produce different continuations.

## Question 7

**What happens if the program encounters a word for which no transition has been observed?**

`distribution()` returns an empty dictionary. `most_probable_next()` returns `None`, and `generate()` stops if it reaches that context because it has no distribution to sample from. The model does not invent a transition or apply smoothing.

## Question 8

**If one of the totals is 0.87, what does this tell you about the implementation?**

The conditional probabilities for that context are not normalized: they should sum to approximately 1. A total of 0.87 suggests a counting, denominator, or probability-construction error, such as leaving out observed transitions or dividing by the wrong total. The normalization check in `first_order.py` reports 1.0 for every observed context on this dataset.

## Question 9

**Are the most probable predictions always the same as the words that you would personally expect? What does this tell you about the difference between a probability model and human linguistic expectations?**

Not necessarily. The model selects what was most frequent after a context in this tiny training set; it does not use broader grammar, meaning, or conversational intent. For example, after `the`, the most frequent continuations are `cat` and `dog`, tied at 0.25. This illustrates that a probability model reflects its data and assumptions, while a person may draw on much broader linguistic knowledge and context.

## Question 10

**Compare the two sets of generated sentences. Which mode produces more variation? Why?**

Sampling produces more variation because it can choose any observed continuation according to its probability. Greedy generation always follows the same highest-probability path. In the saved run (`generation_mode_comparison.txt`, seed 42), greedy produced 1 distinct sequence out of 5 and cycled until the token limit; sampling produced 4 distinct sequences out of 5 and all reached `<END>`. The first-order model can repeat fragments because it conditions on only one previous token.

## Question 11

**How does the second-order model differ from the first-order model in terms of (1) graph structure, (2) the conditional probability table, (3) the amount of context available for prediction, and (4) the amount of data needed?**

1. **Graph structure:** First order has one parent for each token, \(X_{t-1}\to X_t\). Second order has two parents, \(X_{t-2}\to X_t\leftarrow X_{t-1}\).
2. **Conditional probability table:** First order has a row for each previous token; second order has a row for each pair of previous tokens. The second-order table is larger and sparser in this dataset.
3. **Context:** First order uses only the immediately previous token. Second order uses the two immediately previous tokens.
4. **Data needed:** Second order needs more data because counts are split across pairs of context tokens. Many pairs may have few or no observations.

## Question 12

**Why does increasing the amount of context potentially improve prediction? Why can it simultaneously make the model harder to estimate from limited data? Relate your answer to the size of the conditional probability table.**

More context can distinguish cases that look identical under a shorter context. For example, the preceding two words can provide a more specific clue about the next word than the last word alone. But with a vocabulary of size \(V\), a first-order table can have about \(V\) contexts and \(V\) possible next tokens per context, while a second-order table can have about \(V^2\) contexts and \(V\) possible next tokens per context. The larger table needs many more observations; with limited data, many rows remain unseen or poorly estimated.

## Question 13

**Why is Approach B preferable when constructing an intelligent system? Discuss the importance of specifying the intended behaviour, understanding the representation, validating the generated implementation, testing probabilistic invariants, and distinguishing implementation from model.**

Approach B states the model behavior precisely: estimate \(P(X_t\mid X_{t-1})\) from transition counts and generate by sampling. That makes the representation and intended computation clear before code is written. The implementation can then be checked against that specification: confirm it counts the right transitions, computes each conditional distribution correctly, and samples rather than silently switching to greedy choice. Invariants such as each row summing to 1 provide concrete checks. Keeping the model (the specified probability distribution) distinct from its implementation (the Python code) makes it possible to identify whether an error is in the mathematical design or in the code.

## Question 14

**What did thinking of the language model as a Bayesian network give you? Discuss at least three of the following: a representation of dependencies; a factorisation of the joint distribution; a way of interpreting conditional probabilities; a principled method for generation; a way to reason about independence assumptions; a way to understand the effect of increasing context; a way to test whether an implementation matches its probabilistic specification.**

Thinking of the model as a Bayesian network made the token dependencies explicit: in the first-order model, each token depends on the previous token; in the second-order model, it depends on the previous two. It also showed how the joint probability of a sentence factors into conditional probabilities, which gives a principled way to generate a sentence one token at a time. Finally, the graph makes the independence assumption visible and helps explain how increasing context changes the model and its probability tables. The normalization checks then test whether the code implements valid conditional distributions as specified.
