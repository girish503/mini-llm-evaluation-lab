import csv


with open("data/evaluation_results.csv", "r", encoding="utf-8") as file:
    results = list(csv.DictReader(file))


total_evaluated = len(results)

passed = sum(
    1
    for row in results
    if row["correct"].lower() == "true"
)

failed = sum(
    1
    for row in results
    if row["correct"].lower() == "false"
)


if total_evaluated > 0:
    pass_rate = (passed / total_evaluated) * 100
else:
    pass_rate = 0


print("Total evaluated:", total_evaluated)
print("Passed:", passed)
print("Failed:", failed)
print(f"Pass rate: {pass_rate:.2f}%")