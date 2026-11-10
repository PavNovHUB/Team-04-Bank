from datetime import datetime
from decimal import Decimal, InvalidOperation


def validate_transaction(transaction):
    errors = []

    required_fields = [
        "id", "date", "type",
        "category", "amount", "description"
    ]

    for field in required_fields:
        if not transaction.get(field):
            errors.append(f"Не заполнено поле: {field}")

    if errors:
        return errors

    try:
        datetime.strptime(transaction["date"], "%Y-%m-%d")
    except ValueError:
        errors.append("Неверный формат даты")

    if transaction["type"] not in ["доход", "расход"]:
        errors.append("Тип должен быть доход или расход")

    try:
        amount = Decimal(transaction["amount"])

        if amount <= 0:
            errors.append("Сумма должна быть положительной")

        if amount.as_tuple().exponent < -2:
            errors.append("Допускается не более двух знаков после запятой")

    except (InvalidOperation, ValueError):
        errors.append("Некорректная сумма")

    return errors