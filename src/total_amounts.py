from decimal import Decimal
import pandas as pd

ALL_TYPES = ["доход", "расход"]
ZERO = Decimal("0")

def total_by_type(df: pd.DataFrame) -> pd.Series:
    """Сколько всего доходов и расходов. Оба типа всегда присутствуют."""
    if df.empty:
        return pd.Series({"доход": ZERO, "расход": ZERO}, dtype=object)
    result = df.groupby("type")["amount"].sum()
    return result.reindex(ALL_TYPES, fill_value=ZERO)

def balance(df: pd.DataFrame) -> Decimal:
    """Баланс: доходы минус расходы."""
    totals = total_by_type(df)
    return totals["доход"] - totals["расход"]