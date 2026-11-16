"""Generate and compare five greedy and five sampled first-order sequences."""

from pathlib import Path
import random

from dataset import SENTENCES
from first_order import FirstOrderModel


def render(tokens):
    return " ".join(token for token in tokens if token not in ("<START>", "<END>"))


def main():
    model = FirstOrderModel(SENTENCES)
    sample_rng = random.Random(42)
    max_tokens = 30

    greedy = [model.generate_greedy(max_tokens=max_tokens) for _ in range(5)]
    sampled = [model.generate(max_tokens=max_tokens, rng=sample_rng) for _ in range(5)]

    lines = ["Greedy generation (argmax):"]
    for number, tokens in enumerate(greedy, start=1):
        ending = "reached <END>" if tokens[-1] == "<END>" else "stopped at token limit"
        lines.append(f"{number}. {render(tokens)} [{ending}]")

    lines.append("")
    lines.append("Sampling generation:")
    for number, tokens in enumerate(sampled, start=1):
        ending = "reached <END>" if tokens[-1] == "<END>" else "stopped at token limit"
        lines.append(f"{number}. {render(tokens)} [{ending}]")

    greedy_unique = len({tuple(tokens) for tokens in greedy})
    sampled_unique = len({tuple(tokens) for tokens in sampled})
    lines.extend(
        [
            "",
            f"Distinct sequences: greedy {greedy_unique}/5; sampling {sampled_unique}/5.",
            "Greedy repeats the same highest-probability path, while sampling can choose different next tokens according to their probabilities.",
            "If greedy generation reaches the token limit, its argmax choices are cycling without selecting <END>.",
        ]
    )

    output_path = Path(__file__).with_name("generation_mode_comparison.txt")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nSaved comparison to {output_path.name}.")


if __name__ == "__main__":
    main()
