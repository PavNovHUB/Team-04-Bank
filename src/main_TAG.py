'''Первый импорт это заглушка-пример для проверки функции, он будет заменен и код из этого файла будет переписан, когда его сделает другой разработчик'''
from data import load_data
from total_amounts import total_by_type
from grouping import total_by_category, income_by_category, expense_by_category

path = input("Введите путь к CSV-файлу: ") # Нужно вводить полный путь к файлу. Пример: "C:\Users\Ivan\Documents\data.csv"
df = load_data(path)

print(total_by_type(df))
print(total_by_category(df))
print(income_by_category(df))
print(expense_by_category(df))