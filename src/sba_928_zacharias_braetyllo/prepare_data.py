import csv
from pathlib import Path

SOURCE_PATH = Path("data/source/womens_clothing_reviews.csv")
OUTPUT_PATH = Path("data/processed/womens_clothing_reviews_clean.csv")

KEEP_COLUMNS = [
    "Clothing ID",
    "Age",
    "Review Text",
    "Rating",
    "Recommended IND",
    "Positive Feedback Count",
    "Department Name",
    "Class Name",
]


def main():
    kept_rows = 0
    skipped_rows = 0

    with SOURCE_PATH.open(newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)

        with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=KEEP_COLUMNS)
            writer.writeheader()

            for row in reader:
                review_text = row["Review Text"].strip()

                if not review_text:
                    skipped_rows += 1
                    continue

                cleaned_row = {
                    column: row[column].strip()
                    for column in KEEP_COLUMNS
                }

                writer.writerow(cleaned_row)
                kept_rows += 1

    print(f"Kept rows: {kept_rows}")
    print(f"Skipped rows with missing review text: {skipped_rows}")
    print(f"Saved cleaned dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
