# Prompt Engineering

## Dataset

This project uses the Women's E-Commerce Clothing Reviews dataset as the source market research data.

The cleaned dataset contains 22,641 reviews after removing records with missing review text.

## Prompt Engineering Model

The prompt-engineering experiment uses `Qwen/Qwen2.5-0.5B-Instruct`.

This model is used to evaluate how changes in prompt design affect model behavior during inference. The model itself is not trained during this phase.

The prompt variations progressively introduce:

1. A broad question
2. Explicit task instructions
3. A market research role and stronger grounding
4. A constrained output structure

The same source review is used throughout each scenario so that the prompt design is the primary variable being tested.

# Scenario 1: Customer Satisfaction Analysis

## Test Review

### Reference Metadata

The following information comes from the source dataset and is retained for evaluating the model's responses.

**Rating:** 4/5  
**Recommended:** Yes  
**Department:** Tops  
**Class:** Knits  

### Review Text

I ordered this in carbon for store pick up, and had a ton of stuff (as always) to try on and used this top to pair (skirts and pants). everything went with it. the color is really nice charcoal with shimmer, and went well with pencil skirts, flare pants, etc. my only compaint is it is a bit big, sleeves are long and it doesn't go in petite. also a bit loose for me, but no xxs... so i kept it and wil ldecide later since the light color is already sold out in hte smallest size...

---

## Prompt 1: Broad Baseline

### Prompt

Is the customer satisfied with this product?

### Prompting Technique

This is the baseline prompt. It asks a broad question without specifying the type of response, analytical perspective, or output format.

### Model Output

> Based on the customer's review, I would say that they are generally satisfied with the product. The reviewer mentions that the color is "really nice charcoal with shimmer" and that it goes well with various types of clothing. They also express satisfaction with the sizing, noting that the sleeves are long and not too tight.
>
> However, there are a few minor complaints:
>
> 1. The color is described as being "a bit big," which could be seen as an issue if the customer wanted something smaller.
> 2. The reviewer states that the sleeves are "loose for me, but no XXS..." This suggests that while the overall fit is good, the specific size might not meet the customer's needs.
>
> Overall, the positive aspects seem to outweigh the negative

### Observation

The baseline prompt produced a detailed answer, but the response was loosely controlled.

The model correctly identified several positive signals in the review, including the color and versatility of the top. However, it also misinterpreted some of the review text. For example, it described the customer as satisfied with the sizing even though the customer specifically complained that the item was too large and that the sleeves were too long.

The response demonstrates that a broad prompt can produce useful information, but it leaves significant freedom for the model to determine what kind of analysis to perform.

---

## Prompt 2: Explicit Classification

### Prompt

Classify the customer's overall satisfaction as positive, mixed, or negative.

Briefly explain what in the review supports your classification.

### Prompting Technique

This variation increases specificity by defining the available satisfaction categories and requiring the model to explain its classification.

### Model Output

> Based on the review provided, I would classify the customer's overall satisfaction as **mixed**. Here’s why:
>
> 1. **Positive aspects:**
>    - The reviewer mentions that everything went "with it" and that the color was "really nice charcoal with shimmer."
>    - They express satisfaction with the product's fit ("went well with pencil skirts, flare pants, etc.") and the overall appearance.
>
> 2. **Negative aspect:**
>    - There is one minor complaint about the size: "the color is really nice charcoal with shimmer, and went well with pencil skirts, flare pants, etc." However, this is presented more as an observation rather than a significant issue.
>    - The reviewer states they will keep the item if the light

### Observation

The explicit classification prompt improved the response by producing a clear satisfaction category.

The model classified the review as mixed, which better reflects the combination of positive comments and sizing concerns in the source review.

The response also became more structured because the model separated positive and negative evidence. Some interpretation errors remained, but the prompt produced a more focused market research response than the broad baseline.

---

## Prompt 3: Market Research Role

### Prompt

You are a market research analyst evaluating customer feedback.

Determine whether the customer's overall experience is positive, mixed, or negative.

Identify the strongest positive product attribute and the most important customer concern.

Base your analysis only on the review.

### Prompting Technique

This variation adds a professional role, identifies specific analytical tasks, and introduces a grounding constraint requiring the response to rely on the review.

### Model Output

> Based on the review provided, I would classify the overall experience as **mixed**. Here’s why:
>
> 1. **Positive Attributes:**
>    - The color is described as "really nice charcoal with shimmer" which is generally considered a good quality.
>    - The skirt and pants fit well, especially for the style and length.
>    - The sizing seems reasonable, though there was one minor complaint about the sleeve length being too long and not fitting perfectly for the wearer.
>
> 2. **Negative Attributes:**
>    - The main issue mentioned is that the size is slightly larger than expected, specifically for the skirts and pants. This is a significant drawback for customers who prefer smaller sizes.
>    - There is an additional complaint about the sleeve length being too long

### Observation

The market research role produced a response that was more clearly oriented toward product attributes and customer concerns.

The model maintained the mixed satisfaction classification and identified the product's color as a positive attribute while recognizing sizing and sleeve length as concerns.

The response was more useful for market research than the earlier prompts because the requested analytical categories were clearer. However, some inaccuracies remained, including confusion between the clothing that the top was paired with and the product being reviewed.

---

## Prompt 4: Structured Market Research Output

### Prompt

You are a market research analyst evaluating customer feedback for a product research report.

Analyze the review using only evidence provided by the customer.

Return your answer in exactly this format:

Satisfaction: [positive, mixed, or negative]  
Positive: [main positive product attribute]  
Concern: [main customer concern]  
Customer action: [what the customer appears likely to do]

Do not invent information that is not supported by the review.

### Prompting Technique

This variation combines role-based prompting, task specificity, source grounding, and a strict response format.

The goal is to reduce unnecessary explanation while producing information that could be used directly in a market research workflow.

### Model Output

> Satisfaction: [mixed]  
> Positive: [color]  
> Concern: [sleeves length]  
> Customer action: [keep the item]

### Observation

The structured prompt produced the most concise and controlled response of the four variations.

The model classified the review as mixed, identified the color as the main positive attribute, identified sleeve length as a concern, and recognized that the customer appeared likely to keep the item.

Unlike the earlier responses, the output closely followed the requested structure and avoided unnecessary explanation.

The model retained the square brackets from the example format, but the requested fields were completed correctly and remained grounded in the review.

---

## Scenario 1 Comparison

The prompt variations demonstrate how increasingly specific instructions changed the model's behavior.

The broad baseline produced a detailed response but gave the model significant freedom in how to interpret the task. This resulted in useful observations alongside several inaccurate interpretations.

Adding an explicit classification task produced a clearer satisfaction judgment and encouraged the model to organize supporting evidence.

Adding a market research role and specific analytical objectives further focused the response on product attributes and customer concerns, although some interpretation errors remained.

The final structured prompt produced the most controlled and immediately usable response. By defining the analyst role, limiting the model to source evidence, specifying the required fields, and constraining the response format, the prompt reduced unnecessary output and improved format adherence.

Overall, the experiment shows that prompt engineering can improve the relevance, structure, and usability of model output without changing the model's parameters.

# Scenario 2: Product Strengths and Complaints

## Test Review

### Reference Metadata

The following information comes from the source dataset and is retained for evaluating the model's responses.

**Rating:** 2/5  
**Recommended:** No  
**Department:** Dresses  
**Class:** Dresses  

### Review Text

I love tracy reese dresses, but this one is not for the very petite. i am just under 5 feet tall and usually wear a 0p in this brand. this dress was very pretty out of the package but its a lot of dress. the skirt is long and very full so it overwhelmed my small frame. not a stranger to alterations, shortening and narrowing the skirt would take away from the embellishment of the garment. i love the color and the idea of the style but it just did not work on me. i returned this dress.

---

## Prompt 1: Broad Baseline

### Prompt

What does the customer like and dislike about this product?

### Prompting Technique

This baseline asks the model to identify positive and negative feedback without specifying how the response should be organized or which details should receive priority.

### Model Output

> Based on the customer's review, they seem to have mixed feelings towards the Tracy Reese dress. They initially enjoyed the dress due to its attractive design and the fact that it matches their size perfectly. However, upon trying it on, they found that it was too large for them, specifically stating that it "overwhelmed" their small frame.
>
> The main issues they encountered were:
>
> 1. **Size**: The dress was described as being "very pretty out of the package," which suggests that it didn't fit well or accurately reflected their body type.
> 2. **Length and Fit**: The skirt was described as "long and very full," which made it difficult to fully cover their small frame.
> 3. **Adjustability**: The reviewer mentions that alterations, shortening, and narrowing the skirt could potentially detract from the overall appearance of the dress, especially if worn with other accessories.

### Observation

The broad prompt produced several relevant observations, but it also introduced inaccurate interpretations.

The model correctly recognized that the dress was attractive and that fit was the primary problem. However, it incorrectly stated that the dress matched the customer's size perfectly before later describing it as too large.

This response demonstrates that a broad request can identify major themes, but the lack of constraints allows the model to introduce interpretations that are not fully supported by the review.

---

## Prompt 2: Direct Extraction

### Prompt

Identify one thing the customer liked about this specific dress and one thing the customer disliked about this specific dress.

Do not use the customer's general opinion of the Tracy Reese brand as a product strength.

### Prompting Technique

This prompt narrows the task to two specific pieces of information and distinguishes feedback about the individual product from the customer's broader opinion of the brand.

### Model Output

> The customer liked that the dress was "very pretty out of the package" and appreciated the "color and the idea of the style." However, they found it "overwhelmed" with the dress due to its size and length, which made it difficult to fit comfortably. They also noted that alterations, shortening, and narrowing the skirt could detract from the overall design and appearance of the dress. The customer ultimately decided to return the dress after experiencing some issues with fitting and styling.

### Observation

The direct extraction prompt improved the response by focusing on product-specific feedback.

The model correctly identified positive attributes such as the appearance, color, and style of the dress. It also identified the sizing and length problem as the main source of dissatisfaction.

Compared with the broad baseline, this response was better grounded in the actual product review and avoided treating the customer's general preference for the brand as the main product strength.

---

## Prompt 3: Evidence-Grounded Analysis

### Prompt

You are a market research analyst reviewing feedback about one specific dress.

Identify:

1. The strongest positive attribute of this dress.
2. The most important complaint about this dress.

For each answer, use evidence stated directly in the review.

Important constraints:

- Analyze this dress only.
- Do not treat the customer's general preference for Tracy Reese dresses as evidence about this product.
- Do not infer qualities that the customer did not state.

### Prompting Technique

This variation adds a market research role and explicit grounding constraints.

The prompt also separates the positive attribute from the complaint and directs the model to rely only on product-specific evidence.

### Model Output

> 1. **The strongest positive attribute of this dress:**
>    - The strong positive attribute identified in the customer review is "color." The reviewer explicitly states, "I love the color," which indicates a significant positive aspect of the dress.
>
> 2. **The most important complaint about this dress:**
>    - The most important complaint identified in the customer review is "the skirt is long and very full so it overwhelmed my small frame." This statement highlights a critical feature of the dress that negatively impacted the wearer's comfort and appearance.

### Observation

The evidence-grounded prompt produced a much more precise response.

The model selected a clearly supported positive attribute, color, and paired it with direct evidence from the review.

It also identified the oversized, full skirt as the primary complaint and supported that conclusion with the customer's own description.

This version showed stronger factual grounding and reduced unsupported interpretation compared with the earlier prompts.

---

## Prompt 4: Structured Market Research Summary

### Prompt

You are a market research analyst summarizing feedback about one specific dress.

Use only information stated in the customer review.

Identify:

- one positive attribute of this specific dress
- the main problem with this specific dress
- what the customer ultimately did

Do not use the customer's general opinion of Tracy Reese as a product strength.  
Do not invent product qualities.

Return exactly this format:

Strength: [one positive attribute]  
Complaint: [main problem]  
Customer action: [what the customer did]

### Prompting Technique

This final variation combines product-specific grounding with a strict output structure.

The goal is to convert the analysis into concise information that could be used directly in a market research summary or downstream data-processing workflow.

### Model Output

> Strength: Pretty  
> Complaint: Very large size  
> Customer action: Returned the dress.

### Observation

The structured prompt produced the most concise and operationally useful response in Scenario 2.

The model identified a positive attribute of the specific dress, summarized the main sizing problem, and correctly captured the customer's final action.

The response followed the requested structure closely and avoided the broader brand-level interpretation that appeared in earlier attempts.

---

## Scenario 2 Comparison

The second scenario shows a clear progression from broad interpretation to focused product-specific analysis.

The baseline prompt identified several useful themes but also introduced contradictory and unsupported interpretations.

The direct extraction prompt improved relevance by separating what the customer liked from what they disliked and by focusing on the specific dress rather than the brand.

The evidence-grounded prompt further improved factual consistency by requiring product-specific evidence and explicitly preventing unsupported inference.

The final structured prompt converted those findings into a concise format suitable for market research reporting.

Overall, Scenario 2 demonstrates that increasingly specific instructions, grounding constraints, and output formatting can improve both the precision and usability of model-generated market research insights.

# Scenario 3: Category Comparison

## Comparison Samples

Scenario 3 compares one sampled Top review with one sampled Dress review.

These reviews are used as examples for prompt engineering only. The model is not instructed to generalize the findings to all products in either category.

### Top Review

**Department:** Tops  
**Class:** Blouses  
**Rating:** 5/5  
**Recommended:** Yes  

This shirt is very flattering to all due to the adjustable front tie. it is the perfect length to wear with leggings and it is sleeveless so it pairs well with any cardigan. love this shirt!!!

### Dress Review

**Department:** Dresses  
**Class:** Dresses  
**Rating:** 2/5  
**Recommended:** No  

I love tracy reese dresses, but this one is not for the very petite. i am just under 5 feet tall and usually wear a 0p in this brand. this dress was very pretty out of the package but its a lot of dress. the skirt is long and very full so it overwhelmed my small frame. not a stranger to alterations, shortening and narrowing the skirt would take away from the embellishment of the garment. i love the color and the idea of the style but it just did not work on me. i returned this dress.

---

## Prompt 1: Broad Baseline

### Prompt

Compare these two customer reviews.

### Prompting Technique

This baseline provides two reviews and asks for a comparison without specifying which aspects should be compared or how the answer should be structured.

### Model Output

> The Top Review:
> - The shirt has an adjustable front tie that makes it flattering.
> - It's suitable for both leggings and cardigans.
> - The reviewer loves the shirt overall.
>
> The Dress Review:
> - Tracy Reese dresses are known for their versatility.
> - The reviewer is slightly under 5'6" and wears a 0P.
> - The dress is described as "very pretty out of the package."
> - The skirt is described as "long and very full."
> - The reviewer mentions alterations, shortening, and narrowing the skirt.
> - They state they don't like how the skirt takes away from the embellishments.
> - They return the dress because they didn't like it fitting them properly.
>
> Overall, the top review highlights the flattering features of the shirt and positive experience with the dress, while the bottom review expresses dissatisfaction with the fit and design.

### Observation

The broad comparison identified several important differences, but it also introduced errors.

The model correctly recognized the positive experience in the Top review and the fit problems in the Dress review. However, it misread the customer's height and introduced unsupported claims about the Tracy Reese brand.

The loose prompt also allowed the response to become inconsistent in how the two reviews were described.

---

## Prompt 2: Explicit Comparison

### Prompt

Compare the Top review with the Dress review.

Identify the main positive point in each review and explain the biggest difference in the customers' experiences.

Use only information from the reviews.

### Prompting Technique

This variation defines the comparison criteria and adds a grounding instruction.

Instead of asking for a general comparison, it directs the model to identify a positive point for each product and then summarize the main difference between the customer experiences.

### Model Output

> **Top Review:**
> - **Main Positive Point:** The adjustable front tie allows for a flattering fit.
> - **Biggest Difference:** The customer's experience was significantly impacted by the dress being too large for their size, which caused them to feel unflattering and uncomfortable.
>
> **Dress Review:**
> - **Main Positive Point:** The dress is beautiful and has a unique design that stands out.
> - **Biggest Difference:** The customer found the dress to be overly large for their body type, resulting in an overall unsatisfactory experience. They felt like they were wearing a "package" rather than a piece of clothing, leading to disappointment and dissatisfaction.

### Observation

The explicit comparison improved focus by identifying a positive point from each review and emphasizing the difference in customer experience.

The model correctly identified the adjustable front tie as a positive feature of the Top and recognized that sizing was the primary problem with the Dress.

However, it still introduced unsupported language, including describing the dress design as unique and claiming that the customer felt like they were wearing a package.

The prompt improved task focus, but factual grounding still needed stronger constraints.

---

## Prompt 3: Market Research Comparison

### Prompt

You are a market research analyst comparing two sampled customer reviews from different product categories.

For the Top review:

- identify the main positive product attribute
- identify whether the customer experience is positive, mixed, or negative

For the Dress review:

- identify the main positive product attribute
- identify whether the customer experience is positive, mixed, or negative
- identify the main concern

Then describe the clearest difference between the two customer experiences.

Use only information in the reviews.  
Do not generalize these findings to all Tops or all Dresses.

### Prompting Technique

This variation adds a market research role, separates the analysis by product, and introduces explicit limits on generalization.

The prompt also defines which information should be extracted from each review.

### Model Output

> **Top Review:**
> - **Main Positive Product Attribute:** The adjustable front tie
> - **Customer Experience:** Positive
> - **Concerns:** Mixed (The dress is too large for the reviewer's height)
>
> **Dress Review:**
> - **Main Positive Product Attribute:** The Tracy Reese dress
> - **Customer Experience:** Negative
> - **Concerns:** Mixed (The dress does not fit properly for the reviewer's height)
> - **Reasoning:** The dress is described as "very pretty out of the package" but lacks the desired features like adjustable front ties, which are crucial for comfort and fitting. Additionally, the overall design and fit do not meet the reviewer's expectations regarding their body size.

### Observation

The market research framing improved the response by correctly classifying the Top experience as positive and the Dress experience as negative.

The model also correctly identified the adjustable front tie as the Top's strongest positive attribute and fit as the major concern in the Dress review.

However, some information from the two reviews was still mixed together. For example, the response incorrectly applied the Dress sizing issue to the Top review and suggested that the Dress lacked an adjustable front tie.

This showed that additional constraints were needed to keep information from the two sources separate.

---

## Prompt 4: Constrained Category Comparison

### Prompt

You are a market research analyst comparing two sampled customer reviews.

Analyze each review separately before comparing them.

For the experience fields, you MUST use exactly one of these three labels:

positive  
mixed  
negative  

For the strength fields, identify something the customer explicitly liked about that specific product.

For the concern field, identify something the customer explicitly disliked or found problematic.

Important rules:

- Do not mix information between the two reviews.
- Do not use general opinions about a brand.
- Do not invent information.
- Do not treat a complaint as a strength.
- Do not make claims about all Tops or all Dresses.
- Complete all six fields.

Return exactly six lines in this format:

Top experience: [positive, mixed, or negative]  
Top strength: [positive attribute from the Top review]  
Dress experience: [positive, mixed, or negative]  
Dress strength: [positive attribute from the Dress review]  
Dress concern: [negative issue from the Dress review]  
Key difference: [difference between the two customers' overall experiences]

### Prompting Technique

This final variation adds strict separation between the two source reviews, controlled classification labels, explicit anti-hallucination constraints, and a fixed output structure.

The goal is to prevent information from one review from being incorrectly transferred to the other while producing a concise category-comparison summary.

### Model Output

> Top experience: positive  
> Top strength: adjustable front tie  
> Dress experience: negative  
> Dress strength: very pretty out of the package  
> Dress concern: too long and full skirt  
> Key difference: struggled with alterations, shortening, and changing skirt size

### Observation

The constrained prompt produced the most controlled response in Scenario 3.

The model correctly classified the Top customer experience as positive and identified the adjustable front tie as the main positive attribute.

For the Dress review, it correctly classified the experience as negative, identified the appearance of the dress as a positive attribute, and identified the long, full skirt as the main concern.

Most importantly, the response kept the two reviews separate and did not transfer product details from one review to the other.

The Key difference field was somewhat awkwardly phrased, but it remained grounded in the Dress review rather than introducing unsupported information.

---

## Scenario 3 Comparison

Scenario 3 demonstrates the importance of prompt structure when comparing multiple sources.

The broad baseline identified useful differences between the reviews but also introduced unsupported claims and interpretation errors.

The explicit comparison improved task focus but still allowed the model to add information that was not present in the source reviews.

The market research prompt improved classification and analytical framing, but the model still mixed details between the two products.

The final constrained prompt produced the strongest result by requiring the model to analyze each review separately, limiting the allowed classification labels, preventing unsupported generalization, and enforcing a fixed output structure.

Overall, the scenario shows that source separation and explicit grounding constraints are especially important when a prompt asks a model to compare multiple pieces of market research data.

# Prompt Engineering Conclusion

Across all three scenarios, the results show that prompt design had a clear effect on the usefulness of model responses.

Broad prompts often produced relevant information, but they also gave the model enough freedom to introduce inaccurate interpretations or unsupported details.

Adding explicit task requirements improved focus. Role-based prompting helped orient the model toward market research analysis, while grounding constraints reduced unsupported interpretations.

The strongest results generally came from prompts that combined a clearly defined task with explicit source limitations and a structured output format.

The experiments demonstrate that prompt engineering does not change the model's parameters. Instead, it changes how the model is instructed during inference. More precise prompts improved the relevance, factual grounding, format adherence, and practical usability of the generated market research insights.