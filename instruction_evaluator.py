import re


def evaluate_instruction_response(response):
    text = response.lower()

    recursion_terms = [
        "recursion",
        "recursive",
        "calls itself",
        "itself",
    ]

    real_world_terms = [
        "real-world",
        "real world",
        "family tree",
        "directory",
        "folder",
        "file system",
        "tree",
        "stack of plates",
        "countdown",
    ]

    explanation_terms = [
        "because",
        "example",
        "base case",
        "recursive step",
        "smaller",
        "simpler",
        "step",
    ]

    has_recursion = any(term in text for term in recursion_terms)
    has_real_world_example = any(term in text for term in real_world_terms)
    has_explanation = any(term in text for term in explanation_terms)

    return (
        has_recursion
        and has_real_world_example
        and has_explanation
    )