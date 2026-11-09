def filter_transactions(transactions, transaction_type=None, category=None):
    result = []

    for transaction in transactions:

        if transaction_type and transaction["type"] != transaction_type:
            continue

        if category and transaction["category"].lower() != category.lower():
            continue

        result.append(transaction)

    return result