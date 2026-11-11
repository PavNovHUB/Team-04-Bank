import pandas as pd

ALL_TYPES = ["доход", "расход"]

def total_by_type(df: pd.DataFrame) -> pd.Series:
    """Сколько всего доходов и расходов. Оба типа всегда присутствуют."""
    result = df.groupby("type")["amount"].sum()
    return result.reindex(ALL_TYPES, fill_value=0).astype(float)

def balance(df: pd.DataFrame) -> float:
    """Баланс: доходы минус расходы."""
    totals = total_by_type(df)
    return totals["доход"] - totals["расход"]