import csv
import json
import re

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

DATA_PATH = "data/processed/womens_clothing_reviews_clean.csv"
OUTPUT_PATH = "data/processed/fine_tuning_examples.jsonl"

TARGET_PER_CLASS = 10

INSTRUCTION = (
    "Analyze the customer review and summarize the customer's satisfaction, "
    "main positive product attribute, and main concern."
)


def rating_to_satisfaction(rating):
    rating = int(rating)

    if rating >= 4:
        return "positive"

    if rating == 3:
        return "mixed"

    return "negative"


def build_prompt(review_text):
    return f"""
You are extracting evidence from a customer review for a supervised
training dataset.

Return exactly two lines:

Main positive: [short exact phrase copied from the review]
Main concern: [short exact phrase copied from the review]

Rules:
- Copy words directly from the review.
- Do not paraphrase.
- Do not explain.
- Do not invent information.
- Do not change a positive statement into a concern.
- Do not change a negative statement into a positive.
- Keep each extracted phrase short.
- If there is no clear positive statement, write exactly:
  Main positive: none stated
- If there is no clear concern, write exactly:
  Main concern: none stated
- Return exactly two non-empty lines.
- Do not use markdown or bullet points.

Example:

Review:
Absolutely wonderful - silky and sexy and comfortable

Target:
Main positive: silky and sexy and comfortable
Main concern: none stated

Example:

Review:
The color is beautiful, but the sleeves are too long and the fit is too loose.

Target:
Main positive: the color is beautiful
Main concern: the sleeves are too long

Example:

Review:
This shirt is very flattering to all due to the adjustable front tie. it is sleeveless so it pairs well with any cardigan.

Target:
Main positive: adjustable front tie
Main concern: none stated

Now analyze this review:

Review:
{review_text}

Target:
""".strip()


def generate_analysis_fields(tokenizer, model, review_text):
    prompt = build_prompt(review_text)

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=False,
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()


def normalize_text(text):
    text = text.casefold()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def phrase_is_grounded(phrase, review_text):
    if phrase.casefold() == "none stated":
        return True

    normalized_phrase = normalize_text(phrase)
    normalized_review = normalize_text(review_text)

    return normalized_phrase in normalized_review


def validate_analysis_fields(generated_text, review_text):
    lines = [
        line.strip()
        for line in generated_text.splitlines()
        if line.strip()
    ]

    if len(lines) != 2:
        return False, "wrong number of lines"

    if not lines[0].startswith("Main positive:"):
        return False, "missing Main positive field"

    if not lines[1].startswith("Main concern:"):
        return False, "missing Main concern field"

    main_positive = lines[0].split(":", 1)[1].strip()
    main_concern = lines[1].split(":", 1)[1].strip()

    if not main_positive:
        return False, "empty Main positive"

    if not main_concern:
        return False, "empty Main concern"

    if not phrase_is_grounded(main_positive, review_text):
        return False, "ungrounded Main positive"

    if not phrase_is_grounded(main_concern, review_text):
        return False, "ungrounded Main concern"

    return True, "valid"


def build_target(satisfaction, generated_text):
    lines = [
        line.strip()
        for line in generated_text.splitlines()
        if line.strip()
    ]

    main_positive = lines[0].split(":", 1)[1].strip()
    main_concern = lines[1].split(":", 1)[1].strip()

    return (
        f"Satisfaction: {satisfaction}\n"
        f"Main positive: {main_positive}\n"
        f"Main concern: {main_concern}"
    )


def save_example(example):
    with open(
        OUTPUT_PATH,
        "a",
        encoding="utf-8",
    ) as f:
        json.dump(
            example,
            f,
            ensure_ascii=False,
        )
        f.write("\n")


def all_classes_complete(counts):
    return all(
        counts[label] >= TARGET_PER_CLASS
        for label in ["positive", "mixed", "negative"]
    )


def main():
    print(f"Loading target-generation model: {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
    )

    model.eval()

    accepted_counts = {
        "positive": 0,
        "mixed": 0,
        "negative": 0,
    }

    rejected_count = 0
    processed_count = 0

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ):
        pass

    print(
        f"Collecting {TARGET_PER_CLASS} examples "
        "for each satisfaction class..."
    )

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if all_classes_complete(accepted_counts):
                break

            review_text = row["Review Text"].strip()
            rating = row["Rating"].strip()

            satisfaction = rating_to_satisfaction(rating)

            if accepted_counts[satisfaction] >= TARGET_PER_CLASS:
                continue

            processed_count += 1

            generated_text = generate_analysis_fields(
                tokenizer,
                model,
                review_text,
            )

            is_valid, reason = validate_analysis_fields(
                generated_text,
                review_text,
            )

            if not is_valid:
                rejected_count += 1

                print(
                    f"Rejected #{processed_count}: {reason} "
                    f"| positive={accepted_counts['positive']} "
                    f"mixed={accepted_counts['mixed']} "
                    f"negative={accepted_counts['negative']}"
                )

                continue

            target = build_target(
                satisfaction,
                generated_text,
            )

            example = {
                "instruction": INSTRUCTION,
                "context": review_text,
                "target": target,
            }

            save_example(example)

            accepted_counts[satisfaction] += 1

            print(
                f"Accepted {satisfaction}: "
                f"{accepted_counts[satisfaction]}/{TARGET_PER_CLASS} "
                f"| positive={accepted_counts['positive']} "
                f"mixed={accepted_counts['mixed']} "
                f"negative={accepted_counts['negative']}"
            )

    if not all_classes_complete(accepted_counts):
        raise RuntimeError(
            "Could not collect enough validated examples "
            "for every satisfaction class."
        )

    total_accepted = sum(accepted_counts.values())

    print("\nGeneration complete.")
    print(f"Processed candidate reviews: {processed_count}")
    print(f"Accepted examples: {total_accepted}")
    print(f"  positive: {accepted_counts['positive']}")
    print(f"  mixed: {accepted_counts['mixed']}")
    print(f"  negative: {accepted_counts['negative']}")
    print(f"Rejected examples: {rejected_count}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()