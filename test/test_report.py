import os
import pandas as pd
import pytest

from total_amounts import total_by_type, balance
from grouping import (
    total_by_category,
    income_by_category,
    expense_by_category,
    balance_by_category,
)

# Путь к CSV — рядом с тестами
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions_sample.csv")

# ── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def sample_df():
    return pd.read_csv(CSV_PATH, encoding="utf-8")

@pytest.fixture
def income_only_df():
    return pd.DataFrame({
        "id": [1, 4, 5],
        "date": ["2026-11-09","2026-11-07","2026-11-06"],
        "type": ["доход","доход","доход"],
        "category": ["Зарплата","Подработка","Подработка"],
        "amount": [50000.0, 5000.0, 5000.0],
        "description": ["Зарплата","Подработка","Подработка"],
    })

@pytest.fixture
def expense_only_df():
    return pd.DataFrame({
        "id": [2, 3, 6],
        "date": ["2026-11-09","2026-11-08","2026-11-06"],
        "type": ["расход","расход","расход"],
        "category": ["Еда","Транспорт","Транспорт"],
        "amount": [1500.0, 120.0, 120.0],
        "description": ["Продукты","Проезд","Проезд"],
    })

@pytest.fixture
def empty_df():
    return pd.DataFrame(columns=["id","date","type","category","amount","description"])


# ── total_by_type ─────────────────────────────────────────

def test_total_by_type_sample(sample_df):
    expected = pd.Series({"доход": 60000.0, "расход": 1740.0})
    pd.testing.assert_series_equal(total_by_type(sample_df), expected, check_names=False)

def test_total_by_type_income_only(income_only_df):
    expected = pd.Series({"доход": 60000.0, "расход": 0.0})
    pd.testing.assert_series_equal(total_by_type(income_only_df), expected, check_names=False)

def test_total_by_type_expense_only(expense_only_df):
    expected = pd.Series({"доход": 0.0, "расход": 1740.0})
    pd.testing.assert_series_equal(total_by_type(expense_only_df), expected, check_names=False)

def test_total_by_type_empty(empty_df):
    expected = pd.Series({"доход": 0.0, "расход": 0.0})
    pd.testing.assert_series_equal(total_by_type(empty_df), expected, check_names=False)


# ── balance ───────────────────────────────────────────────

def test_balance_sample(sample_df):
    assert balance(sample_df) == pytest.approx(58260.0)

def test_balance_income_only(income_only_df):
    assert balance(income_only_df) == pytest.approx(60000.0)

def test_balance_expense_only(expense_only_df):
    assert balance(expense_only_df) == pytest.approx(-1740.0)

def test_balance_empty(empty_df):
    assert balance(empty_df) == pytest.approx(0.0)


# ── total_by_category ─────────────────────────────────────

def test_total_by_category_sample(sample_df):
    expected = pd.Series({"Зарплата": 50000.0, "Подработка": 10000.0,
                          "Еда": 1500.0, "Транспорт": 240.0})
    pd.testing.assert_series_equal(
        total_by_category(sample_df).sort_index(), expected.sort_index(), check_names=False)


# ── income_by_category ────────────────────────────────────

def test_income_by_category_sample(sample_df):
    expected = pd.Series({"Зарплата": 50000.0, "Подработка": 10000.0})
    pd.testing.assert_series_equal(
        income_by_category(sample_df).sort_index(), expected.sort_index(), check_names=False)

def test_income_by_category_no_income(expense_only_df):
    assert income_by_category(expense_only_df).empty


# ── expense_by_category ───────────────────────────────────

def test_expense_by_category_sample(sample_df):
    expected = pd.Series({"Еда": 1500.0, "Транспорт": 240.0})
    pd.testing.assert_series_equal(
        expense_by_category(sample_df).sort_index(), expected.sort_index(), check_names=False)

def test_expense_by_category_no_expense(income_only_df):
    assert expense_by_category(income_only_df).empty


# ── balance_by_category ───────────────────────────────────

def test_balance_by_category_sample(sample_df):
    expected = pd.Series({"Зарплата": 50000.0, "Подработка": 10000.0,
                          "Еда": -1500.0, "Транспорт": -240.0})
    pd.testing.assert_series_equal(
        balance_by_category(sample_df), expected.sort_index(), check_names=False)

def test_balance_by_category_income_only(income_only_df):
    expected = pd.Series({"Зарплата": 50000.0, "Подработка": 10000.0})
    pd.testing.assert_series_equal(
        balance_by_category(income_only_df), expected.sort_index(), check_names=False)

def test_balance_by_category_expense_only(expense_only_df):
    expected = pd.Series({"Еда": -1500.0, "Транспорт": -240.0})
    pd.testing.assert_series_equal(
        balance_by_category(expense_only_df), expected.sort_index(), check_names=False)

def test_balance_by_category_empty(empty_df):
    assert balance_by_category(empty_df).empty