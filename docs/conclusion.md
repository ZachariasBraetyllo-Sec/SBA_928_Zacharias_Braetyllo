# Conclusion

## Project Summary

This project explored how prompt engineering and supervised fine-tuning can be used to improve AI-assisted market research.

The source data came from the Women's Clothing E-Commerce Reviews dataset. After cleaning, the dataset contained 22,641 usable customer reviews.

The project was completed in two distinct phases:

- prompt engineering
- model fine-tuning

The prompt-engineering phase tested how different instructions, roles, constraints, and output formats affected model responses without changing model parameters.

The fine-tuning phase used a separate structured dataset containing instruction, review context, and validated target responses to perform actual task-specific training.

## Prompt Engineering Findings

The prompt-engineering experiments showed that broad prompts often produced responses that were relevant but incomplete or inaccurate.

More explicit prompts improved focus.

Adding market-research roles helped orient the model toward the intended analytical task.

Grounding instructions reduced unsupported interpretation.

The strongest results came from combining a clear task with source restrictions and a structured output format.

The prompt-engineering phase demonstrated that changing the prompt can substantially change model behavior even when the underlying model remains unchanged.

## Fine-Tuning Findings

The fine-tuning experiment used `google/flan-t5-small`.

A balanced 30-example supervised dataset was created with:

```text
10 positive
10 mixed
10 negative
```

The data was divided into:

```text
24 training examples
3 validation examples
3 held-out evaluation examples
```

The model was fine-tuned for five epochs.

Validation loss decreased from approximately:

```text
1.6330
```

after the first epoch to approximately:

```text
0.7595
```

after the fifth epoch.

The completed fine-tuned model was saved to:

```text
models/flan_t5_market_research
```

## Base Model vs Fine-Tuned Model

The pretrained base model frequently produced short or generic responses that did not follow the required market-research structure.

The fine-tuned model showed a clear improvement in format adherence and completeness.

After fine-tuning, the model consistently attempted to produce:

```text
Satisfaction: ...
Main positive: ...
Main concern: ...
```

The fine-tuned model also showed stronger task awareness on some held-out examples.

However, improvement was not consistent across all aspects of the task.

The model sometimes classified satisfaction incorrectly or assigned neutral and negative phrases to the wrong field.

This means the fine-tuning experiment improved task structure more reliably than semantic accuracy.

## Data Quality Findings

One of the most important findings from the experiment was the effect of training-target quality.

The target-generation process required extracted phrases to be grounded directly in the source review.

This prevented unsupported or invented content from being accepted.

However, exact grounding did not guarantee that a phrase was correctly labeled as positive or negative.

A phrase could appear directly in the review while still being assigned to the wrong semantic field.

This limitation was visible in both the target data and the fine-tuned model outputs.

The experiment therefore demonstrated that supervised fine-tuning depends heavily on the quality of the target labels, not only on whether the text is grounded in the source.

## Bias and Fairness Findings

The original review dataset was strongly imbalanced toward positive ratings.

Product categories were also unevenly represented.

To reduce the impact of satisfaction-class imbalance, the fine-tuning dataset was intentionally balanced across positive, mixed, and negative examples.

This helped prevent the small training experiment from being dominated by positive reviews.

The project also identified a second source of bias in the labeling process.

Automated grounding checks were effective at verifying source support but were not sufficient for validating sentiment or semantic role.

For a larger implementation, manual review or stronger semantic validation would improve both fairness and training quality.

## Limitations

This experiment was intentionally small.

The training dataset contained only 24 training examples, and the held-out evaluation set contained only three examples.

The results therefore should not be treated as evidence of broad production-level performance.

The goal was to demonstrate a complete prompt-engineering and fine-tuning workflow rather than build a production market-research system.

A larger project would benefit from:

- more manually validated training examples
- a larger held-out evaluation set
- broader product-category representation
- stronger semantic validation of target labels

## Final Takeaway

The project demonstrated that prompt engineering and fine-tuning solve related but different problems.

Prompt engineering improved responses by changing how the model was instructed.

Fine-tuning changed the model's task-specific behavior through supervised training.

The fine-tuned model did not become uniformly more accurate, but it showed clear improvements in response structure, completeness, and adherence to the requested market-research format.

The experiment also showed that better model behavior depends on more than training alone.

Source-data balance and target-label quality both have a direct effect on the usefulness of the final model.

Overall, the project successfully demonstrated the full workflow of prompt development, supervised fine-tuning, held-out evaluation, and bias analysis for an AI-assisted market-research task.