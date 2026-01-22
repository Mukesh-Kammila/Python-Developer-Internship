"""
Personal Expense Tracker - Main Application
This is the entry point for the expense tracking application.
"""

from expense_manager import ExpenseManager
from utils import validate_amount, validate_date, clear_screen
import sys


def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("     PERSONAL EXPENSE TRACKER")
    print("="*50)
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. View Expenses by Date")
    print("5. Generate Monthly Report")
    print("6. Delete Expense")
    print("7. Exit")
    print("="*50)


def add_expense(manager):
    """Handle adding a new expense"""
    print("\n--- Add New Expense ---")
    
    try:
        date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date:
            from datetime import date as dt
            date = str(dt.today())
        elif not validate_date(date):
            print("Invalid date format!")
            return
        
        category = input("Enter category (Food/Transport/Entertainment/Bills/Other): ").strip()
        if not category:
            category = "Other"
        
        description = input("Enter description: ").strip()
        if not description:
            print("Description cannot be empty!")
            return
        
        amount_str = input("Enter amount: ").strip()
        amount = validate_amount(amount_str)
        if amount is None:
            print("Invalid amount!")
            return
        
        if manager.add_expense(date, category, description, amount):
            print(f"\n✓ Expense added successfully! (${amount:.2f})")
        else:
            print("\n✗ Failed to add expense!")
            
    except Exception as e:
        print(f"Error: {str(e)}")


def view_all_expenses(manager):
    """Display all expenses"""
    print("\n--- All Expenses ---")
    expenses = manager.get_all_expenses()
    
    if not expenses:
        print("No expenses found!")
        return
    
    print(f"\n{'Date':<12} {'Category':<15} {'Description':<25} {'Amount':>10}")
    print("-" * 65)
    
    total = 0
    for exp in expenses:
        print(f"{exp['date']:<12} {exp['category']:<15} {exp['description']:<25} ${exp['amount']:>9.2f}")
        total += exp['amount']
    
    print("-" * 65)
    print(f"{'Total:':<52} ${total:>9.2f}")


def view_by_category(manager):
    """View expenses filtered by category"""
    print("\n--- View by Category ---")
    category = input("Enter category: ").strip()
    
    expenses = manager.get_expenses_by_category(category)
    
    if not expenses:
        print(f"No expenses found for category: {category}")
        return
    
    print(f"\nExpenses in '{category}':")
    print(f"{'Date':<12} {'Description':<30} {'Amount':>10}")
    print("-" * 55)
    
    total = 0
    for exp in expenses:
        print(f"{exp['date']:<12} {exp['description']:<30} ${exp['amount']:>9.2f}")
        total += exp['amount']
    
    print("-" * 55)
    print(f"{'Total:':<42} ${total:>9.2f}")


def main():
    """Main application loop"""
    manager = ExpenseManager()
    
    print("\nWelcome to Personal Expense Tracker!")
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            add_expense(manager)
        
        elif choice == '2':
            view_all_expenses(manager)
        
        elif choice == '3':
            view_by_category(manager)
        
        elif choice == '4':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            expenses = manager.get_expenses_by_date(date)
            if expenses:
                total = sum(exp['amount'] for exp in expenses)
                print(f"\nTotal expenses on {date}: ${total:.2f}")
                for exp in expenses:
                    print(f"  - {exp['category']}: {exp['description']} (${exp['amount']:.2f})")
            else:
                print(f"No expenses found for {date}")
        
        elif choice == '5':
            month = input("Enter month (YYYY-MM): ").strip()
            report = manager.generate_monthly_report(month)
            if report:
                print(f"\n--- Monthly Report for {month} ---")
                print(f"Total Expenses: ${report['total']:.2f}")
                print("\nBy Category:")
                for cat, amt in report['by_category'].items():
                    print(f"  {cat}: ${amt:.2f}")
            else:
                print("No data available for this month")
        
        elif choice == '6':
            view_all_expenses(manager)
            idx = input("\nEnter expense number to delete (or 'c' to cancel): ").strip()
            if idx.lower() != 'c' and idx.isdigit():
                if manager.delete_expense(int(idx) - 1):
                    print("✓ Expense deleted successfully!")
                else:
                    print("✗ Invalid expense number!")
        
        elif choice == '7':
            print("\nThank you for using Personal Expense Tracker!")
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()