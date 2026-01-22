# Python Internship Projects - Complete Code

This document contains all the code for the three projects mentioned in the internship report.

## Mini Project 1: Personal Expense Tracker

A command-line application to track personal expenses with categorization and reporting features.

### Files Structure:
```
expense_tracker/
├── main.py              # Main application entry point
├── expense_manager.py   # Core business logic
└── utils.py            # Utility functions
```

### Installation & Running:
```bash
# No external dependencies required (uses Python standard library)
python main.py
```

### Features:
- Add expenses with date, category, description, and amount
- View all expenses
- Filter by category or date
- Generate monthly reports
- Delete expenses
- Data stored in CSV format

---

## Mini Project 2: Weather Information Dashboard

A console application that fetches and displays weather information using the OpenWeatherMap API.

### Files Structure:
```
weather_dashboard/
├── main.py              # Main application
├── weather_api.py       # API interaction module
└── data_storage.py     # Local data storage
```

### Installation:
```bash
pip install requests
```

### Setup:
1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace `'your_api_key_here'` in `main.py` with your actual API key

### Running:
```bash
python main.py
```

### Features:
- Get current weather for any city
- View 5-day forecast
- Save favorite locations
- Cached API responses (10-minute cache)
- Export favorites to text file

---

## Major Project: Inventory Management System

A complete web-based inventory management system built with Flask.

### Files Structure:
```
inventory_system/
├── app.py                      # Main Flask application
├── templates/
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── dashboard.html         # Dashboard
│   ├── items.html             # Items listing
│   ├── add_item.html          # Add item form
│   ├── item_detail.html       # Item details
│   ├── add_transaction.html   # Add transaction
│   └── reports.html           # Reports page
└── inventory.db               # SQLite database (created automatically)
```

### Installation:
```bash
pip install flask flask-sqlalchemy
```

### Running:
```bash
python app.py
```


### Default Login:
- Username: `admin`
- Password: `admin123`

### Features:
- User authentication with role-based access (Admin, Manager, Viewer)
- Complete CRUD operations for items, categories, and locations
- Transaction tracking (check-out, return, transfer, adjust)
- Low stock alerts
- Advanced filtering and search
- Reports generation
  - Inventory by location
  - Low stock items
  - Transaction history
- Responsive web interface using Bootstrap 5
- SQLite database for data persistence

### Database Schema:

**Users Table:**
- id, username, password (hashed), role, created_at

**Categories Table:**
- id, name, description

**Locations Table:**
- id, name, address

**Items Table:**
- id, name, description, category_id, location_id, quantity, min_quantity, price, serial_number, purchase_date, created_at

**Transactions Table:**
- id, item_id, user_id, transaction_type, quantity, notes, created_at

---

## Additional Templates Needed for Major Project
