"""
Reporting and analysis functions for SpendSense.

Handles totals, monthly filtering, category breakdowns,
insights, and CSV report exports.
"""


from datetime import datetime
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"


def parse_date(date_str: str) -> datetime:
    """Convert a DD/MM/YYYY date string into a datetime object."""
    return datetime.strptime(date_str, "%d/%m/%Y")


def filter_transactions_by_month(transactions, year: int, month: int):
    """Return only transactions from the specified month and year."""

    filtered = []
    for t in transactions:
        dt = parse_date(t["date"])
        if dt.year == year and dt.month == month:
            filtered.append(t)
    return filtered


def calculate_totals(transactions):
    """Calculate total income, expenses, and balance."""

    total_income = 0.0
    total_expense = 0.0

    for transaction in transactions:
        amount = float(transaction["amount"])

        if transaction["type"] == "income":
            total_income += amount
        elif transaction["type"] == "expense":
            total_expense += amount

    balance = total_income - total_expense
    return total_income, total_expense, balance


def category_breakdown_expenses(transactions):
    """Group expense totals by category."""
    breakdown = {}

    for t in transactions:
        if t["type"] != "expense":
            continue

        category = (t["category"] or "uncategorised").strip().lower()
        amount = float(t["amount"])

        breakdown[category] = breakdown.get(category, 0.0) + amount

    return breakdown


def top_categories(breakdown: dict, top_n: int = 3):
    """Return the top spending categories."""
    return sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:top_n]


def export_monthly_report_csv(transactions, year: int, month: int):
    """Export monthly transactions to a CSV report file."""
    REPORTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spendsense_report_{year}-{month:02d}_{timestamp}.csv"
    path = REPORTS_DIR / filename

    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "amount", "type", "category", "note"])

        for t in transactions:
            writer.writerow([t["date"], t["amount"], t["type"], t["category"], t["note"]])

    return path

def average_daily_spend(transactions):
    """Calculate the average daily expense amount"""
    days = set()
    total = 0.0

    for t in transactions:
        if t["type"] != "expense":
            continue

        total += float(t["amount"])
        days.add(t["date"])

    if not days:
        return 0.0

    return round(total / len(days), 2)


def largest_single_expense(transactions):
    """Find the largest single expense transaction."""
    expenses = [
        (t["category"], float(t["amount"]), t["date"])
        for t in transactions
        if t["type"] == "expense"
    ]

    if not expenses:
        return None

    return max(expenses, key=lambda x: x[1])


def expense_percentage_by_category(breakdown: dict):
    """Calculate percentage spend per category."""
    total = sum(breakdown.values())
    if total == 0:
        return {}

    percentages = {}
    for cat, amt in breakdown.items():
        percentages[cat] = round((amt / total) * 100, 1)

    return percentages

