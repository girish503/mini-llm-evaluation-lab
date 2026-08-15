import re


def evaluate_math_response(prompt, response, expected_answer):
    expression_match = re.search(
        r"(\d+(?:\.\d+)?)\s*([*+\-/])\s*(\d+(?:\.\d+)?)",
        prompt
    )

    if not expression_match:
        return False

    left = float(expression_match.group(1))
    operator = expression_match.group(2)
    right = float(expression_match.group(3))

    if operator == "*":
        calculated_answer = left * right
    elif operator == "+":
        calculated_answer = left + right
    elif operator == "-":
        calculated_answer = left - right
    elif operator == "/":
        calculated_answer = left / right
    else:
        return False

    left_text = expression_match.group(1)
    right_text = expression_match.group(3)

    patterns = [
        rf"{re.escape(left_text)}\s*(?:\*|×|\\times)\s*{re.escape(right_text)}\s*=\s*(\d+(?:\.\d+)?)",

        rf"{re.escape(left_text)}\s+multiplied\s+by\s+{re.escape(right_text)}\s+equals\s+(\d+(?:\.\d+)?)",

        rf"the\s+product\s+of\s+{re.escape(left_text)}\s+and\s+{re.escape(right_text)}\s+is\s+(\d+(?:\.\d+)?)",
    ]

    model_answer = None

    for pattern in patterns:
        match = re.search(pattern, response, re.I)

        if match:
            model_answer = float(match.group(1))
            break

    if model_answer is None:
        return False

    return model_answer == calculated_answer == float(expected_answer)