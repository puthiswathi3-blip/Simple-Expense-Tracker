
import json
import os
from datetime import datetime
from collections import defaultdict

FILE_NAME = "expenses.json"


# Load expenses from the JSON file
def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read expense file.")
        return []


# Save expenses to the JSON file
def save_expenses(expenses):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(expenses, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save expenses.")
        return False


# Get and validate the expense date
def get_expense_date():
    while True:
        date = input("Enter expense date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format.")


# Add a new expense
def add_expense(expenses):
    print("\n--- Add New Expense ---")

    date = get_expense_date()

    category = input("Enter category (Food, Travel, etc.): ").strip()
    while not category:
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    description = input("Enter description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Enter description: ").strip()

    while True:
        try:
            amount = float(input("Enter amount: ₹"))
            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                break
        except ValueError:
            print("Please enter a valid numeric amount.")

    expense = {
        "date": date,
        "category": category.title(),
        "description": description,
        "amount": round(amount, 2)
    }

    expenses.append(expense)

    if save_expenses(expenses):
        print("Expense added successfully!")
    else:
        expenses.pop()


# Display all expenses
def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("-" * 75)
    print(f"{'Date':<13}{'Category':<15}{'Description':<25}{'Amount (₹)':>12}")
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense['date']:<13}"
            f"{expense['category']:<15}"
            f"{expense['description'][:24]:<25}"
            f"{expense['amount']:>12.2f}"
        )

    print("-" * 75)


# Generate category-wise spending summary
def category_summary(expenses):
    print("\n--- Category-wise Spending Summary ---")

    if not expenses:
        print("No expenses available.")
        return

    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["category"]] += expense["amount"]

    for category, total in sorted(totals.items()):
        print(f"{category:<20} ₹{total:.2f}")


# Generate total spending report
def total_report(expenses):
    print("\n--- Total Spending Report ---")

    total = sum(expense["amount"] for expense in expenses)

    print(f"Number of expenses: {len(expenses)}")
    print(f"Total spending: ₹{total:.2f}")

    if expenses:
        average = total / len(expenses)
        print(f"Average expense: ₹{average:.2f}")
    else:
        print("Average expense: ₹0.00")


# Main menu
def main():
    expenses = load_expenses()

    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category-wise Summary")
        print("4. Total Spending Report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            category_summary(expenses)
        elif choice == "4":
            total_report(expenses)
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice! Please select 1 to 5.")


if __name__ == "__main__":
    main()
