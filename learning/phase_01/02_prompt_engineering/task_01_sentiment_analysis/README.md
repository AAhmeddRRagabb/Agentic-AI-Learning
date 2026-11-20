# Prompt Engineering: Sentiment Analysis

Test how prompt design and generation settings affect movie-review classification using `openai/gpt-oss-120b` model.

## Scope

Input: 10 labeled reviews in [movie_sentiment_samples.json](data/movie_sentiment_samples.json). Target output: exactly `positive`, `negative`, or `neutral`.

Five prompt styles progressively add guidance:

| Prompt | Added guidance |
| --- | --- |
| Generic | Basic classification request |
| Structured | Platform context and assigned role |
| Constrained | Explicit labels and one-word output |
| One-shot | One labeled example |
| Few-shot | Examples covering all three labels |

Prompts live in `prompts/prompts.py`; `core/generation.py` and `providers/groq.py` handle requests.

## Workflow

1. Load API settings and labeled reviews.
2. Test all five prompts with temperatures `0` / `0.2` and token limits `1` / `512`: 20 combinations, 200 requests if completed.
3. Lowercase and trim each prediction; compare it directly with the expected label.
4. Print each prediction and report accuracy (`correct / 10`) for every combination.

Extra explanation or an incomplete label counts as incorrect, so the score measures output compliance as well as classification.

## Expected result

The console should show reviews, actual/predicted labels, and a comparison of prompt/settings accuracy. Clear constraints and examples are intended to improve consistency; the experiment determines whether they do.
