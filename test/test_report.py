import os
from decimal import Decimal
import pandas as pd
import pytest

from total_amounts import total_by_type, balance
from grouping import (
    total_by_category,
    income_by_category,
    expense_by_category,
    balance_by_category,
    category_summary,
)
from data import load_data

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions_sample.csv")


# ── Fixtures (теперь с Decimal) ───────────────────────────

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5, 6],
        "date": ["2026-11-09","2026-11-09","2026-11-08",
                  "2026-11-07","2026-11-06","2026-11-06"],
        "type": ["доход","расход","расход","доход","доход","расход"],
        "category": ["Зарплата","Еда","Транспорт","Подработка","Подработка","Транспорт"],
        "amount": [Decimal("50000.00"), Decimal("1500.00"), Decimal("120.00"),
                   Decimal("5000.00"), Decimal("5000.00"), Decimal("120.00")],
        "description": ["Зарплата","Продукты","Проезд","Подработка","Подработка","Проезд"],
    })

@pytest.fixture
def income_only_df():
    return pd.DataFrame({
        "id": [1, 4, 5],
        "date": ["2026-11-09","2026-11-07","2026-11-06"],
        "type": ["доход","доход","доход"],
        "category": ["Зарплата","Подработка","Подработка"],
        "amount": [Decimal("50000.00"), Decimal("5000.00"), Decimal("5000.00")],
        "description": ["Зарплата","Подработка","Подработка"],
    })

@pytest.fixture
def expense_only_df():
    return pd.DataFrame({
        "id": [2, 3, 6],
        "date": ["2026-11-09","2026-11-08","2026-11-06"],
        "type": ["расход","расход","расход"],
        "category": ["Еда","Транспорт","Транспорт"],
        "amount": [Decimal("1500.00"), Decimal("120.00"), Decimal("120.00")],
        "description": ["Продукты","Проезд","Проезд"],
    })

@pytest.fixture
def empty_df():
    return pd.DataFrame(columns=["id","date","type","category","amount","description"])


# ── Точность Decimal (регресс на float-артефакт) ──────────

def test_decimal_precision():
    """0.30 - 0.10 - 0.20 == 0.00 ровно, без float-погрешности."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "date": ["2026-11-01"] * 3,
        "type": ["доход", "расход", "расход"],
        "category": ["Тест", "Тест", "Тест"],
        "amount": [Decimal("0.30"), Decimal("0.10"), Decimal("0.20")],
        "description": [""] * 3,
    })
    assert balance(df) == Decimal("0.00")
    bal_cat = balance_by_category(df)
    assert bal_cat["Тест"] == Decimal("0.00")


# ── total_by_type ─────────────────────────────────────────

def test_total_by_type_sample(sample_df):
    expected = pd.Series({"доход": Decimal("60000.00"), "расход": Decimal("1740.00")}, dtype=object)
    pd.testing.assert_series_equal(total_by_type(sample_df), expected, check_names=False)

def test_total_by_type_income_only(income_only_df):
    expected = pd.Series({"доход": Decimal("60000.00"), "расход": Decimal("0")}, dtype=object)
    pd.testing.assert_series_equal(total_by_type(income_only_df), expected, check_names=False)

def test_total_by_type_expense_only(expense_only_df):
    expected = pd.Series({"доход": Decimal("0"), "расход": Decimal("1740.00")}, dtype=object)
    pd.testing.assert_series_equal(total_by_type(expense_only_df), expected, check_names=False)

def test_total_by_type_empty(empty_df):
    expected = pd.Series({"доход": Decimal("0"), "расход": Decimal("0")}, dtype=object)
    pd.testing.assert_series_equal(total_by_type(empty_df), expected, check_names=False)


# ── balance ───────────────────────────────────────────────

def test_balance_sample(sample_df):
    assert balance(sample_df) == Decimal("58260.00")

def test_balance_income_only(income_only_df):
    assert balance(income_only_df) == Decimal("60000.00")

def test_balance_expense_only(expense_only_df):
    assert balance(expense_only_df) == Decimal("-1740.00")

def test_balance_empty(empty_df):
    assert balance(empty_df) == Decimal("0")


# ── category_summary (4 показателя) ───────────────────────

def test_category_summary_sample(sample_df):
    result = category_summary(sample_df)
    assert result.loc["Зарплата", "count"] == 1
    assert result.loc["Зарплата", "income"] == Decimal("50000.00")
    assert result.loc["Зарплата", "expense"] == Decimal("0")
    assert result.loc["Зарплата", "balance"] == Decimal("50000.00")

    assert result.loc["Подработка", "count"] == 2
    assert result.loc["Подработка", "income"] == Decimal("10000.00")
    assert result.loc["Подработка", "balance"] == Decimal("10000.00")

    assert result.loc["Еда", "count"] == 1
    assert result.loc["Еда", "income"] == Decimal("0")
    assert result.loc["Еда", "expense"] == Decimal("1500.00")
    assert result.loc["Еда", "balance"] == Decimal("-1500.00")

    assert result.loc["Транспорт", "count"] == 2
    assert result.loc["Транспорт", "expense"] == Decimal("240.00")
    assert result.loc["Транспорт", "balance"] == Decimal("-240.00")

def test_category_summary_empty(empty_df):
    result = category_summary(empty_df)
    assert result.empty
    assert list(result.columns) == ["count", "income", "expense", "balance"]


# ── CSV → Decimal (согласованный формат) ──────────────────

def test_load_data_returns_decimal():
    """load_data приводит amount к Decimal, даже если в CSV строки."""
    df = load_data(CSV_PATH)
    assert df["amount"].apply(type).eq(Decimal).all()
    assert df["amount"].iloc[0] == Decimal("50000.00")


def test_load_data_string_amounts():
    """Строки из CSV корректно конвертируются в Decimal."""
    import tempfile, os
    csv_content = "id,date,type,category,amount,description\n1,2026-01-01,доход,Тест,0.30,ok\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        tmp_path = f.name
    try:
        df = load_data(tmp_path)
        assert df["amount"].iloc[0] == Decimal("0.30")
    finally:
        os.unlink(tmp_path)


# ── income_by_category ───────────────────────

def test_income_by_category_no_income(expense_only_df):
    assert income_by_category(expense_only_df).empty

# ── expense_by_category ──────────────────────

def test_expense_by_category_no_expense(income_only_df):
    assert expense_by_category(income_only_df).empty

# ── balance_by_category ──────────────────────

def test_balance_by_category_income_only(income_only_df):
    expected = pd.Series({"Зарплата": Decimal("50000.00"), "Подработка": Decimal("10000.00")}, dtype=object)
    pd.testing.assert_series_equal(
        balance_by_category(income_only_df), expected.sort_index(), check_names=False)

def test_balance_by_category_expense_only(expense_only_df):
    expected = pd.Series({"Еда": Decimal("-1500.00"), "Транспорт": Decimal("-240.00")}, dtype=object)
    pd.testing.assert_series_equal(
        balance_by_category(expense_only_df), expected.sort_index(), check_names=False)

def test_balance_by_category_empty(empty_df):
    assert balance_by_category(empty_df).empty