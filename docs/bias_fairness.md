# Bias and Fairness Analysis

## Overview

Bias and fairness were evaluated at three points in the project:

- the original source dataset
- the fine-tuning dataset
- the model outputs produced during evaluation

The goal was to identify where the data or modeling process could produce distorted market-research insights and to document practical mitigation strategies.

## Bias in the Source Dataset

The original Women's Clothing E-Commerce Reviews dataset was not evenly distributed across satisfaction levels.

The rating distribution was strongly positive:

```text
1 star: 842
2 stars: 1,565
3 stars: 2,871
4 stars: 5,077
5 stars: 13,131
```

This means the source dataset contains far more highly rated reviews than low-rated reviews.

If examples were sampled randomly without adjustment, a fine-tuning dataset would likely contain many more positive reviews than mixed or negative reviews.

That imbalance could encourage the model to overpredict positive satisfaction or become less reliable when analyzing complaints.

## Product Category Imbalance

The source dataset also contained uneven representation across product departments.

The department distribution included:

```text
Tops: 10,468
Dresses: 6,319
Bottoms: 3,799
Intimate: 1,735
Jackets: 1,032
Trend: 119
Missing department: 14
```

Some product categories therefore appear much more frequently than others.

A model trained directly on the full distribution could learn more about the language associated with heavily represented categories such as Tops and Dresses while having much less exposure to categories such as Trend.

This could make performance appear stronger on common categories even if the model performs poorly on less represented products.

## Mitigation Through Balanced Fine-Tuning Data

To reduce satisfaction-class imbalance during the fine-tuning experiment, the final 30-example dataset was intentionally balanced.

It contained:

```text
10 positive
10 mixed
10 negative
```

The training split preserved this balance:

```text
8 positive
8 mixed
8 negative
```

The validation and held-out evaluation sets each contained:

```text
1 positive
1 mixed
1 negative
```

This ensured that the small experiment did not train almost entirely on positive reviews.

The balanced sampling strategy does not remove bias from the original source dataset, but it reduces one obvious source of imbalance within the fine-tuning experiment.

## Bias Introduced During Target Generation

A second source of bias was introduced by the training-target generation process.

The target-generation model was asked to extract:

```text
Main positive: ...
Main concern: ...
```

Candidate phrases were accepted only if they could be verified as exact text from the review.

This grounding check reduced hallucinated content, but it did not fully verify the semantic role of each phrase.

For example:

```text
Main positive: These run very small
```

may be directly grounded in the review text while still representing a complaint rather than a positive feature.

This creates a labeling bias problem.

The target may be factually grounded but still incorrectly categorized.

Because supervised fine-tuning teaches the model from the provided targets, incorrect semantic labels can become part of the learned behavior.

## Evidence From Model Evaluation

This limitation appeared during held-out evaluation.

The fine-tuned model frequently followed the expected output structure, but it sometimes treated negative or neutral statements as positive features.

It also occasionally identified a positive or neutral detail as a concern.

These errors suggest that the fine-tuned model learned the response structure more consistently than it learned the semantic distinction between praise and complaints.

The problem therefore was not only model behavior. It was also connected to the quality of the supervised labels.

## Demographic Considerations

The source dataset includes customer age, but the fine-tuning task did not use age as an input feature.

This was intentional.

The task focused on the content of the review rather than making assumptions based on demographic characteristics.

Using demographic information unnecessarily could introduce additional bias if the model began associating certain ages with satisfaction levels, product preferences, or complaint patterns.

For this experiment, demographic attributes were therefore excluded from the fine-tuning context.

## Representation Limitations

The dataset represents reviews from a specific women's clothing e-commerce context.

As a result, findings from this experiment should not be generalized automatically to:

- all retail products
- all customer populations
- all geographic regions
- all market-research settings

Language patterns in clothing reviews may differ from reviews involving technology, food, financial products, services, or other industries.

A model trained on this dataset would require additional evaluation before being used for a different market-research domain.

## Fairness Strategies

Several strategies could improve fairness and reduce bias in a larger implementation.

### Balanced Sampling

Training and evaluation samples should be checked for class imbalance before fine-tuning.

Balancing positive, mixed, and negative examples can reduce the risk of majority-class behavior dominating the model.

### Category-Aware Sampling

Examples should also be sampled across product categories so that highly represented departments do not dominate the training data.

A larger experiment could define minimum representation targets for each department or class.

### Manual Target Validation

The strongest improvement would be human review of training targets.

Exact text matching can verify grounding, but human validation is better suited to determining whether a phrase actually represents a positive feature, a concern, or a neutral statement.

### Separate Grounding and Sentiment Checks

A larger automated pipeline could use separate validation stages.

One stage could verify that the phrase is grounded in the source review.

A second stage could verify whether the phrase matches the intended semantic role.

This would reduce the type of labeling error observed in the current experiment.

### Larger Held-Out Evaluation

A three-example held-out set is sufficient for demonstrating the classroom workflow, but it is not large enough to establish broad fairness or performance claims.

A production-oriented evaluation should include substantially more examples across satisfaction classes and product categories.

### Avoid Unsupported Generalization

Model outputs should remain tied to the specific review or sample being analyzed.

One customer review should not be treated as evidence that all customers share the same preference or complaint.

This is especially important in market research, where small or skewed samples can easily produce misleading conclusions.

## Fairness Summary

The primary bias identified in the source data was the strong imbalance toward positive reviews.

Product categories were also unevenly represented.

The fine-tuning experiment reduced satisfaction-class imbalance by creating a balanced 30-example dataset.

However, the project also revealed a different type of bias introduced during target generation: a phrase could be source-grounded while still being assigned to the wrong semantic category.

The most important mitigation for future work would therefore be stronger target validation, especially human review of whether extracted phrases correctly represent positive features or concerns.

Overall, the experiment shows that fairness in AI-assisted market research depends on both the distribution of the source data and the quality of the labels used during model training.