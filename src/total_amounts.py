import pandas as pd

def total_by_type(df: pd.DataFrame) -> pd.Series:
    """Сколько всего доходов и расходов."""
    return df.groupby("type")["amount"].sum()