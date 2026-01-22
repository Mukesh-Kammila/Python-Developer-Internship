"""
Expense Manager Module
Handles all expense-related operations including storage and retrieval.
"""

import csv
import os
from datetime import datetime


class ExpenseManager:
    """Manages expense tracking operations"""
    
    def __init__(self, filename='expenses.csv'):
        """Initialize the expense manager"""
        self.filename = filename
        self.expenses = []
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from CSV file"""
        if not os.path.exists(self.filename):
            # Create file with headers if it doesn't exist
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Description', 'Amount'])
            return
        
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                self.expenses = []
                for row in reader:
                    row['Amount'] = float(row['Amount'])
                    self.expenses.append(row)
        except Exception as e:
            print(f"Error loading expenses: {e}")
            self.expenses = []
    
    def save_expenses(self):
        """Save expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Date', 'Category', 'Description', 'Amount'])
                writer.writeheader()
                writer.writerows(self.expenses)
            return True
        except Exception as e:
            print(f"Error saving expenses: {e}")
            return False
    
    def add_expense(self, date, category, description, amount):
        """Add a new expense"""
        expense = {
            'Date': date,
            'Category': category.capitalize(),
            'Description': description,
            'Amount': float(amount)
        }
        self.expenses.append(expense)
        return self.save_expenses()
    
    def get_all_expenses(self):
        """Return all expenses"""
        return [
            {
                'date': exp['Date'],
                'category': exp['Category'],
                'description': exp['Description'],
                'amount': exp['Amount']
            }
            for exp in self.expenses
        ]
    
    def get_expenses_by_category(self, category):
        """Get expenses filtered by category"""
        category = category.capitalize()
        return [
            {
                'date': exp['Date'],
                'description': exp['Description'],
                'amount': exp['Amount']
            }
            for exp in self.expenses
            if exp['Category'].lower() == category.lower()
        ]
    
    def get_expenses_by_date(self, date):
        """Get expenses for a specific date"""
        return [
            {
                'category': exp['Category'],
                'description': exp['Description'],
                'amount': exp['Amount']
            }
            for exp in self.expenses
            if exp['Date'] == date
        ]
    
    def generate_monthly_report(self, month):
        """Generate a report for a specific month (YYYY-MM format)"""
        monthly_expenses = [
            exp for exp in self.expenses
            if exp['Date'].startswith(month)
        ]
        
        if not monthly_expenses:
            return None
        
        total = sum(exp['Amount'] for exp in monthly_expenses)
        
        # Group by category
        by_category = {}
        for exp in monthly_expenses:
            cat = exp['Category']
            by_category[cat] = by_category.get(cat, 0) + exp['Amount']
        
        return {
            'total': total,
            'by_category': by_category,
            'count': len(monthly_expenses)
        }
    
    def delete_expense(self, index):
        """Delete an expense by index"""
        try:
            if 0 <= index < len(self.expenses):
                self.expenses.pop(index)
                return self.save_expenses()
            return False
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False
    
    def get_total_expenses(self):
        """Calculate total of all expenses"""
        return sum(exp['Amount'] for exp in self.expenses)
    
    def get_category_summary(self):
        """Get summary of expenses by category"""
        summary = {}
        for exp in self.expenses:
            cat = exp['Category']
            summary[cat] = summary.get(cat, 0) + exp['Amount']
        return summary