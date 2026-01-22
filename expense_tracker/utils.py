"""
Utility Functions for Expense Tracker
Contains helper functions for validation and formatting.
"""

import os
import re
from datetime import datetime


def validate_date(date_string):
    """
    Validate date string format (YYYY-MM-DD)
    Returns True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_amount(amount_string):
    """
    Validate and convert amount to float
    Returns float value if valid, None otherwise
    """
    try:
        amount = float(amount_string)
        if amount <= 0:
            return None
        return amount
    except (ValueError, TypeError):
        return None


def format_currency(amount):
    """Format amount as currency string"""
    return f"${amount:,.2f}"


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_current_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime('%Y-%m-%d')


def get_current_month():
    """Get current month in YYYY-MM format"""
    return datetime.now().strftime('%Y-%m')


def parse_month(month_string):
    """
    Parse month string and validate format (YYYY-MM)
    Returns True if valid, False otherwise
    """
    pattern = r'^\d{4}-\d{2}$'
    if not re.match(pattern, month_string):
        return False
    
    try:
        year, month = map(int, month_string.split('-'))
        if 1 <= month <= 12:
            return True
        return False
    except:
        return False


def format_date(date_string):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_string


def validate_category(category):
    """
    Validate category name
    Returns True if valid, False otherwise
    """
    valid_categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Other']
    return category.capitalize() in valid_categories


def sanitize_input(input_string):
    """Remove potentially harmful characters from input"""
    # Remove any special characters except basic punctuation
    return re.sub(r'[^\w\s\-.,!?]', '', input_string)


def calculate_percentage(part, total):
    """Calculate percentage of part in total"""
    if total == 0:
        return 0
    return (part / total) * 100


def export_to_text(expenses, filename='expenses_export.txt'):
    """Export expenses to a text file"""
    try:
        with open(filename, 'w') as f:
            f.write("EXPENSE REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            total = 0
            for exp in expenses:
                f.write(f"Date: {exp['date']}\n")
                f.write(f"Category: {exp['category']}\n")
                f.write(f"Description: {exp['description']}\n")
                f.write(f"Amount: ${exp['amount']:.2f}\n")
                f.write("-" * 60 + "\n")
                total += exp['amount']
            
            f.write(f"\nTotal Expenses: ${total:.2f}\n")
        return True
    except Exception as e:
        print(f"Error exporting: {e}")
        return False


def get_date_range(start_date, end_date):
    """Validate date range"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return start <= end
    except:
        return False