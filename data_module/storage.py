import csv
import os
from .csv_loader import load_csv

def load_saved_transactions(file_path):
    transactions = []

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transactions.append(row)

    except FileNotFoundError:
        return []

    return transactions
def save_transactions(file_path, transactions):
    temp_path = str(file_path) + ".tmp"

    with open(temp_path, "w", encoding="utf-8", newline="") as file:
        fieldnames = [
            "id", "date", "type",
            "category", "amount", "description"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

    os.replace(temp_path, file_path)


def import_transactions(csv_file, storage_file):
    saved = load_saved_transactions(storage_file)

    saved_ids = set()

    for transaction in saved:
        saved_ids.add(transaction["id"])

    new_transactions, errors = load_csv(csv_file, saved_ids)

    if errors:
        return errors

    all_transactions = saved + new_transactions

    save_transactions(storage_file, all_transactions)

    return []