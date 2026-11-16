"""Task 4 diagnostics: zero-initialisation symmetry and hidden activations."""

import torch
from torch import nn


INPUTS = torch.tensor(
    [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]],
    dtype=torch.float32,
)
TARGETS = torch.tensor([[0.0], [1.0], [1.0], [0.0]], dtype=torch.float32)
SEED = 1
STEPS = 5000
LEARNING_RATE = 0.1


def make_model(activation: nn.Module) -> nn.Sequential:
    return nn.Sequential(nn.Linear(2, 2), activation, nn.Linear(2, 1))


def train(
    model: nn.Sequential,
) -> tuple[float, torch.Tensor, torch.Tensor, float]:
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # Measure the first-layer gradient before the first update as an early-step check.
    optimizer.zero_grad()
    loss_fn(model(INPUTS), TARGETS).backward()
    early_gradient_norm = torch.linalg.vector_norm(model[0].weight.grad).item()

    for _ in range(STEPS):
        optimizer.zero_grad()
        loss = loss_fn(model(INPUTS), TARGETS)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        logits = model(INPUTS)
        final_loss = loss_fn(logits, TARGETS).item()
        probabilities = torch.sigmoid(logits).squeeze(1)
        predictions = (probabilities >= 0.5).to(torch.int64)
    return final_loss, probabilities, predictions, early_gradient_norm


def zero_initialisation_experiment() -> None:
    torch.manual_seed(SEED)
    model = make_model(nn.Sigmoid())
    for parameter in model.parameters():
        nn.init.zeros_(parameter)

    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    checkpoints = {0, 1, 10, 100, STEPS}
    hidden_weight_rows = {}

    for step in range(STEPS + 1):
        if step in checkpoints:
            hidden_weight_rows[step] = model[0].weight.detach().clone()
        if step == STEPS:
            break
        optimizer.zero_grad()
        loss = loss_fn(model(INPUTS), TARGETS)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        logits = model(INPUTS)
        final_loss = loss_fn(logits, TARGETS).item()
        probabilities = torch.sigmoid(logits).squeeze(1)
        predictions = (probabilities >= 0.5).to(torch.int64)

    print("Zero-initialisation symmetry experiment (sigmoid, seed 1):")
    for step, rows in hidden_weight_rows.items():
        print(f"  hidden weight rows after step {step}: {rows.tolist()}")
        print(f"    rows identical: {torch.equal(rows[0], rows[1])}")
    print(f"  final BCE loss: {final_loss:.6f}")
    print("  final probabilities:", probabilities.tolist())
    print("  thresholded labels:", predictions.tolist())


def activation_experiments() -> None:
    activations = {
        "sigmoid": nn.Sigmoid,
        "tanh": nn.Tanh,
        "ReLU": nn.ReLU,
    }
    print("\nHidden activation experiment (seed 1, same training settings):")
    for name, activation_factory in activations.items():
        torch.manual_seed(SEED)
        model = make_model(activation_factory())
        final_loss, probabilities, predictions, early_gradient_norm = train(model)
        correct = (predictions == TARGETS.squeeze(1).to(torch.int64)).sum().item()
        print(f"  {name}:")
        print(f"    final BCE loss: {final_loss:.6f}")
        print(f"    probabilities: {probabilities.tolist()}")
        print(f"    thresholded labels: {predictions.tolist()} ({correct}/4 correct)")
        print(f"    first-layer gradient norm at step 0: {early_gradient_norm:.6g}")


def main() -> None:
    zero_initialisation_experiment()
    activation_experiments()


if __name__ == "__main__":
    main()
