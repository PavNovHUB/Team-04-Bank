from decimal import Decimal
import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")
    # Приводим amount к Decimal (работает и со строками, и с числами)
    df["amount"] = df["amount"].apply(lambda x: Decimal(str(x)))
    return df