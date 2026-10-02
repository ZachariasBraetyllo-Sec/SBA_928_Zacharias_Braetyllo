# SBA 928 - Enhancing Market Research with AI Prompt Engineering

## Overview

This project explores two separate AI workflows for market research:

- prompt engineering
- supervised fine-tuning

The prompt-engineering phase tests how changes to instructions, roles, constraints, context, and output format affect model responses during inference.

The fine-tuning phase trains a pretrained language model on structured examples so that its behavior changes through actual parameter updates.

The project uses customer-review data from the Women's Clothing E-Commerce Reviews dataset.

## Project Goals

The project was designed to:

- create market-research prompt variations
- compare prompt-engineering strategies
- prepare structured instruction-context-target training data
- fine-tune a pretrained language model
- compare base-model and fine-tuned outputs
- evaluate bias and fairness concerns
- document limitations and findings

## Dataset

Source dataset:

```text
Women's Clothing E-Commerce Reviews
```

The original dataset contained:

```text
23,486 reviews
```

After removing rows with missing review text, the cleaned dataset contained:

```text
22,641 reviews
```

The cleaned data is stored at:

```text
data/processed/womens_clothing_reviews_clean.csv
```

## Models

### Prompt Engineering

Prompt-engineering experiments used:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

This model was used for inference during the prompt-engineering phase.

It was also used to create candidate extractive fields for the supervised fine-tuning dataset. Candidate fields were validated against the source review before being accepted.

### Fine-Tuning

The pretrained base model used for supervised fine-tuning was:

```text
google/flan-t5-small
```

The completed fine-tuned model was saved locally to:

```text
models/flan_t5_market_research
```

Large generated model-weight and optimizer files are intentionally excluded from Git because they exceed standard GitHub file-size limits.

The repository includes the training code, configuration files, tokenizer metadata, evaluation outputs, and training summary needed to document and reproduce the experiment.

## Fine-Tuning Dataset

The final supervised dataset contained 30 validated examples:

```text
10 positive
10 mixed
10 negative
```

The dataset was divided into:

```text
Training:   24 examples
Validation:  3 examples
Evaluation:  3 examples
```

The training set contained:

```text
8 positive
8 mixed
8 negative
```

The validation set contained:

```text
1 positive
1 mixed
1 negative
```

The held-out evaluation set contained:

```text
1 positive
1 mixed
1 negative
```

Files:

```text
data/splits/train.jsonl
data/splits/validation.jsonl
data/splits/evaluation.jsonl
```

## Training Data Validation

Candidate training targets were required to use phrases grounded directly in the source review.

During balanced dataset generation:

```text
Processed candidate reviews: 121
Accepted examples: 30
Rejected examples: 91
```

The validation process reduced unsupported generated content but did not guarantee that every grounded phrase was assigned to the correct semantic field.

This limitation is discussed in:

```text
docs/evaluation.md
docs/bias_fairness.md
```

## Training Configuration

The FLAN-T5-small fine-tuning experiment used:

```text
Epochs: 5
Training batch size: 2
Validation batch size: 2
Learning rate: 5e-5
Weight decay: 0.01
Random seed: 42
```

Final reported training loss:

```text
1.5134
```

Validation loss decreased across the five epochs:

```text
Epoch 1: 1.6330
Epoch 2: 1.0080
Epoch 3: 0.8447
Epoch 4: 0.7750
Epoch 5: 0.7595
```

Training completed in approximately:

```text
26.27 seconds
```

A concise training record is stored at:

```text
outputs/fine_tuned_model/training_summary.txt
```

## Evaluation Summary

The pretrained base model often returned very short or generic answers that did not follow the requested market-research structure.

The fine-tuned model showed clear improvement in:

```text
Format adherence
Completeness
Task-specific response structure
```

Semantic accuracy remained inconsistent.

The fine-tuned model sometimes assigned neutral or negative review phrases to the wrong field.

The experiment therefore showed stronger improvement in response structure than in reliable sentiment interpretation.

Base-model evaluation outputs are stored at:

```text
outputs/base_model/evaluation_results.jsonl
```

Fine-tuned evaluation outputs are stored at:

```text
outputs/fine_tuned_model/evaluation_results.jsonl
```

Detailed analysis is available in:

```text
docs/evaluation.md
```

## Bias and Fairness

The original source dataset was strongly skewed toward positive ratings.

The fine-tuning dataset was intentionally balanced across positive, mixed, and negative satisfaction classes to reduce majority-class bias during this small experiment.

The project also identified a limitation in automated target validation: a phrase may be directly grounded in a review while still being assigned to the wrong semantic category.

Detailed discussion is available in:

```text
docs/bias_fairness.md
```

## Repository Structure

```text
SBA_928_Zacharias_Braetyllo/
├── data/
│   ├── source/
│   │   └── womens_clothing_reviews.csv
│   ├── processed/
│   │   ├── womens_clothing_reviews_clean.csv
│   │   └── fine_tuning_examples.jsonl
│   └── splits/
│       ├── train.jsonl
│       ├── validation.jsonl
│       └── evaluation.jsonl
│
├── docs/
│   ├── prompt_engineering.md
│   ├── fine_tuning.md
│   ├── evaluation.md
│   ├── bias_fairness.md
│   └── conclusion.md
│
├── models/
│   └── flan_t5_market_research/
│       └── model configuration and tokenizer metadata
│
├── outputs/
│   ├── base_model/
│   │   └── evaluation_results.jsonl
│   ├── fine_tuned_model/
│   │   ├── evaluation_results.jsonl
│   │   └── training_summary.txt
│   └── prompt_engineering/
│
├── src/
│   └── sba_928_zacharias_braetyllo/
│       ├── prepare_data.py
│       ├── run_base_model.py
│       ├── generate_training_examples.py
│       ├── split_fine_tuning_data.py
│       ├── train_flan_t5.py
│       └── evaluate_models.py
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Large Model Files

The local fine-tuning process generated model and optimizer files larger than GitHub's normal file-size limit.

The following generated artifacts are therefore excluded from Git:

```text
*.safetensors
optimizer.pt
scheduler.pt
rng_state.pth
checkpoint directories
```

The fine-tuned model can be recreated by running the training script using the included dataset splits and project dependencies.

## Setup

This project uses `uv` for Python environment and dependency management.

Install dependencies with:

```bash
uv sync
```

## Main Commands

### Prepare the cleaned dataset

```bash
uv run python src/sba_928_zacharias_braetyllo/prepare_data.py
```

### Run prompt-engineering experiments

```bash
uv run python src/sba_928_zacharias_braetyllo/run_base_model.py
```

### Generate fine-tuning examples

```bash
uv run python src/sba_928_zacharias_braetyllo/generate_training_examples.py
```

### Create train, validation, and evaluation splits

```bash
uv run python src/sba_928_zacharias_braetyllo/split_fine_tuning_data.py
```

### Fine-tune FLAN-T5-small

```bash
uv run python src/sba_928_zacharias_braetyllo/train_flan_t5.py
```

### Compare base and fine-tuned models

```bash
uv run python src/sba_928_zacharias_braetyllo/evaluate_models.py
```

## Documentation

Detailed project documentation is available in:

```text
docs/prompt_engineering.md
docs/fine_tuning.md
docs/evaluation.md
docs/bias_fairness.md
docs/conclusion.md
```

## Final Takeaway

Prompt engineering improved responses by changing how the model was instructed.

Fine-tuning changed the model's task-specific behavior through supervised training.

The fine-tuned model became much more consistent at producing the requested market-research response structure, but semantic accuracy remained limited by the small training dataset and imperfections in automated target labeling.

This project demonstrates a complete workflow from source-data preparation through prompt engineering, supervised fine-tuning, held-out evaluation, and bias analysis.