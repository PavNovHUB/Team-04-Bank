def filter_by_type(transactions: list, operation_type: str) -> list:
    target_type = operation_type.strip().lower()
    return [a for a in transactions if a.get('type', '').strip().lower() == target_type]

def filter_by_category(transactions: list, category: str) -> list:
    target_category = category.strip().lower()
    return [a for a in transactions if target_category in a.get('category', '').strip().lower()]
