# Output Validation

Extend natural-language-to-SQL generation with schema checks, consistency checks, business rules, and correction retries.

## Scope

Input: 30 requests in [samples.json](assets/samples.json), covering ordinary queries, joins/aggregations, prohibited writes, sensitive data, and unavailable tables.

Output fields: `query` (SQL or null), `required_query_type` (string), and `tables_used` (list or null). A null query represents refusal or an unsupported request.

Validation layers in `agents/llm_agent.py`:

| Layer | Checks |
| --- | --- |
| Schema | Valid JSON, strict Pydantic types, required fields, no extras |
| Consistency | Query/table presence agrees; declared tables are allowed; SQL starts with its declared type |
| Business rules | Non-SELECT requests and sensitive-keyword requests must return null SQL |

Allowed tables: `customers`, `products`, `orders`, `sales`, `categories`, `countries`.

## Workflow

1. Select each Groq model's JSON mode/schema and load its prompt.
2. Generate output and apply all validation layers.
3. On invalid output, send the error and request back for correction: up to three retries after the initial attempt.
4. Return validated output or failure details; save per-model JSON in [assets/output](assets/output/) and diagnostics in [logs.txt](assets/logs.txt).
5. Score validation success, query-type agreement, and exact table-set agreement over all 30 samples.

## Results

Scores from `assets/logs.txt`:

| Model | Validation | Query type | Table set |
| --- | ---: | ---: | ---: |
| Llama 3.1 8B | 96.7% | 96.7% | 70.0% |
| Qwen3 32B | 96.7% | 96.7% | 76.7% |
| GPT-OSS 120B | 100% | 100% | 93.3% |
| Llama 3.3 70B | 100% | 100% | 93.3% |

GPT-OSS and Llama 70B performed best on these checks. Validation success includes valid refusals. It does not prove SQL correctness: checks inspect declared metadata and prefixes, without parsing/executing SQL. The saved log even accepts an `orders` query for an unavailable `invoices` request.
