"""Task 3: Train a 2-2-1 PyTorch network on the four XOR examples."""

import torch
from torch import nn


def main() -> None:
    # Fix the seed so the initial weights and run can be reproduced.
    torch.manual_seed(1)

    # Keep all four labeled examples together for full-batch training.
    inputs = torch.tensor(
        [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]],
        dtype=torch.float32,
    )
    targets = torch.tensor([[0.0], [1.0], [1.0], [0.0]], dtype=torch.float32)

    # The model has two sigmoid hidden units and one output logit.
    model = nn.Sequential(
        nn.Linear(2, 2),
        nn.Sigmoid(),
        nn.Linear(2, 1),
    )
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

    # Save the starting loss to compare with the trained model.
    with torch.no_grad():
        initial_loss = loss_fn(model(inputs), targets).item()

    # Reuse the entire four-example dataset for each CPU training step.
    for _ in range(5000):
        optimizer.zero_grad()
        logits = model(inputs)
        loss = loss_fn(logits, targets)
        loss.backward()
        optimizer.step()

    # Recompute loss and gradients at the final parameters for inspection.
    optimizer.zero_grad()
    final_logits = model(inputs)
    final_loss = loss_fn(final_logits, targets)
    final_loss.backward()

    probabilities = torch.sigmoid(final_logits.detach()).squeeze(1)
    predictions = (probabilities >= 0.5).to(torch.int64)
    first_layer_weight_gradient = model[0].weight.grad.detach().clone()

    print(f"Initial BCE loss: {initial_loss:.6f}")
    print(f"Final BCE loss:   {final_loss.item():.6f}")
    print("Final probabilities:", probabilities.tolist())
    print("Thresholded labels:", predictions.tolist())
    print("First-layer weight gradient after final backward():")
    print(first_layer_weight_gradient)


if __name__ == "__main__":
    main()
