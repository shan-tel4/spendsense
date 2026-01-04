"""
Transaction handling for SpendSense.

Collects user input, saves transactions to CSV,
and loads existing transactions for display.
"""

import csv
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "transactions.csv"


def add_transaction():
    """Prompt the user for a transaction and save it to the CSV file."""
    transaction_date = input("Enter date (DD/MM/YYYY) or leave blank for today: ").strip()
    if transaction_date == "":
        transaction_date = date.today().strftime("%d/%m/%Y")

    amount_input = input("Enter amount: ").strip()
    try:
        amount = float(amount_input)
    except ValueError:
        print("Amount must be a number.")
        return

    transaction_type = input("Enter type (income/expense): ").strip().lower()
    if transaction_type not in ["income", "expense"]:
        print("Type must be income or expense.")
        return

    category = input("Enter category: ").strip()
    note = input("Enter note (optional): ").strip()

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([transaction_date, amount, transaction_type, category, note])

    print("Transaction saved.")


def load_transactions():
    """Load all transactions from the CSV file."""

    transactions = []

    with open(CSV_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)

    return transactions


def show_latest(transactions, limit=5):
    """Display the most recent transactions in the terminal."""
    if not transactions:
        print("No transactions found.")
        return

    print("\nLatest transactions:")
    for transaction in transactions[-limit:]:
        print(
            f"{transaction['date']} | "
            f"{transaction['type']} | "
            f"£{transaction['amount']} | "
            f"{transaction['category']} | "
            f"{transaction['note']}"
        )


