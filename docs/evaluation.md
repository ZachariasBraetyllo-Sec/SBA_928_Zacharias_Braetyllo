# Model Evaluation

## Overview

The evaluation phase compared the pretrained base model, `google/flan-t5-small`, against the fine-tuned checkpoint saved at:

```text
models/flan_t5_market_research
```

The comparison used three held-out examples that were not included in the training or validation datasets.

The evaluation focused on:

- relevance to the review
- factual grounding
- completeness
- specificity
- consistency
- format adherence
- potential bias

The goal was not to prove that the fine-tuned model was universally better. The goal was to determine what changed after task-specific fine-tuning and whether those changes improved the market-research response behavior.

## Evaluation Dataset

The held-out evaluation set contained three examples:

```text
1 positive
1 mixed
1 negative
```

This balanced the evaluation across the three satisfaction classes used during fine-tuning.

The evaluation data was stored at:

```text
data/splits/evaluation.jsonl
```

The same examples were passed to both the pretrained base model and the fine-tuned model.

## Evaluation Example 1

### Review

```text
I'm surprised other reviewers loved this one so much. it's completely different then how it looks on the model. it's much shorter, which others do mention, but it flares a lot. enough to feel maternity-ish on me. it looks fitted on the model. maybe it's my shape, i have a short torso and carry weight in myhips. i ordered an xs too. i will say the material
is very nice and it's well made, but it's going back.
```

### Expected Target

```text
Satisfaction: mixed
Main positive: The material is very nice
Main concern: It's going back
```

### Pretrained Base Model Output

```text
satisfied
```

### Fine-Tuned Model Output

```text
Satisfaction: positive Main positive: it looks fitted on the model Main concern: it looks fitted on the model
```

### Analysis

The pretrained base model produced a very short answer and did not follow the required output structure.

The fine-tuned model showed clear improvement in format adherence because it attempted all three required fields.

However, the fine-tuned response was not semantically accurate. It classified the review as positive even though the expected label was mixed. It also used the same phrase as both the positive feature and the concern.

This example shows that fine-tuning improved task structure without reliably improving interpretation.

## Evaluation Example 2

### Review

```text
Love this dress!  it's sooo pretty.  i happened to find it in a store, and i'm glad i did bc i never would have ordered it online bc it's petite.  i bought a petite and am 5'8".  i love the length on me- hits just a little below the knee.  would definitely be a true midi on someone who is truly petite.
```

### Expected Target

```text
Satisfaction: positive
Main positive: Love this dress
Main concern: None stated
```

### Pretrained Base Model Output

```text
flattering
```

### Fine-Tuned Model Output

```text
Satisfaction: positive Main positive: it's petite Main concern: it hits just a little below the knee Main concern: it's petite
```

### Analysis

The pretrained base model again produced a short generic answer rather than the requested structured summary.

The fine-tuned model correctly identified the satisfaction as positive and attempted to follow the task-specific format.

However, it incorrectly treated positive or neutral details as concerns and repeated the `Main concern` field.

This example represents partial improvement. The fine-tuned model was more complete and more aligned with the requested structure, but the semantic interpretation of the concern field was still weak.

## Evaluation Example 3

### Review

```text
These run very small!! they are also short, almost like a crop pant. the fit was so weird that i won't even exchange for a bigger size.
```

### Expected Target

```text
Satisfaction: negative
Main positive: These run very small
Main concern: The fit was so weird that I won't even exchange for a bigger size
```

### Pretrained Base Model Output

```text
They are not as big as the size of the pant.
```

### Fine-Tuned Model Output

```text
Satisfaction: negative Main positive: They are also short Main concern: The fit was so weird that I won't even exchange for a bigger size
```

### Analysis

The pretrained base model produced a vague response that did not follow the target structure.

The fine-tuned model correctly identified the review as negative and reproduced the main concern closely.

It also followed the expected three-field structure more closely than the pretrained model.

The main remaining problem was the `Main positive` field. The phrase `They are also short` is not actually a positive feature in the context of this review.

This was the strongest held-out result for the fine-tuned model because the satisfaction label and concern were both aligned with the expected target.

## Side-by-Side Comparison

| Evaluation Area | Pretrained Base Model | Fine-Tuned Model |
|---|---|---|
| Format adherence | Poor | Clearly improved |
| Satisfaction classification | Inconsistent or absent | Improved, but not fully reliable |
| Completeness | Very limited | Much more complete |
| Specificity | Low | Improved |
| Factual grounding | Mixed | Mixed |
| Positive/concern separation | Not demonstrated | Still inconsistent |
| Consistency | Low | Improved structurally |
| Overall task alignment | Weak | Partial improvement |

## Main Findings

The strongest improvement from fine-tuning was format adherence.

The pretrained FLAN-T5-small model frequently responded with a single word or short sentence. These outputs did not match the required market-research structure.

After fine-tuning, the model consistently attempted to produce satisfaction, positive-feature, and concern fields.

The fine-tuned model also showed better task awareness. It successfully classified the negative example and correctly reproduced the main concern in that case.

However, semantic accuracy remained inconsistent.

The model sometimes treated neutral or negative statements as positive features. It also created concerns from details that were not actually complaints.

These errors show that the model learned the structure of the task more successfully than it learned the semantic distinction between positive and negative evidence.

## Impact of Training Data Quality

The evaluation also revealed a limitation in the fine-tuning targets.

The target-generation pipeline verified that extracted phrases appeared directly in the source review. This prevented unsupported or invented text from entering the dataset.

However, exact phrase grounding did not guarantee that the phrase was correctly assigned as a positive feature or concern.

For example, the expected target for Evaluation Example 3 contains:

```text
Main positive: These run very small
```

The phrase appears directly in the review, so it passed the grounding check. However, within the review it is clearly a negative complaint.

This means the training data contained some semantically incorrect field assignments even though the phrases themselves were source-grounded.

That limitation likely contributed to the fine-tuned model learning stronger output structure than sentiment-role accuracy.

## Evaluation Limitations

This evaluation used only three held-out examples.

The results therefore cannot be treated as a broad measurement of model performance across the entire source dataset.

The fine-tuning dataset was also intentionally small because the purpose of the experiment was to demonstrate the fine-tuning workflow rather than train a production-quality market-research model.

A larger experiment would benefit from more manually validated targets and a larger held-out evaluation set.

## Evaluation Conclusion

The fine-tuning experiment produced mixed but meaningful results.

The fine-tuned model improved substantially in format adherence, completeness, and task-specific response structure compared with the pretrained base model.

Semantic accuracy improved in some areas, particularly in identifying the negative held-out example and reproducing its main concern.

At the same time, the model remained inconsistent when separating positive features from complaints.

The results show that task-specific fine-tuning changed the model's behavior in a measurable way, but also demonstrate that model quality depends heavily on the quality of the supervised target data.

For this experiment, fine-tuning was most effective at teaching the response format and overall task structure rather than producing consistently accurate sentiment interpretation.