"""Second-order Markov language model for the BN lab dataset."""

from collections import Counter, defaultdict
import random

from dataset import SENTENCES


class SecondOrderModel:
    """Estimate P(next_token | previous_two_tokens) from triple counts."""

    def __init__(self, sentences):
        self.transition_counts = defaultdict(Counter)
        self.start_counts = Counter()

        for sentence in sentences:
            if len(sentence) >= 2 and sentence[0] == "<START>":
                self.start_counts[sentence[1]] += 1

            for first, second, next_token in zip(sentence, sentence[1:], sentence[2:]):
                self.transition_counts[(first, second)][next_token] += 1

        self.probabilities = {}
        for context, next_counts in self.transition_counts.items():
            total = sum(next_counts.values())
            self.probabilities[context] = {
                next_token: count / total
                for next_token, count in next_counts.items()
            }

        start_total = sum(self.start_counts.values())
        self.start_probabilities = {
            token: count / start_total
            for token, count in self.start_counts.items()
        } if start_total else {}

    def distribution(self, previous_two_tokens):
        """Return P(next_token | context), or an empty dict if unseen."""
        return self.probabilities.get(tuple(previous_two_tokens), {})

    def display_distribution(self, previous_two_tokens):
        """Print next-token probabilities for a two-token context."""
        context = tuple(previous_two_tokens)
        distribution = self.distribution(context)
        if not distribution:
            print(f"No observed transitions from {context!r}.")
            return

        print(f"P(next token | {context!r}):")
        for next_token, probability in sorted(distribution.items()):
            print(f"  {next_token}: {probability:.3f}")

    def most_probable_next(self, previous_two_tokens):
        """Return the most probable next token, or None for an unseen context."""
        distribution = self.distribution(previous_two_tokens)
        if not distribution:
            return None
        return max(distribution, key=distribution.get)

    def normalization_totals(self):
        """Return probability sums for every observed two-token context."""
        return {
            context: sum(distribution.values())
            for context, distribution in self.probabilities.items()
        }

    def generate(self, max_tokens=50, rng=None):
        """Sample from <START>, using START counts for the first token."""
        rng = rng or random
        tokens = ["<START>"]
        if not self.start_probabilities:
            return tokens

        first_tokens = list(self.start_probabilities)
        tokens.append(rng.choices(
            first_tokens,
            weights=[self.start_probabilities[token] for token in first_tokens],
            k=1,
        )[0])

        while tokens[-1] != "<END>" and len(tokens) < max_tokens:
            distribution = self.distribution(tokens[-2:])
            if not distribution:
                break
            choices = list(distribution)
            tokens.append(rng.choices(
                choices,
                weights=[distribution[token] for token in choices],
                k=1,
            )[0])

        return tokens


if __name__ == "__main__":
    model = SecondOrderModel(SENTENCES)
    for context in (("<START>", "the"), ("the", "cat"), ("the", "dog"), ("cat", "sat"), ("dog", "ran")):
        model.display_distribution(context)
        prediction = model.most_probable_next(context)
        if prediction is not None:
            print(f"  Most probable next token: {prediction}")

    print("\nProbability normalization totals:")
    for context, total in sorted(model.normalization_totals().items()):
        print(f"  {context}: {total:.12f}")

    print("\nSample generated sentences:")
    rng = random.Random(42)
    for _ in range(5):
        print(" ".join(model.generate(rng=rng)))
