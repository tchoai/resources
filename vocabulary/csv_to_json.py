import json
import os
import argparse
from collections import defaultdict

path_csv = "./csv"
path_json = "./json"
ID_LENGTH = 2


def to_json(file):
    vocabulary = defaultdict(lambda: defaultdict(list))
    csv_file = os.path.join(path_csv, file)
    json_file = os.path.join(path_json, file.replace(".csv", ".json"))

    with open(csv_file, encoding="utf-8") as f:
        rows = f.readlines()
        headers = rows[0].strip().split(",")
        languages = headers[ID_LENGTH:]

        for row in rows[1:]:
            parts = row.strip().split(",")
            level = int(parts[0])
            pos = parts[1]
            word_entry = {
                lang: parts[idx + ID_LENGTH] for idx, lang in enumerate(languages)
            }
            vocabulary[level][pos].append(word_entry)

    # Ensure empty lists are included if no words exist for a pos in a level
    all_levels = set(range(1, max(vocabulary.keys(), default=0) + 1))
    all_pos = {"adjective", "noun", "verb"}

    for level in all_levels:
        if level not in vocabulary:
            vocabulary[level] = {}
        for pos in all_pos:
            if pos not in vocabulary[level]:
                vocabulary[level][pos] = []

    vocabulary = {level: dict(pos_data) for level, pos_data in vocabulary.items()}

    os.makedirs(path_json, exist_ok=True)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)

    print(f"JSON saved to {json_file}")
    return len(rows) - 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    csv_files = [f for f in os.listdir(path_csv) if f.endswith(".csv")]

    index_data = {}

    for csv_file in csv_files:
        num_rows = to_json(csv_file)
        index_data[csv_file.replace(".csv", "")] = num_rows

    index_path = os.path.join(path_json, "_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
