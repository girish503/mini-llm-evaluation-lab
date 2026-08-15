# Mini LLM Evaluation Lab

A lightweight local framework for evaluating Large Language Model responses using task-specific automated evaluators.

## Overview

This project demonstrates a practical LLM evaluation pipeline:

```text
Prompts
   ↓
Ollama + Qwen
   ↓
Generated Responses
   ↓
Task-Specific Evaluators
   ↓
Evaluation Results
   ↓
Metrics