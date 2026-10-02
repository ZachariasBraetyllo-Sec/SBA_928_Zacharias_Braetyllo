import json
import random
from collections import defaultdict
from pathlib import Path

INPUT_PATH = Path("data/processed/fine_tuning_examples.jsonl")

TRAIN_PATH = Path("data/splits/train.jsonl")
VALIDATION_PATH = Path("data/splits/validation.jsonl")
EVALUATION_PATH = Path("data/splits/evaluation.jsonl")

RANDOM_SEED = 42


def load_examples():
    with INPUT_PATH.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def get_satisfaction(example):
    first_line = example["target"].splitlines()[0]

    return (
        first_line
        .split(":", 1)[1]
        .strip()
        .lower()
    )


def save_jsonl(path, examples):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:
        for example in examples:
            json.dump(
                example,
                f,
                ensure_ascii=False,
            )
            f.write("\n")


def print_distribution(name, examples):
    counts = {
        "positive": 0,
        "mixed": 0,
        "negative": 0,
    }

    for example in examples:
        label = get_satisfaction(example)
        counts[label] += 1

    print(f"{name}:")
    print(f"  Total: {len(examples)}")
    print(f"  positive: {counts['positive']}")
    print(f"  mixed: {counts['mixed']}")
    print(f"  negative: {counts['negative']}")


def main():
    examples = load_examples()

    if len(examples) != 30:
        raise ValueError(
            f"Expected 30 examples, but found {len(examples)}."
        )

    grouped = defaultdict(list)

    for example in examples:
        label = get_satisfaction(example)
        grouped[label].append(example)

    for label in [
        "positive",
        "mixed",
        "negative",
    ]:
        if len(grouped[label]) != 10:
            raise ValueError(
                f"Expected 10 {label} examples, "
                f"but found {len(grouped[label])}."
            )

    random.seed(RANDOM_SEED)

    train_examples = []
    validation_examples = []
    evaluation_examples = []

    for label in [
        "positive",
        "mixed",
        "negative",
    ]:
        random.shuffle(grouped[label])

        train_examples.extend(
            grouped[label][:8]
        )

        validation_examples.append(
            grouped[label][8]
        )

        evaluation_examples.append(
            grouped[label][9]
        )

    random.shuffle(train_examples)
    random.shuffle(validation_examples)
    random.shuffle(evaluation_examples)

    save_jsonl(
        TRAIN_PATH,
        train_examples,
    )

    save_jsonl(
        VALIDATION_PATH,
        validation_examples,
    )

    save_jsonl(
        EVALUATION_PATH,
        evaluation_examples,
    )

    print("\nDataset split complete.\n")

    print_distribution(
        "Training set",
        train_examples,
    )

    print()

    print_distribution(
        "Validation set",
        validation_examples,
    )

    print()

    print_distribution(
        "Held-out evaluation set",
        evaluation_examples,
    )

    print("\nSaved files:")
    print(TRAIN_PATH)
    print(VALIDATION_PATH)
    print(EVALUATION_PATH)


if __name__ == "__main__":
    main()