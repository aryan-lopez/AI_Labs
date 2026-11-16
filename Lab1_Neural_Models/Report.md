# Task 1: Problem specification and linear-model prediction

## Problem specification

The device receives two binary sensor readings, so the input space is
\(X = \{(0,0), (0,1), (1,0), (1,1)\}\). It must return a binary
sensor-disagreement warning, so the output space is \(Y = \{0,1\}\).
The warning is on exactly when the sensors disagree (XOR):

| Sensor 1 | Sensor 2 | Warning |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

## Prediction for a linear model

A single affine transformation followed by a sigmoid has a straight-line
decision boundary in this two-dimensional input space. It cannot separate
the two warning examples, \((0,1)\) and \((1,0)\), from the two no-warning
examples, \((0,0)\) and \((1,1)\), because the classes occupy alternating
corners of the square. Therefore, I predict that this linear model will not
classify all four examples correctly, even after training. Its loss may
decrease, but it should not reach a perfect fit; at a 0.5 threshold, it can
get at most three of the four labels correct. A nonlinear hidden layer is
needed to represent this XOR rule.

## Task 2: Neural model design and validation

### Model design

I will use a fully connected network with two input values, two hidden units,
and one output. The hidden layer will use a sigmoid activation, and the output
will use a sigmoid so its value can be interpreted as the probability of a
warning. I will train it with binary cross-entropy (BCE) and gradient-based
optimisation.

In equations, for input \(x = (x_1,x_2)\), the model is

\[
h = \sigma(W_1x + b_1), \qquad
\hat{y} = \sigma(W_2h + b_2),
\]

where \(h\) contains the two hidden activations, \(\hat{y}\) is the predicted
warning probability, and \(\sigma(z)=1/(1+e^{-z})\). The prediction is 1 when
\(\hat{y} \ge 0.5\), and 0 otherwise.

### Why use a nonlinear hidden layer?

Without a nonlinear activation, composing the two affine layers is equivalent
to one affine transformation. It would still have only a straight-line
decision boundary and could not represent XOR. The hidden sigmoid units make
the overall input-to-output mapping nonlinear, allowing the network to
separate the alternating corner labels.

### Output and loss choice

The target is a single yes/no label, so one sigmoid output gives a probability
for the positive class. Binary cross-entropy compares that probability with
the target label and penalizes confident wrong predictions. These choices
match the binary classification task. (In a PyTorch implementation, the
equivalent numerically stable setup is to output a raw logit and use
`BCEWithLogitsLoss`, applying sigmoid only when displaying probabilities.)

### What will count as successful learning?

I will check the following after training:

1. The final BCE loss is substantially lower than the initial loss.
2. Thresholding the four predicted probabilities at 0.5 gives the target
   labels \([0,1,1,0]\) for inputs \([(0,0),(0,1),(1,0),(1,1)]\).
3. The predicted probabilities for the positive examples are above 0.5 and
   those for the negative examples are below 0.5, with the four probabilities
   recorded for inspection.
4. The parameter gradients are finite and nonzero during learning, indicating
   that the model received an update signal.

## Task 3: First implementation

I asked for a concise PyTorch implementation of the Task 2 design, with the
four XOR examples, a 2–2–1 network, sigmoid hidden units, one output logit
trained with `BCEWithLogitsLoss`, random weight initialisation, a fixed seed,
and full-batch CPU training for a few thousand steps. I also requested the
initial and final loss, all four final probabilities and thresholded labels,
and one parameter-gradient tensor.

**Prompt used:**

> Write concise PyTorch code for the XOR sensor-warning task from this write-up. Use the four examples `(0,0)->0`, `(0,1)->1`, `(1,0)->1`, `(1,1)->0` and exactly a 2-input, 2-hidden-unit, 1-output network. Use sigmoid hidden activations and one output logit trained with `BCEWithLogitsLoss`; use random weight initialisation, set a reproducible random seed, and train full-batch on CPU for a few thousand steps. Do not change the architecture or task. Print the initial and final loss, all four final probabilities, their labels thresholded at 0.5, and one parameter-gradient tensor after a final backward pass. Add a one-sentence explanation for each reported check. Do not execute the code.

**Code review before execution:** The forward pass returns logits to
`BCEWithLogitsLoss`, sigmoid is applied only to produce reported
probabilities, and the final backward pass populates the displayed first-layer
weight gradient. No code corrections were needed before the first run. The
script is saved as [`task3_xor.py`](task3_xor.py); Task 4 records the seed
adjustment made after checking its first run.

The initial and final losses show whether optimisation reduced the training
error; the four probabilities show the model's confidence on each input; the
thresholded labels show whether it learned the required XOR mapping; and the
first-layer weight gradient shows the direction and size of the loss signal
for those weights at the final parameters.

## Task 4: Execution, tests, and diagnosis

I installed CPU-only PyTorch 2.14.1 in a Python virtual environment and ran
the implementation. The first run used seed 7, reduced BCE loss from 0.700702
to 0.477390, but predicted `[0, 1, 1, 1]`, so it got only 3/4 labels right.
Following the lab instructions, I changed only the random seed to 1 and kept
the architecture, activation, optimizer, learning rate, and 5,000 full-batch
steps unchanged.

### Successful baseline run (seed 1)

| Measurement | Result |
|---|---|
| Initial BCE loss | 0.702770 |
| Final BCE loss | 0.000026 |
| Probabilities for `(0,0), (0,1), (1,0), (1,1)` | 0.0000395, 0.999976, 0.999976, 0.0000178 |
| Thresholded labels | `[0, 1, 1, 0]` (4/4 correct) |

The first-layer weight gradient after the final backward pass was
`[[-3.67e-8, -2.88e-8], [-2.86e-7, -3.27e-7]]`. Each entry is the loss
derivative with respect to one first-layer weight; these small values are
consistent with the model being near a fitted solution. The loss decrease and
correct labels show useful learning beyond the existence of a nonzero
gradient alone.

### Backpropagation and symmetry checks

I set every weight and bias to zero, then trained the unchanged sigmoid
network for the same 5,000 steps. The two hidden-unit weight rows were
identical at steps 0, 1, 10, 100, and 5,000 (in fact, both remained
`[0, 0]`). The final loss was 0.693147, all four probabilities were 0.5,
and thresholding produced `[1, 1, 1, 1]` (2/4 correct). Identical hidden units
receive identical gradients, so zero initialisation preserves their symmetry
and does not let them learn distinct features.

### Hidden-activation comparison

Each run used seed 1, the same 2–2–1 architecture, Adam learning rate 0.1,
and 5,000 full-batch steps; only the hidden activation changed. The gradient
norm is the Euclidean norm of the first-layer weight gradient before the
first parameter update.

| Hidden activation | Final BCE loss | Thresholded labels | Early first-layer gradient norm |
|---|---:|---|---:|
| Sigmoid | 0.000026 | `[0, 1, 1, 0]` (4/4) | 0.004304 |
| Tanh | 0.346576 | `[0, 1, 0, 0]` (3/4) | 0.018582 |
| ReLU | 0.477386 | `[0, 1, 0, 0]` (3/4) | 0.019311 |

For this seed and training setup, sigmoid learned all four labels, while tanh
and ReLU did not; the larger early gradient norms for tanh and ReLU did not
mean they achieved better final classification. This is an observation from
these small runs, not evidence that sigmoid is universally best. The
diagnostic code is in [`task4_diagnostics.py`](task4_diagnostics.py).

The baseline was run with the CPU-only PyTorch virtual environment at
`/tmp/lab1-venv`; the workspace-mounted `Lab1/.venv` installation stalled
during extraction, so it was not used for the reported runs.

## Task 5: Three-class extension

I recoded the target as three mutually exclusive classes: class 0 means both
sensors are off, class 1 means they disagree, and class 2 means both are on.
In the four-example order used above, the class targets are `[0, 1, 1, 2]`.

### Prediction before running

Only the output layer and loss change from Task 3: the final layer has three
logits, so its weight matrix should have shape `(3, 2)` and its bias shape
`(3,)`; each example should produce three logits. Softmax exponentiates and
normalises those logits, so the three class probabilities for each example
should sum to 1. For cross-entropy with a one-hot target, the logit gradient
should be `p - y`, where `p` is the softmax vector and `y` is the one-hot
label vector. This follows by differentiating cross-entropy through softmax:
the derivative of the log-sum-exp term contributes `p`, while the target
logit contributes `-y`.

### Implementation and results

The two-input/two-hidden-unit sigmoid network, seed 1, Adam learning rate 0.1,
and 5,000 full-batch steps were kept the same. I changed the output layer to
three logits and used `CrossEntropyLoss` with integer class targets. The
implementation is in [`task5_three_class.py`](task5_three_class.py).

The initial cross-entropy loss was 1.232794 and the final loss was 0.000026.
The learned output weight shape was `(3, 2)` and its bias shape was `(3,)`.
The resulting probabilities were:

| Input | Class 0 | Class 1 | Class 2 | Predicted class |
|---|---:|---:|---:|---:|
| `(0, 0)` | 0.99997 | 0.0000316 | 0.0000000000583 | 0 |
| `(0, 1)` | 0.0000116 | 0.99998 | 0.0000103 | 1 |
| `(1, 0)` | 0.0000107 | 0.99998 | 0.0000104 | 1 |
| `(1, 1)` | 0.0000000000486 | 0.0000294 | 0.99997 | 2 |

Each row's probabilities summed to 1. As the optional stability check, I added
100 to all three logits for `(0, 0)`; its softmax probabilities were unchanged
to floating-point precision (maximum difference about `2.2e-16`). This works
because adding a common constant multiplies every exponentiated logit by the
same factor, which cancels during normalisation.

## Reflection questions

1. **What did the XOR experiment demonstrate about depth and nonlinearity?**
   Adding an affine layer without a nonlinear activation still composes to a
   single affine map, so depth alone cannot separate XOR's alternating
   corners. The nonlinear hidden layer made the required decision rule
   representable, and the trained 2–2–1 network classified all four examples.

2. **What showed that backpropagation supplied a useful learning signal?**
   With seed 1, training reduced BCE from 0.702770 to 0.000026 and changed the
   predictions to all four correct XOR labels. The gradients were finite, and
   the loss and predictions improved together; a nonzero gradient by itself
   would not have shown that learning succeeded.

3. **Why did identical or zero initialisation stop the hidden units learning distinct features?**
   Identical hidden units compute the same activations and receive the same
   gradients, so updates preserve their symmetry. In the all-zero run, both
   hidden weight rows stayed `[0, 0]`; because the output weights also began
   at zero, the first-layer gradient was initially zero as well. The network
   consequently stayed at 0.5 probabilities and did not learn XOR.

4. **How did the hidden activation affect the observed gradients and results?**
   In these runs, the early first-layer gradient norms were 0.004304 for
   sigmoid, 0.018582 for tanh, and 0.019311 for ReLU. Sigmoid's derivative can
   become small when its units saturate; tanh also saturates away from zero,
   while ReLU has zero derivative for negative pre-activations. The measured
   engineering outcomes were 4/4 correct for sigmoid and 3/4 for tanh and
   ReLU. These results describe this seed and setup: the larger early norms
   did not guarantee better final classification and do not establish a
   universally best activation.

5. **Why must the output layer and loss match the task?**
   For binary warning prediction, one logit with `BCEWithLogitsLoss` represents
   one yes/no target. For the three mutually exclusive classes, three logits
   with `CrossEntropyLoss` represent one choice among three classes. The loss
   determines how outputs and targets are interpreted and what gradients are
   produced, so the output shape and target format must match it.

6. **How did the LLM help, and where was human verification essential?**
   It helped draft the repetitive PyTorch model and training loop from the
   written design. Verification was essential: the first run looked plausible
   and lowered loss, but with seed 7 it classified only 3/4 examples. Checking
   the actual labels exposed the miss; changing only the seed gave a run with
   all four labels correct. I also checked tensor shapes, probability sums,
   and the softmax shift diagnostic instead of relying on code appearance.

7. **Which tests should remain if the model scales, and which become too expensive?**
   I would keep checks for input/output shapes, label ranges, finite loss and
   gradients, and task-level performance on representative data. I would also
   keep small reproducible runs and occasional sampled gradient checks. An
   exhaustive finite-difference check for every parameter would become costly:
   it requires many extra forward evaluations as the parameter count grows.
   Sampling a few parameters on a small batch is a practical gradient check.