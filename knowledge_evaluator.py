import re


def evaluate_knowledge_response(response, expected_answer):
    expected = expected_answer.strip()

    if not expected:
        return False

    pattern = rf"\b{re.escape(expected)}\b"

    return bool(re.search(pattern, response, re.IGNORECASE))