"""Compare first- and second-order models on table size and generated text."""

from pathlib import Path
import random

from dataset import SENTENCES
from first_order import FirstOrderModel
from second_order import SecondOrderModel


def render(tokens):
    return " ".join(token for token in tokens if token not in ("<START>", "<END>"))


def table_size(distributions):
    entries = sum(len(distribution) for distribution in distributions.values())
    free_parameters = sum(max(0, len(distribution) - 1) for distribution in distributions.values())
    return entries, free_parameters


def generate_samples(model, order, count=20, seed=42):
    rng = random.Random(seed)
    results = []
    for _ in range(count):
        if order == 1:
            tokens = model.generate(max_tokens=50, rng=rng)
        else:
            tokens = model.generate(max_tokens=50, rng=rng)
        results.append((render(tokens), tokens[-1] == "<END>"))
    return results


def main():
    first = FirstOrderModel(SENTENCES)
    second = SecondOrderModel(SENTENCES)

    first_entries, first_free = table_size(first.probabilities)
    second_entries, second_free = table_size(second.probabilities)
    # Include the second-order model's separate distribution for the first token.
    second_entries += len(second.start_probabilities)
    second_free += max(0, len(second.start_probabilities) - 1)

    vocabulary = {token for sentence in SENTENCES for token in sentence}
    possible_context_tokens = vocabulary - {"<END>"}
    first_zero_contexts = len(possible_context_tokens) - len(first.probabilities)
    possible_pair_contexts = len(possible_context_tokens) ** 2
    second_zero_contexts = possible_pair_contexts - len(second.probabilities)

    first_samples = generate_samples(first, order=1)
    second_samples = generate_samples(second, order=2)
    first_unique = len({text for text, _ in first_samples})
    second_unique = len({text for text, _ in second_samples})
    first_ended = sum(ended for _, ended in first_samples)
    second_ended = sum(ended for _, ended in second_samples)

    lines = [
        "First-order vs second-order model comparison",
        "",
        "Parameter counts (a table entry is one stored conditional probability; free parameters are degrees of freedom per normalized row):",
        f"First order: {first_entries} probability entries; {first_free} free parameters.",
        f"Second order: {second_entries} probability entries, including its initial-token distribution; {second_free} free parameters.",
        "",
        "Unseen context counts (candidate contexts formed from vocabulary tokens, excluding <END>):",
        f"First order: {first_zero_contexts} unseen contexts out of {len(possible_context_tokens)} possible previous-token contexts.",
        f"Second order: {second_zero_contexts} unseen contexts out of {possible_pair_contexts} possible two-token combinations ({len(second.probabilities)} observed). Some combinations are not valid sentence positions, so this is the full vocabulary-pair space.",
        "",
        f"Generated-text diversity over 20 sampled sequences (fixed seed): first order {first_unique}/20 unique, {first_ended}/20 reached <END>; second order {second_unique}/20 unique, {second_ended}/20 reached <END>.",
        "",
        "First-order examples:",
    ]
    lines.extend(f"{i}. {text}" for i, (text, _) in enumerate(first_samples[:5], start=1))
    lines.extend(["", "Second-order examples:"])
    lines.extend(f"{i}. {text}" for i, (text, _) in enumerate(second_samples[:5], start=1))
    lines.extend(
        [
            "",
            "Qualitative comparison:",
            "The first-order model remembers only the immediately previous token, so it can switch between sentence fragments or loop (for example, repeating 'the cat sat on the ...').",
            "The second-order model also conditions on the preceding token, which tends to preserve short phrases and sentence endings seen in the training data. With this tiny corpus, it mostly recombines familiar fragments and has many unseen two-token contexts.",
        ]
    )

    report = "\n".join(lines) + "\n"
    output_path = Path(__file__).with_name("model_comparison.txt")
    output_path.write_text(report, encoding="utf-8")
    print(report, end="")
    print(f"Saved comparison to {output_path.name}.")


if __name__ == "__main__":
    main()
