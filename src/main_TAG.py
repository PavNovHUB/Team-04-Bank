from data import load_data
from total_amounts import total_by_type, balance
from grouping import total_by_category, income_by_category, expense_by_category, balance_by_category, category_summary

path = input("Введите путь к CSV-файлу: ")
df = load_data(path)

print("=== Итого по типам ===")
print(total_by_type(df))
print(f"\nБаланс: {balance(df):.2f}")
print("\n=== Итого по категориям ===")
print(total_by_category(df))
print("\n=== Доходы по категориям ===")
print(income_by_category(df))
print("\n=== Расходы по категориям ===")
print(expense_by_category(df))
print("\n=== Баланс по категориям ===")
print(balance_by_category(df))
print("\n=== Таблица ===")
print(category_summary(df))