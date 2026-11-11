import pandas as pd

def total_by_category(df: pd.DataFrame) -> pd.Series:
    """Сумма по каждой категории (всё вместе)."""
    return df.groupby("category")["amount"].sum()

def income_by_category(df: pd.DataFrame) -> pd.Series:
    """Доходы по категориям."""
    return df[df["type"] == "доход"].groupby("category")["amount"].sum()

def expense_by_category(df: pd.DataFrame) -> pd.Series:
    """Расходы по категориям."""
    return df[df["type"] == "расход"].groupby("category")["amount"].sum()

def balance_by_category(df: pd.DataFrame) -> pd.Series:
    """Баланс по категориям: доходы минус расходы."""
    income = income_by_category(df)
    expense = expense_by_category(df)
    all_cats = sorted(set(income.index) | set(expense.index))
    income = income.reindex(all_cats, fill_value=0)
    expense = expense.reindex(all_cats, fill_value=0)
    return (income - expense).sort_index()