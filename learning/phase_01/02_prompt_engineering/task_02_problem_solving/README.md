# Prompt Engineering: Problem Solving

Compare prompts and models on 14 everyday math problems, measuring numerical answers, units, and JSON compliance separately.

## Scope

- Input: [problem_solving_examples.json](data/problem_solving_examples.json), containing problems, expected answers, and units.
- Output: JSON with `answer`, `unit`, and `solving_steps`.
- Prompts: `v1` (basic instructions), `v2` (adds output/unit constraints), `one_shot` (adds a worked example).
- Models: Groq-hosted Llama 3.1 8B and Qwen3 32B; temperature `0`, token limit `256`.

## Workflow

1. Load samples and run each model/prompt combination.
2. Request the solution, remove `<think>` blocks, and parse JSON.
3. Check required keys; compare integer-converted answers and case-insensitive units with reference values.
4. Count invalid output as unsuccessful; report answer, unit, and required-field scores over all 14 samples.
5. Save prompts, raw responses, parsed solutions, and errors to [output_file.txt](data/output_file.txt); print aggregate scores.

## Results

Counts below are reconstructed from the saved log. Each column is out of 14; failed parsing receives no answer/unit credit.

| Model | Prompt | Parsed with required fields | Correct answer | Matching unit |
| --- | --- | ---: | ---: | ---: |
| Llama 8B | v1 | 13 | 12 | 13 |
| Llama 8B | v2 | 13 | 12 | 13 |
| Llama 8B | One-shot | 14 | 12 | 14 |
| Qwen 32B | v1 | 4 | 4 | 4 |
| Qwen 32B | v2 | 6 | 6 | 4 |
| Qwen 32B | One-shot | 7 | 7 | 7 |

One-shot improved formatting without improving Llama's answer count. Qwen frequently exhausted the short token budget before completing JSON; exact unit matching also penalized `pound` versus `pounds`. These results apply to this dataset and configuration.

