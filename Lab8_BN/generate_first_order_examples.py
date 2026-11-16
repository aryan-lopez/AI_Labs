"""Print first-order next-token distributions and save 20 sample sentences."""

from pathlib import Path
import random

from dataset import SENTENCES
from first_order import FirstOrderModel


def main():
    model = FirstOrderModel(SENTENCES)

    print("Next-token distributions:")
    for context in ("the", "cat", "dog", "sat", "ran"):
        model.display_distribution(context)

    rng = random.Random(42)
    generated = []
    for _ in range(20):
        tokens = model.generate(rng=rng)
        sentence = [token for token in tokens if token not in ("<START>", "<END>")]
        generated.append(" ".join(sentence))

    output_path = Path(__file__).with_name("first_order_generated.txt")
    output_path.write_text("\n".join(generated) + "\n", encoding="utf-8")

    print(f"\nGenerated 20 sentences and saved them to {output_path.name}:")
    for number, sentence in enumerate(generated, start=1):
        print(f"{number:2}. {sentence}")


if __name__ == "__main__":
    main()
