import csv
import argparse
import os

path = "./topic"


def sort_csv(input_csv):
    file_csv = os.path.join(path, input_csv)
    with open(file_csv, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        data = list(reader)

    # Remove duplicates (if same pos and word)
    seen = set()
    unique_data = []
    for row in data:
        key = (row["pos"], row["en"].strip())
        if key not in seen:
            seen.add(key)
            unique_data.append(row)

    columns = reader.fieldnames

    # Sort based on the header columns
    sorted_data = sorted(
        unique_data,
        key=lambda x: [
            x[col] if not x[col].isdigit() else int(x[col]) for col in columns
        ],
    )

    with open(file_csv, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)

    print(f"CSV file '{file_csv}' has been sorted by columns {columns}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]
    for csv_file in csv_files:
        sort_csv(csv_file)
