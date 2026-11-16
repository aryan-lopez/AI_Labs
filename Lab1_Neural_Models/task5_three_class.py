"""Task 5: Extend the sensor task to three mutually exclusive classes."""

import torch
from torch import nn


def main() -> None:
    torch.manual_seed(1)

    inputs = torch.tensor(
        [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]],
        dtype=torch.float32,
    )
    # Class 0: both off; class 1: sensors disagree; class 2: both on.
    targets = torch.tensor([0, 1, 1, 2], dtype=torch.int64)

    # Keep the two-input, two-hidden-unit sigmoid representation unchanged.
    model = nn.Sequential(
        nn.Linear(2, 2),
        nn.Sigmoid(),
        nn.Linear(2, 3),
    )
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

    with torch.no_grad():
        initial_loss = loss_fn(model(inputs), targets).item()

    # Train on all four examples as one batch; CrossEntropyLoss takes logits.
    for _ in range(5000):
        optimizer.zero_grad()
        logits = model(inputs)
        loss = loss_fn(logits, targets)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        logits = model(inputs)
        final_loss = loss_fn(logits, targets).item()
        probabilities = torch.softmax(logits, dim=1)
        predictions = probabilities.argmax(dim=1)

        # Adding a common constant to logits should leave softmax unchanged.
        shifted_probabilities = torch.softmax(logits[0] + 100.0, dim=0)

    print(f"Initial cross-entropy loss: {initial_loss:.6f}")
    print(f"Final cross-entropy loss:   {final_loss:.6f}")
    print("Output weight shape:", tuple(model[2].weight.shape))
    print("Output bias shape:", tuple(model[2].bias.shape))
    print("Logits for each input:\n", logits)
    print("Softmax probabilities for each input:\n", probabilities)
    print("Probability sums per input:", probabilities.sum(dim=1).tolist())
    print("Predicted classes:", predictions.tolist())
    print("First-example probabilities after adding 100 to all logits:")
    print(shifted_probabilities)
    print(
        "Maximum softmax change after the shift:",
        (shifted_probabilities - probabilities[0]).abs().max().item(),
    )


if __name__ == "__main__":
    main()
