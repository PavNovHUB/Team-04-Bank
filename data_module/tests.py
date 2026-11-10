import unittest
import tempfile
import csv
from .storage import import_transactions, load_saved_transactions
from .validator import validate_transaction
from .csv_loader import load_csv
from pathlib import Path
from .xlsx_exporter import export_to_xlsx
from openpyxl import load_workbook
folder = Path(__file__).resolve().parent.parent
csv_file = folder / "transactions_test.csv"

class TransactionTests(unittest.TestCase):



    def test_valid_transaction(self):
        transaction = {
            "id": "1",
            "date": "2026-11-09",
            "type": "доход",
            "category": "Зарплата",
            "amount": "1000.00",
            "description": "Тест"
        }
        errors = validate_transaction(transaction)
        self.assertEqual(errors, [])

    def test_empty_xlsx_export(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            xlsx_file = Path(temp_dir) / "empty_report.xlsx"

            export_to_xlsx([], xlsx_file)

            self.assertTrue(xlsx_file.exists())

            workbook = load_workbook(xlsx_file)

            self.assertEqual(
                workbook.sheetnames,
                ["Данные", "Итоги"]
            )

            data_sheet = workbook["Данные"]
            summary_sheet = workbook["Итоги"]

            self.assertEqual(data_sheet.max_row, 1)
            self.assertEqual(
                data_sheet.cell(1, 1).value,
                "id"
            )

            self.assertEqual(summary_sheet.cell(2, 2).value, 0)
            self.assertEqual(summary_sheet.cell(3, 2).value, 0)
            self.assertEqual(summary_sheet.cell(4, 2).value, 0)
            self.assertEqual(summary_sheet.cell(5, 2).value, 0)

            workbook.close()

    def test_negative_amount(self):
        transaction = {
            "id": "2",
            "date": "2026-11-09",
            "type": "расход",
            "category": "Еда",
            "amount": "-100",
            "description": "Тест"
        }
        errors = validate_transaction(transaction)
        self.assertIn("Сумма должна быть положительной", errors)

    def test_invalid_date(self):
        transaction = {
            "id": "3",
            "date": "2026-13-45",
            "type": "доход",
            "category": "Зарплата",
            "amount": "1000",
            "description": "Тест"
        }
        errors = validate_transaction(transaction)
        self.assertIn("Неверный формат даты", errors)

    def test_zero_amount(self):
        transaction = {
            "id": "4",
            "date": "2026-11-09",
            "type": "расход",
            "category": "Еда",
            "amount": "0",
            "description": "Тест"
        }
        errors = validate_transaction(transaction)
        self.assertIn("Сумма должна быть положительной", errors)

    def test_too_many_decimal_places(self):
        transaction = {
            "id": "5",
            "date": "2026-11-09",
            "type": "доход",
            "category": "Зарплата",
            "amount": "1000.123",
            "description": "Тест"
        }
        errors = validate_transaction(transaction)
        self.assertIn(
            "Допускается не более двух знаков после запятой",
            errors
        )

    def test_duplicate_ids_in_csv(self):
        transactions, errors = load_csv(csv_file)
        self.assertEqual(transactions, [])
        self.assertTrue(any("Повторяющийся ID" in error for error in errors))

    def test_existing_id(self):
        transactions, errors =load_csv(
    csv_file,
    existing_ids={"10"}
)
        self.assertEqual(transactions, [])
        self.assertTrue(any("Повторяющийся ID" in error for error in errors))

    def test_successful_import(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            csv_file = folder / "new_transactions.csv"
            storage_file = folder / "saved_transactions.csv"

            with open(csv_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "id", "date", "type",
                    "category", "amount", "description"
                ])

                writer.writerow([
                    "100", "2026-11-09", "доход",
                    "Зарплата", "1000.00", "Тест"
                ])

            errors = import_transactions(csv_file, storage_file)

            saved = load_saved_transactions(storage_file)

            self.assertEqual(errors, [])
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved[0]["id"], "100")

    def test_failed_import_does_not_change_storage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            csv_file = folder / "new_transactions.csv"
            storage_file = folder / "saved_transactions.csv"

            headers = [
                "id", "date", "type",
                "category", "amount", "description"
            ]

            # Создаём старое хранилище
            with open(storage_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow([
                    "100", "2026-11-09", "доход",
                    "Зарплата", "1000.00", "Старая операция"
                ])

            # Создаём файл с повторяющимся ID
            with open(csv_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow([
                    "100", "2026-11-10", "расход",
                    "Еда", "500.00", "Новая операция"
                ])

            errors = import_transactions(csv_file, storage_file)
            saved = load_saved_transactions(storage_file)

            self.assertTrue(errors)
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved[0]["description"], "Старая операция")

    def test_failed_import_with_invalid_date_does_not_change_storage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            csv_file = folder / "bad_transactions.csv"
            storage_file = folder / "saved_transactions.csv"

            with open(storage_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "id", "date", "type",
                    "category", "amount", "description"
                ])
                writer.writerow([
                    "200", "2026-11-09", "доход",
                    "Зарплата", "1000.00", "Старая операция"
                ])

            with open(csv_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "id", "date", "type",
                    "category", "amount", "description"
                ])
                writer.writerow([
                    "201", "неправильная дата", "доход",
                    "Зарплата", "500.00", "Новая операция"
                ])

            errors = import_transactions(csv_file, storage_file)
            saved = load_saved_transactions(storage_file)

            self.assertTrue(errors)
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved[0]["id"], "200")

    def test_successful_import_appends_transactions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            csv_file = folder / "new_transactions.csv"
            storage_file = folder / "saved_transactions.csv"

            headers = [
                "id", "date", "type",
                "category", "amount", "description"
            ]

            # Существующая операция
            with open(storage_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow([
                    "300", "2026-11-09", "доход",
                    "Зарплата", "1000.00", "Старая операция"
                ])

            # Новая операция
            with open(csv_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow([
                    "301", "2026-11-10", "расход",
                    "Еда", "500.00", "Новая операция"
                ])

            errors = import_transactions(csv_file, storage_file)
            saved = load_saved_transactions(storage_file)

            self.assertEqual(errors, [])
            self.assertEqual(len(saved), 2)
            self.assertEqual(saved[0]["id"], "300")
            self.assertEqual(saved[1]["id"], "301")

    def test_missing_required_column(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "bad.csv"

            # Не хватает столбца description
            with open(csv_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "id", "date", "type", "category", "amount"
                ])
                writer.writerow([
                    "400", "2026-11-10", "доход",
                    "Зарплата", "1000.00"
                ])

            transactions, errors = load_csv(csv_file)

            self.assertEqual(transactions, [])
            self.assertTrue(any("description" in error for error in errors))

    def test_empty_csv_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "empty.csv"

            # Создаём пустой CSV
            csv_file.touch()

            transactions, errors = load_csv(csv_file)

            self.assertEqual(transactions, [])
            self.assertTrue(errors)
            self.assertIn(
                "Файл пустой или не содержит заголовков",
                errors
            )

    def test_collects_errors_from_multiple_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "bad.csv"

            with open(csv_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "id", "date", "type",
                    "category", "amount", "description"
                ])

                writer.writerow([
                    "501", "неправильная дата", "доход",
                    "Зарплата", "1000", "Тест 1"
                ])

                writer.writerow([
                    "502", "2026-11-10", "покупка",
                    "Еда", "500", "Тест 2"
                ])

                writer.writerow([
                    "503", "2026-11-10", "расход",
                    "Еда", "-100", "Тест 3"
                ])

            transactions, errors = load_csv(csv_file)

            self.assertEqual(transactions, [])
            self.assertGreaterEqual(len(errors), 3)

            self.assertTrue(any("Строка 2" in error for error in errors))
            self.assertTrue(any("Строка 3" in error for error in errors))
            self.assertTrue(any("Строка 4" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
