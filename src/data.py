"""Временный код"""
import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8")