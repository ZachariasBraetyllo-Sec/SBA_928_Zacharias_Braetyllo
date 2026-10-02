# Fine-Tuning Experiment

## Overview

The fine-tuning phase used `google/flan-t5-small` as the pretrained base model.

This phase was separate from the prompt-engineering experiments. Prompt engineering changed the instructions given to the model during inference, while fine-tuning updated the model through supervised training on structured examples.

The goal of the fine-tuning experiment was to teach the model to produce a consistent market-research summary from a customer review using the following format:

```text
Satisfaction: ...
Main positive: ...
Main concern: ...
```

Each training example contained:

- an instruction
- the customer review as source context
- a validated target response

## Fine-Tuning Task

The instruction used across the fine-tuning dataset was:

```text
Analyze the customer review and summarize the customer's satisfaction, main positive product attribute, and main concern.
```

The target format was standardized as:

```text
Satisfaction: [positive, mixed, or negative]
Main positive: [source-grounded positive feature or none stated]
Main concern: [source-grounded concern or none stated]
```

The purpose of using a fixed structure was to give the model a clear task-specific response pattern to learn.

## Training Data Preparation

The fine-tuning dataset was created from the cleaned Women's Clothing E-Commerce Reviews dataset.

The source dataset contained many more positive reviews than mixed or negative reviews. Because this small classroom experiment would otherwise be dominated by the majority class, the final fine-tuning sample was intentionally balanced.

The final dataset contained 30 examples:

- 10 positive
- 10 mixed
- 10 negative

Satisfaction labels were derived from the source review rating using the following rule:

```text
Ratings 4-5 -> positive
Rating 3    -> mixed
Ratings 1-2 -> negative
```

The `Main positive` and `Main concern` fields were generated as short extractive phrases from the source review.

To reduce unsupported target content, candidate phrases were validated against the source review text. A generated phrase was accepted only if it appeared directly in the review or used the permitted value `none stated`.

During dataset generation:

```text
Processed candidate reviews: 121
Accepted examples: 30
Rejected examples: 91
```

The high rejection count reflects the grounding requirement used during dataset construction. Candidates were rejected when generated fields were malformed or when the extracted phrase could not be verified against the source review.

The final structured dataset was saved to:

```text
data/processed/fine_tuning_examples.jsonl
```

## Dataset Splits

The 30 accepted examples were divided into separate training, validation, and held-out evaluation datasets.

The training set contained 24 examples:

```text
8 positive
8 mixed
8 negative
```

The validation set contained 3 examples:

```text
1 positive
1 mixed
1 negative
```

The held-out evaluation set contained 3 examples:

```text
1 positive
1 mixed
1 negative
```

The files were saved as:

```text
data/splits/train.jsonl
data/splits/validation.jsonl
data/splits/evaluation.jsonl
```

The held-out evaluation examples were not used during model training.

## Model

The pretrained base model used for fine-tuning was:

```text
google/flan-t5-small
```

FLAN-T5-small was selected because it is designed for instruction-response tasks and is lightweight enough for local experimentation.

The tokenizer and sequence-to-sequence model were loaded using Hugging Face Transformers.

## Training Configuration

The fine-tuning run used the following configuration:

```text
Model: google/flan-t5-small
Training examples: 24
Validation examples: 3
Epochs: 5
Training batch size: 2
Validation batch size: 2
Learning rate: 5e-5
Weight decay: 0.01
Maximum input length: 512 tokens
Maximum target length: 128 tokens
Random seed: 42
```

Training used the Hugging Face `Trainer` API with evaluation and checkpoint saving performed after each epoch.

The best model was selected using validation loss.

## Training Results

The model completed all five training epochs successfully.

The reported final training metrics included:

```text
Training runtime: 26.27 seconds
Training loss: 1.5134
Epochs completed: 5
```

Validation loss decreased across the training run:

```text
Epoch 1: 1.6330
Epoch 2: 1.0080
Epoch 3: 0.8447
Epoch 4: 0.7750
Epoch 5: 0.7595
```

The decreasing validation loss indicates that the model became better at reproducing the expected task-specific target patterns on the validation examples during training.

Because the validation set contained only three examples, these values should not be interpreted as a broad measure of general model quality. They are evidence of behavior within this small fine-tuning experiment.

## Saved Model

The fine-tuned model and tokenizer were saved to:

```text
models/flan_t5_market_research
```

This checkpoint was then used for held-out evaluation against the original pretrained FLAN-T5-small model.

## Limitations of the Fine-Tuning Data

Although the target-generation process enforced exact source grounding, this validation method had an important limitation.

A phrase could be verified as appearing in the review without being semantically correct for the assigned field.

For example, a phrase may appear directly in the source review but still represent a negative feature rather than a positive feature.

This means the validation process was effective at detecting unsupported or invented text, but it could not fully validate whether each phrase had the correct sentiment or semantic role.

This limitation became visible during held-out evaluation and is discussed further in the evaluation and bias/fairness sections.

## Fine-Tuning Summary

The fine-tuning phase successfully produced a task-specific FLAN-T5-small checkpoint using a balanced supervised dataset.

The experiment included structured instruction-context-target examples, separate training and validation data, a held-out evaluation set, actual parameter training, validation monitoring, and a saved model checkpoint.

The next phase compares the pretrained base model with the fine-tuned model on the held-out evaluation examples to determine what behavior changed as a result of training.