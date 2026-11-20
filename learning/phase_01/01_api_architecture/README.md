# API Architecture

Build one interface for calling LLMs from Groq and Google Gemini. The task demonstrates how provider wrappers keep application logic independent of SDK-specific calls.

## Scope

- `core.py`: selects the provider and exposes shared `generate()` / `stream()` functions.
- `providers/`: wraps each SDK, prepares input, and extracts response text.
- `helpers/config.py`: loads API keys and defines provider/model names.
- `main.py`: sends the same software-engineering question to both providers using regular and streaming calls.

## Workflow

1. Load `GROQ_API_KEY` and `GOOGLE_API_KEY`.
2. Choose provider, model, prompt, temperature, token limit, and `top_p`.
3. Route the request to the matching wrapper; unsupported providers raise `ValueError`.
4. Return generated text, optionally the complete SDK response, or yield streamed text chunks.
5. Print both providers' responses for comparison.

The interface shares routing and response handling; generation options still use each SDK's parameter names (`max_tokens` versus `max_output_tokens`).

## Expected result

A successful run prints two complete answers, followed by streamed answers from both providers. Full-response mode exposes SDK metadata alongside text.
