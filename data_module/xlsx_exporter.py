from openpyxl import Workbook


def export_to_xlsx(transactions, file_path):
    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Данные"

    headers = [
        "id", "date", "type",
        "category", "amount", "description"
    ]

    sheet.append(headers)

    for transaction in transactions:
        sheet.append([
            transaction["id"],
            transaction["date"],
            transaction["type"],
            transaction["category"],
            float(transaction["amount"]),
            transaction["description"]
        ])

    summary = workbook.create_sheet("Итоги")

    income = 0
    expenses = 0

    categories = {}

    for transaction in transactions:
        amount = float(transaction["amount"])
        category = transaction["category"]

        if transaction["type"] == "доход":
            income += amount
        else:
            expenses += amount

        if category not in categories:
            categories[category] = {
                "count": 0,
                "income": 0,
                "expenses": 0
            }

        categories[category]["count"] += 1

        if transaction["type"] == "доход":
            categories[category]["income"] += amount
        else:
            categories[category]["expenses"] += amount

    summary.append(["Показатель", "Значение"])
    summary.append(["Количество операций", len(transactions)])
    summary.append(["Доходы", income])
    summary.append(["Расходы", expenses])
    summary.append(["Баланс", income - expenses])

    summary.append([])
    summary.append(["Категория", "Количество", "Доходы", "Расходы", "Баланс"])

    for category in sorted(categories):
        data = categories[category]

        summary.append([
            category,
            data["count"],
            data["income"],
            data["expenses"],
            data["income"] - data["expenses"]
        ])

    workbook.save(file_path)