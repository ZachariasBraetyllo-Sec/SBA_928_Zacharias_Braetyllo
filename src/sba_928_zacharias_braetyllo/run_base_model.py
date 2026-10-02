import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

SCENARIO_1_REVIEW = """
I ordered this in carbon for store pick up, and had a ton of stuff (as always) to try on and used this top to pair (skirts and pants). everything went with it. the color is really nice charcoal with shimmer, and went well with pencil skirts, flare pants, etc. my only compaint is it is a bit big, sleeves are long and it doesn't go in petite. also a bit loose for me, but no xxs... so i kept it and wil ldecide later since the light color is already sold out in hte smallest size...
""".strip()

SCENARIO_2_REVIEW = """
I love tracy reese dresses, but this one is not for the very petite. i am just under 5 feet tall and usually wear a 0p in this brand. this dress was very pretty out of the package but its a lot of dress. the skirt is long and very full so it overwhelmed my small frame. not a stranger to alterations, shortening and narrowing the skirt would take away from the embellishment of the garment. i love the color and the idea of the style but it just did not work on me. i returned this dress.
""".strip()

PROMPTS = {
    "Scenario 1 - Prompt 1 - Broad Baseline": f"""
Is the customer satisfied with this product?

Customer review:
{SCENARIO_1_REVIEW}
""".strip(),

    "Scenario 1 - Prompt 2 - Specific Analysis": f"""
Classify the customer's overall satisfaction as positive, mixed, or negative.

Briefly explain what in the review supports your classification.

Customer review:
{SCENARIO_1_REVIEW}
""".strip(),

    "Scenario 1 - Prompt 3 - Market Research Role": f"""
You are a market research analyst evaluating customer feedback.

Determine whether the customer's overall experience is positive, mixed, or negative.

Identify the strongest positive product attribute and the most important customer concern.

Base your analysis only on the review.

Customer review:
{SCENARIO_1_REVIEW}
""".strip(),

    "Scenario 1 - Prompt 4 - Structured Market Research Output": f"""
You are a market research analyst evaluating customer feedback for a product research report.

Analyze the review using only evidence provided by the customer.

Return your answer in exactly this format:

Satisfaction: [positive, mixed, or negative]
Positive: [main positive product attribute]
Concern: [main customer concern]
Customer action: [what the customer appears likely to do]

Do not invent information that is not supported by the review.

Customer review:
{SCENARIO_1_REVIEW}
""".strip(),

    "Scenario 2 - Prompt 1 - Broad Baseline": f"""
What does the customer like and dislike about this product?

Customer review:
{SCENARIO_2_REVIEW}
""".strip(),

    "Scenario 2 - Prompt 2 - Direct Extraction": f"""
Identify one thing the customer liked about this specific dress and one thing the customer disliked about this specific dress.

Do not use the customer's general opinion of the Tracy Reese brand as a product strength.

Customer review:
{SCENARIO_2_REVIEW}
""".strip(),

    "Scenario 2 - Prompt 3 - Evidence-Grounded Analysis": f"""
You are a market research analyst reviewing feedback about one specific dress.

Identify:

1. The strongest positive attribute of this dress.
2. The most important complaint about this dress.

For each answer, use evidence stated directly in the review.

Important constraints:
- Analyze this dress only.
- Do not treat the customer's general preference for Tracy Reese dresses as evidence about this product.
- Do not infer qualities that the customer did not state.

Customer review:
{SCENARIO_2_REVIEW}
""".strip(),

    "Scenario 2 - Prompt 4 - Structured Market Research Summary": f"""
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

Customer review:
{SCENARIO_2_REVIEW}
""".strip(),
}


def generate_response(tokenizer, model, instruction):
    messages = [
        {
            "role": "user",
            "content": instruction,
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(text, return_tensors="pt")

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=180,
            do_sample=False,
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()


def main():
    print(f"Loading prompt-engineering model: {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
    )
    model.eval()

    for prompt_name, prompt in PROMPTS.items():
        response = generate_response(tokenizer, model, prompt)

        print("\n" + "=" * 70)
        print(prompt_name)
        print("=" * 70)
        print(response)


if __name__ == "__main__":
    main()