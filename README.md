# Mini LLM Evaluation Lab

A lightweight, dependency-free framework for evaluating LLM responses with **task-specific automated evaluators** — no API keys, no cloud, everything runs locally.

## Why this exists

Most LLM eval setups either call an expensive judge model or rely on vibes. This lab takes a different approach: for well-defined task categories, **deterministic, code-based evaluators** give you fast, reproducible PASS/FAIL verdicts and a single pass-rate number you can track across runs.

## Pipeline

```text
prompts.csv
    ↓
Ollama (qwen2.5:1.5b)          ← main.py: generate responses
    ↓
responses.csv
    ↓
Task-specific evaluators       ← evaluate.py: route by category
    ↓
evaluation_results.csv
    ↓
Pass-rate metrics               ← metrics.py: aggregate
```

## The 4 evaluators

Each evaluator is matched to what its task category actually requires:

| Category | File | How it judges |
|---|---|---|
| **Math** | `evaluator.py` | Regex-extracts the arithmetic expression from the prompt, computes the answer independently, then searches the response for the result across multiple phrasings (`12 * 8 = 96`, "multiplied by… equals…", "the product of…"). PASS only if the model's answer matches the computed answer. |
| **Knowledge** | `knowledge_evaluator.py` | Checks the expected answer appears in the response (word-boundary, case-insensitive match). |
| **Coding** | `coding_evaluator.py` | Extracts the ```python block, AST-parses it, locates the target function, executes it in a **sandboxed namespace with builtins stripped**, and runs it against 3 test cases (incl. negative and float inputs). PASS only if all 3 pass. |
| **Instruction Following** | `instruction_evaluator.py` | Keyword-coverage check across 3 required dimensions: recursion terminology, a real-world example, and explanation structure. PASS only if all three are present. |

## Repo structure

```text
├── main.py                  # sends prompts to local Ollama, saves responses
├── evaluate.py              # routes responses to the right evaluator
├── metrics.py               # aggregates results → pass rate
├── evaluator.py             # math evaluator
├── knowledge_evaluator.py   # factual-answer evaluator
├── coding_evaluator.py      # sandboxed code-execution evaluator
├── instruction_evaluator.py # instruction-following evaluator
└── data/
    ├── prompts.csv          # prompt, category, expected_answer
    ├── responses.csv        # generated responses (per run)
    └── evaluation_results.csv
```

## Quickstart

Requirements: Python 3 + [Ollama](https://ollama.com) running locally with `qwen2.5:1.5b` pulled. Zero third-party Python dependencies — stdlib only.

```bash
# 1. Add your test cases (prompt, category, expected_answer)
#    Categories: Math | Knowledge | Coding | Instruction Following
nano data/prompts.csv

# 2. Generate responses via local Ollama
python main.py

# 3. Run the task-specific evaluators
python evaluate.py

# 4. See the aggregate score
python metrics.py
```

Sample run on the bundled 4-prompt set (qwen2.5:1.5b): **4/4 PASS** — see `data/evaluation_results.csv`.

## Evaluation methodology

- **Deterministic over LLM-as-judge:** rule-based checks are cheap, reproducible, and debuggable — the right tool for well-scoped tasks.
- **Category-routed:** one generic scorer can't fairly judge math and code; each category gets an evaluator built for its failure modes.
- **Sandboxed execution:** model-generated code never runs with full builtins — the coding evaluator compiles and executes in a restricted namespace.
- **Tracked over time:** every run appends to `evaluation_results.csv`, so pass rates are comparable across models and prompt revisions.

## Limitations & next steps

- Sample set is small (4 prompts) — the framework is built to scale to hundreds; expanding `prompts.csv` and tracking per-category pass rates is the planned next step.
- Evaluators are strict by design (exact-match style); fuzzy/partial-credit scoring is a planned extension.
