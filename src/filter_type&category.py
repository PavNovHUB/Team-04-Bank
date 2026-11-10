
from datetime import datetime


class FilterModule:
    @staticmethod
    def filter_and_search_transactions(transactions_list, t_type=None, category=None, date_from=None, date_to=None,
                                       search_text=None):

        if date_from and date_to:
            dt_from = datetime.strptime(date_from, "%Y-%m-%d")
            dt_to = datetime.strptime(date_to, "%Y-%m-%d")
            if dt_from > dt_to:
                raise ValueError("Начало диапазона дат позже окончания")

        filtered_items = []

        for t in transactions_list:
            if t_type and t.get("type") != t_type:
                continue

            if category and t.get("category") != category:
                continue

            if date_from and t.get("date") < date_from:
                continue

            if date_to and t.get("date") > date_to:
                continue

            if search_text:
                if search_text.lower() not in t.get("description", "").lower():
                    continue

            filtered_items.append(t)

        return sorted(filtered_items, key=lambda x: (x.get("date"), x.get("id")))


import unittest


class TestModule(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"id": "1", "date": "2026-11-09", "type": "доход", "category": "Зарплата", "amount": 1000.0,
             "description": "Перевод"},
            {"id": "2", "date": "2026-11-10", "type": "расход", "category": "Еда", "amount": 200.0,
             "description": "Обед"},
            {"id": "3", "date": "2026-11-12", "type": "расход", "category": "Еда", "amount": 150.0,
             "description": "Ресторан"},
            {"id": "4", "date": "2026-11-10", "type": "расход", "category": "Транспорт", "amount": 50.0,
             "description": "Поездка на метро"},
        ]

    def test_combined_filters_and_search(self):
        result = FilterModule.filter_and_search_transactions(
            self.test_data,
            t_type="расход",
            category="Еда",
            date_from="2026-11-10",
            date_to="2026-11-11",
            search_text="БУРГЕР"
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "2")


if __name__ == "__main__":
    unittest.main()
