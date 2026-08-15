import csv
import urllib.request
import json


with open("data/prompts.csv", "r", encoding="utf-8") as file:
    prompts = list(csv.DictReader(file))


for index, prompt_row in enumerate(prompts, start=1):

    prompt = prompt_row["prompt"]
    run_id = f"run_{index:03d}"

    data = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    print("\n" + "=" * 60)
    print("Run:", run_id)
    print("Prompt:")
    print(prompt)

    print("\nModel response:")
    print(result["response"])

    with open(
        "data/responses.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            prompt,
            "qwen2.5:1.5b",
            result["response"],
            run_id
        ])

    print("Response saved to responses.csv")