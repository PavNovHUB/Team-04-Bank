import csv
from .validator import validate_transaction

def load_csv(file_path, existing_ids=None):
    transactions = []
    errors = []
    existing_ids = set(existing_ids or [])

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            required_fields = [
                "id", "date", "type",
                "category", "amount", "description"
            ]

            if not reader.fieldnames:
                return [], ["Файл пустой или не содержит заголовков"]

            for field in required_fields:
                if field not in reader.fieldnames:
                    errors.append(f"Отсутствует столбец: {field}")

            if errors:
                return [], errors

            used_ids = set(existing_ids)

            for row_number, row in enumerate(reader, start=2):
                row_errors = validate_transaction(row)
                transaction_id = row.get("id")

                if transaction_id and transaction_id in used_ids:
                    row_errors.append("Повторяющийся ID")
                elif transaction_id:
                    used_ids.add(transaction_id)

                for error in row_errors:
                    errors.append(f"Строка {row_number}: {error}")

                transactions.append(row)

    except FileNotFoundError:
        return [], ["Файл не найден"]

    except OSError as error:
        return [], [f"Ошибка чтения файла: {error}"]

    if errors:
        return [], errors

    return transactions, []