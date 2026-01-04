"""
Main CLI entry point for SpendSense.

Provides a menu-driven interface for tracking
and analysing transactions.
"""

from datetime import datetime

from transactions import add_transaction, load_transactions, show_latest
from reports import (
    calculate_totals,
    filter_transactions_by_month,
    category_breakdown_expenses,
    top_categories,
    export_monthly_report_csv,
    average_daily_spend,
    largest_single_expense,
    expense_percentage_by_category,
)


def show_menu():
    """Display the main menu options."""
    print("\nSpendSense Menu")
    print("1. Add transaction")
    print("2. View latest transactions")
    print("3. Show totals (all time)")
    print("4. Monthly report")
    print("5. Exit")


def get_month_year_from_user():
    """Get month and year input from the user with defaults."""
    today = datetime.today()
    year_input = input(f"Enter year (YYYY) or leave blank for {today.year}: ").strip()
    month_input = input(f"Enter month (1-12) or leave blank for {today.month}: ").strip()

    year = today.year if year_input == "" else int(year_input)
    month = today.month if month_input == "" else int(month_input)

    return year, month


def main():
    """Run the main application loop."""
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_transaction()

        elif choice == "2":
            transactions = load_transactions()
            show_latest(transactions)

        elif choice == "3":
            transactions = load_transactions()
            income, expense, balance = calculate_totals(transactions)

            print("\nTotals (all time):")
            print(f"Total income: £{income}")
            print(f"Total expenses: £{expense}")
            print(f"Balance: £{balance}")

        elif choice == "4":
            transactions = load_transactions()
            year, month = get_month_year_from_user()

            monthly = filter_transactions_by_month(transactions, year, month)
            income, expense, balance = calculate_totals(monthly)

            print(f"\nMonthly report for {year}-{month:02d}")
            print(f"Income: £{income}")
            print(f"Expenses: £{expense}")
            print(f"Balance: £{balance}")

            breakdown = category_breakdown_expenses(monthly)
            if not breakdown:
                print("\nNo expense categories to show for this month.")
            else:
                print("\nCategory breakdown (expenses):")
                for cat, amt in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
                    print(f"- {cat}: £{amt}")

                top3 = top_categories(breakdown, top_n=3)
                print("\nTop 3 categories:")
                for cat, amt in top3:
                    print(f"- {cat}: £{amt}")
            print("\nInsights:")

            avg_spend = average_daily_spend(monthly)
            print(f"- Average daily spend: £{avg_spend}")

            largest = largest_single_expense(monthly)
            if largest:
                cat, amt, dt = largest
                print(f"- Largest single expense: £{amt} on {dt} ({cat})")

            percentages = expense_percentage_by_category(breakdown)
            if percentages:
                biggest_cat = max(percentages, key=percentages.get)
                print(
                    f"- Highest spend category share: "
                    f"{biggest_cat} ({percentages[biggest_cat]}%)"
                )

            print("\nInsights:")

            avg_spend = average_daily_spend(monthly)
            print(f"- Average daily spend: £{avg_spend}")

            largest = largest_single_expense(monthly)
            if largest:
                cat, amt, dt = largest
                print(f"- Largest single expense: £{amt} on {dt} ({cat})")

            percentages = expense_percentage_by_category(breakdown)
            if percentages:
                biggest_cat = max(percentages, key=percentages.get)
                print(
                    f"- Highest spend category share: "
                    f"{biggest_cat} ({percentages[biggest_cat]}%)"
                )

            report_path = export_monthly_report_csv(monthly, year, month)
            print(f"\nReport exported to: {report_path}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    main()
