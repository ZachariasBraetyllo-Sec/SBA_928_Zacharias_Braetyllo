import json
from pathlib import Path

from torch.utils.data import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "google/flan-t5-small"

TRAIN_PATH = Path("data/splits/train.jsonl")
VALIDATION_PATH = Path("data/splits/validation.jsonl")

MODEL_OUTPUT_DIR = Path("models/flan_t5_market_research")

MAX_INPUT_LENGTH = 512
MAX_TARGET_LENGTH = 128


class ReviewDataset(Dataset):
    def __init__(self, path, tokenizer):
        self.tokenizer = tokenizer
        self.examples = self.load_examples(path)

    def load_examples(self, path):
        with path.open(encoding="utf-8") as f:
            return [
                json.loads(line)
                for line in f
                if line.strip()
            ]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        example = self.examples[index]

        input_text = (
            f"{example['instruction']}\n\n"
            f"Customer review:\n"
            f"{example['context']}"
        )

        target_text = example["target"]

        model_inputs = self.tokenizer(
            input_text,
            max_length=MAX_INPUT_LENGTH,
            truncation=True,
        )

        labels = self.tokenizer(
            text_target=target_text,
            max_length=MAX_TARGET_LENGTH,
            truncation=True,
        )

        model_inputs["labels"] = labels["input_ids"]

        return model_inputs


def main():
    print(f"Loading tokenizer: {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    print(f"Loading pretrained base model: {MODEL_NAME}")

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    train_dataset = ReviewDataset(
        TRAIN_PATH,
        tokenizer,
    )

    validation_dataset = ReviewDataset(
        VALIDATION_PATH,
        tokenizer,
    )

    print()
    print(f"Training examples: {len(train_dataset)}")
    print(f"Validation examples: {len(validation_dataset)}")
    print()

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
    )

    MODEL_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    training_args = TrainingArguments(
        output_dir=str(MODEL_OUTPUT_DIR),
        num_train_epochs=5,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        learning_rate=5e-5,
        weight_decay=0.01,
        logging_steps=1,
        logging_strategy="steps",
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        seed=42,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        data_collator=data_collator,
        processing_class=tokenizer,
    )

    print("Starting fine-tuning...")
    print()

    train_result = trainer.train()

    print()
    print("Fine-tuning complete.")
    print()

    print("Training metrics:")
    for key, value in train_result.metrics.items():
        print(f"  {key}: {value}")

    print()
    print("Running final validation evaluation...")

    validation_metrics = trainer.evaluate()

    print()
    print("Validation metrics:")
    for key, value in validation_metrics.items():
        print(f"  {key}: {value}")

    print()
    print(f"Saving fine-tuned model to: {MODEL_OUTPUT_DIR}")

    trainer.save_model(
        str(MODEL_OUTPUT_DIR)
    )

    tokenizer.save_pretrained(
        str(MODEL_OUTPUT_DIR)
    )

    print()
    print("Saved fine-tuned model and tokenizer.")
    print("Training finished successfully.")


if __name__ == "__main__":
    main()