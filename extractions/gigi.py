import csv

input_file = "../data/result_data_movies.csv"          # fisierul tau original
output_file = "../data/budget_unique.csv" # fisierul cu bugete unice

unique_budgets = set()

with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        budget = row["Budget"].strip()
        if budget:
            unique_budgets.add(budget)

# scriem valorile unice intr-un fisier nou
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Budget"])
    for b in sorted(unique_budgets):
        writer.writerow([b])

print(f"Am extras {len(unique_budgets)} valori unice în {output_file}")