import csv

from evaluator import evaluate_math_response
from knowledge_evaluator import evaluate_knowledge_response
from coding_evaluator import evaluate_coding_response
from instruction_evaluator import evaluate_instruction_response


# Load prompts
with open("data/prompts.csv", "r", encoding="utf-8") as file:
    prompts = list(csv.DictReader(file))


# Load model responses
with open("data/responses.csv", "r", encoding="utf-8") as file:
    responses = list(csv.DictReader(file))


print("Prompts:", len(prompts))
print("Responses:", len(responses))


for response_row in responses:

    # Find matching prompt
    matching_prompt = next(
        (
            prompt_row
            for prompt_row in prompts
            if prompt_row["prompt"] == response_row["prompt"]
        ),
        None
    )

    if matching_prompt is None:
        print("Prompt not found:", response_row["prompt"])
        continue

    prompt = response_row["prompt"]
    response = response_row["response"]
    category = matching_prompt["category"]
    expected_answer = matching_prompt["expected_answer"]

    print("\n" + "=" * 60)
    print("Run:", response_row["run_id"])
    print("Prompt:", prompt)
    print("Category:", category)
    print("Expected:", expected_answer)

    # Select evaluator based on category
    if category == "Math":

        correct = evaluate_math_response(
            prompt,
            response,
            expected_answer
        )

    elif category == "Knowledge":

        correct = evaluate_knowledge_response(
            response,
            expected_answer
        )

    elif category == "Coding":

        correct = evaluate_coding_response(
            response
        )

    elif category == "Instruction Following":

        correct = evaluate_instruction_response(
            response
        )

    else:

        correct = None

    # Convert result into a readable status
    if correct is True:
        status = "PASS"

    elif correct is False:
        status = "FAIL"

    else:
        status = "NOT EVALUATED"

    print("Result:", status)

    # Save evaluation result
    with open(
        "data/evaluation_results.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            prompt,
            response_row["model"],
            response_row["run_id"],
            category,
            correct
        ])