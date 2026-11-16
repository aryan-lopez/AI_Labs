"""First-order Markov language model for the BN lab's tokenized sentences."""

from collections import Counter, defaultdict
import random

from dataset import SENTENCES


class FirstOrderModel:
    """Estimate P(next_token | current_token) from adjacent token counts."""

    def __init__(self, sentences):
        self.transition_counts = defaultdict(Counter)

        for sentence in sentences:
            for current_token, next_token in zip(sentence, sentence[1:]):
                self.transition_counts[current_token][next_token] += 1

        self.probabilities = {}
        for current_token, next_counts in self.transition_counts.items():
            total = sum(next_counts.values())
            self.probabilities[current_token] = {
                next_token: count / total
                for next_token, count in next_counts.items()
            }

    def distribution(self, current_token):
        """Return P(next_token | current_token), or an empty dict if unseen."""
        return self.probabilities.get(current_token, {})

    def display_distribution(self, current_token):
        """Print the next-token probabilities for one current token."""
        distribution = self.distribution(current_token)
        if not distribution:
            print(f"No observed transitions from {current_token!r}.")
            return

        print(f"P(next token | {current_token!r}):")
        for next_token, probability in sorted(distribution.items()):
            print(f"  {next_token}: {probability:.3f}")

    def most_probable_next(self, current_token):
        """Return the most probable next token, or None for an unseen context."""
        distribution = self.distribution(current_token)
        if not distribution:
            return None
        return max(distribution, key=distribution.get)

    def normalization_totals(self):
        """Return the probability sum for every context in the model."""
        return {
            current_token: sum(distribution.values())
            for current_token, distribution in self.probabilities.items()
        }

    def generate(self, max_tokens=50, rng=None):
        """Sample tokens from <START> until <END> or the safety limit."""
        rng = rng or random
        tokens = ["<START>"]

        while tokens[-1] != "<END>" and len(tokens) < max_tokens:
            distribution = self.distribution(tokens[-1])
            if not distribution:
                break

            choices = list(distribution)
            weights = [distribution[token] for token in choices]
            tokens.append(rng.choices(choices, weights=weights, k=1)[0])

        return tokens

    def generate_greedy(self, max_tokens=50):
        """Always choose the most probable next token until <END>."""
        tokens = ["<START>"]

        while tokens[-1] != "<END>" and len(tokens) < max_tokens:
            next_token = self.most_probable_next(tokens[-1])
            if next_token is None:
                break
            tokens.append(next_token)

        return tokens


if __name__ == "__main__":
    model = FirstOrderModel(SENTENCES)

    for context in ("the", "cat", "dog", "sat", "ran"):
        model.display_distribution(context)
        prediction = model.most_probable_next(context)
        if prediction is not None:
            print(f"  Most probable next token: {prediction}")

    print("\nProbability normalization totals:")
    for context, total in sorted(model.normalization_totals().items()):
        print(f"  {context}: {total:.12f}")

    print("\nSample generated sentences:")
    for _ in range(5):
        print(" ".join(model.generate()))
