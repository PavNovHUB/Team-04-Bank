from decimal import Decimal
import pandas as pd

ZERO = Decimal("0")

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
    income = income.reindex(all_cats, fill_value=ZERO)
    expense = expense.reindex(all_cats, fill_value=ZERO)
    return (income - expense).sort_index()

def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Четыре показателя по каждой категории: count, income, expense, balance."""
    if df.empty:
        return pd.DataFrame(columns=["count", "income", "expense", "balance"])

    count = df.groupby("category").size().astype(int)
    income = income_by_category(df)
    expense = expense_by_category(df)

    all_cats = sorted(set(count.index))
    income = income.reindex(all_cats, fill_value=ZERO)
    expense = expense.reindex(all_cats, fill_value=ZERO)
    bal = income - expense

    return pd.DataFrame({
        "count": count,
        "income": income,
        "expense": expense,
        "balance": bal,
    }, index=all_cats)   