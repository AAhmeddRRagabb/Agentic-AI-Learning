# Structured Output Format

Convert natural-language requests into SQL while comparing model-specific structured-output modes.

## Scope

Input: 20 low-, medium-, and high-complexity requests in [samples.json](assets/samples.json). Output follows the Pydantic schema in `core/schemas.py`:

| Field | Required value |
| --- | --- |
| `query` | SQL string |
| `query_type` | SELECT, INSERT, UPDATE, DELETE, AGGREGATE, JOIN, SUBQUERY, or OTHER |
| `tables_used` | List of table names |

Extra fields are forbidden. `core/response_formats.py` selects strict JSON Schema, best-effort JSON Schema, or JSON-object mode according to its model lists. The configured experiment tests Llama 3.1 8B, Llama 3.3 70B, and Llama 4 Scout; strict mode is available but not enabled in that run.

## Workflow

1. Load samples and initialize the Groq client.
2. Select each model's response format and matching prompt.
3. Generate SQL JSON; parse and validate it with Pydantic.
4. If validation fails, remove reasoning tags/Markdown fences and try parsing again without another model call.
5. Log outputs and count unrecoverable failures per model.

## Results

[output.txt](assets/output.txt) records **0 failures across 20 requests for each of the three models**. All 60 outputs passed directly (`valid_schema: True`), without cleanup.

This establishes formatting compliance for the saved run. SQL is not executed, and query correctness, table existence, and business rules are not evaluated here.

