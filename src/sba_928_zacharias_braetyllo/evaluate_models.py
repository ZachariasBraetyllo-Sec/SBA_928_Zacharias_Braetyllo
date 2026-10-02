import json
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE_MODEL_NAME = "google/flan-t5-small"
FINE_TUNED_MODEL_PATH = "models/flan_t5_market_research"

EVALUATION_PATH = Path("data/splits/evaluation.jsonl")

BASE_OUTPUT_PATH = Path("outputs/base_model/evaluation_results.jsonl")
FINE_TUNED_OUTPUT_PATH = Path(
    "outputs/fine_tuned_model/evaluation_results.jsonl"
)

MAX_INPUT_LENGTH = 512
MAX_NEW_TOKENS = 128


def load_examples():
    with EVALUATION_PATH.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def build_input(example):
    return (
        f"{example['instruction']}\n\n"
        f"Customer review:\n"
        f"{example['context']}"
    )


def generate_response(tokenizer, model, input_text):
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
        )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    ).strip()


def save_results(path, results):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:
        for result in results:
            json.dump(
                result,
                f,
                ensure_ascii=False,
            )
            f.write("\n")


def main():
    examples = load_examples()

    print(f"Loaded held-out evaluation examples: {len(examples)}")
    print()

    print("Loading pretrained base model...")

    base_tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_NAME
    )

    base_model = AutoModelForSeq2SeqLM.from_pretrained(
        BASE_MODEL_NAME
    )

    base_model.eval()

    print("Loading fine-tuned model...")

    fine_tuned_tokenizer = AutoTokenizer.from_pretrained(
        FINE_TUNED_MODEL_PATH
    )

    fine_tuned_model = AutoModelForSeq2SeqLM.from_pretrained(
        FINE_TUNED_MODEL_PATH
    )

    fine_tuned_model.eval()

    base_results = []
    fine_tuned_results = []

    for index, example in enumerate(examples, start=1):
        input_text = build_input(example)

        base_output = generate_response(
            base_tokenizer,
            base_model,
            input_text,
        )

        fine_tuned_output = generate_response(
            fine_tuned_tokenizer,
            fine_tuned_model,
            input_text,
        )

        base_result = {
            "example": index,
            "instruction": example["instruction"],
            "context": example["context"],
            "expected_target": example["target"],
            "model_output": base_output,
        }

        fine_tuned_result = {
            "example": index,
            "instruction": example["instruction"],
            "context": example["context"],
            "expected_target": example["target"],
            "model_output": fine_tuned_output,
        }

        base_results.append(base_result)
        fine_tuned_results.append(fine_tuned_result)

        print("=" * 80)
        print(f"Evaluation Example {index}")
        print("=" * 80)

        print("\nContext:")
        print(example["context"])

        print("\nExpected Target:")
        print(example["target"])

        print("\nBase Model Output:")
        print(base_output)

        print("\nFine-Tuned Model Output:")
        print(fine_tuned_output)

        print()

    save_results(
        BASE_OUTPUT_PATH,
        base_results,
    )

    save_results(
        FINE_TUNED_OUTPUT_PATH,
        fine_tuned_results,
    )

    print("Evaluation complete.")
    print(f"Base outputs saved to: {BASE_OUTPUT_PATH}")
    print(
        "Fine-tuned outputs saved to: "
        f"{FINE_TUNED_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()