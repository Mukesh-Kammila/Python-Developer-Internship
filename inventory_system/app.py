"""
Inventory Management System - Main Application
Flask-based web application for managing inventory items.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='viewer')  # admin, manager, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    items = db.relationship('Item', backref='category', lazy=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200))
    items = db.relationship('Item', backref='location', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    min_quantity = db.Column(db.Integer, default=5)
    price = db.Column(db.Float, default=0.0)
    serial_number = db.Column(db.String(100), unique=True)
    purchase_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='item', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # check-out, return, transfer, adjust
    quantity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='transactions')

# Create tables
with app.app_context():
    db.create_all()
    
    # Create default admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

# Helper functions
def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Homepage"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    total_items = Item.query.count()
    total_categories = Category.query.count()
    total_locations = Location.query.count()
    
    # Items below minimum quantity
    low_stock_items = Item.query.filter(Item.quantity <= Item.min_quantity).all()
    
    # Recent transactions
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html',
                         total_items=total_items,
                         total_categories=total_categories,
                         total_locations=total_locations,
                         low_stock_items=low_stock_items,
                         recent_transactions=recent_transactions)

@app.route('/items')
@login_required
def items():
    """List all items"""
    search = request.args.get('search', '')
    category_id = request.args.get('category', '')
    location_id = request.args.get('location', '')
    
    query = Item.query
    
    if search:
        query = query.filter(Item.name.contains(search) | Item.description.contains(search))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if location_id:
        query = query.filter_by(location_id=location_id)
    
    items = query.all()
    categories = Category.query.all()
    locations = Location.query.all()
    
    return render_template('items.html', items=items, categories=categories, locations=locations)

@app.route('/item/<int:id>')
@login_required
def item_detail(id):
    """Item details"""
    item = Item.query.get_or_404(id)
    transactions = Transaction.query.filter_by(item_id=id).order_by(Transaction.created_at.desc()).all()
    return render_template('item_detail.html', item=item, transactions=transactions)

@app.route('/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    """Add new item"""
    if request.method == 'POST':
        item = Item(
            name=request.form.get('name'),
            description=request.form.get('description'),
            category_id=request.form.get('category_id'),
            location_id=request.form.get('location_id'),
            quantity=int(request.form.get('quantity', 0)),
            min_quantity=int(request.form.get('min_quantity', 5)),
            price=float(request.form.get('price', 0)),
            serial_number=request.form.get('serial_number'),
            purchase_date=datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d') if request.form.get('purchase_date') else None
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash('Item added successfully!', 'success')
        return redirect(url_for('items'))
    
    categories = Category.query.all()
    locations = Location.query.all()
    return render_template('add_item.html', categories=categories, locations=locations)

@app.route('/item/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    """Edit item"""
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.category_id = request.form.get('category_id')
        item.location_id = request.form.get('location_id')
        item.quantity = int(request.form.get('quantity', 0))
        item.min_quantity = int(request.form.get('min_quantity', 5))
        item.price = float(request.form.get('price', 0))
        item.serial_number = request.form.get('serial_number')
        
        if request.form.get('purchase_date'):
            item.purchase_date = datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d')
        
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('item_detail', id=id))
    
    categories = Category.query.all()
    locations = Location.query.all()
    return render_template('edit_item.html', item=item, categories=categories, locations=locations)

@app.route('/item/delete/<int:id>')
@login_required
def delete_item(id):
    """Delete item"""
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('items'))

@app.route('/transaction/add/<int:item_id>', methods=['GET', 'POST'])
@login_required
def add_transaction(item_id):
    """Add transaction"""
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        transaction_type = request.form.get('transaction_type')
        quantity = int(request.form.get('quantity'))
        notes = request.form.get('notes')
        
        # Update item quantity based on transaction type
        if transaction_type in ['check-out', 'transfer']:
            item.quantity -= quantity
        elif transaction_type in ['return', 'adjust']:
            item.quantity += quantity
        
        transaction = Transaction(
            item_id=item_id,
            user_id=session['user_id'],
            transaction_type=transaction_type,
            quantity=quantity,
            notes=notes
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('Transaction recorded successfully!', 'success')
        return redirect(url_for('item_detail', id=item_id))
    
    return render_template('add_transaction.html', item=item)

@app.route('/categories')
@login_required
def categories():
    """List categories"""
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/category/add', methods=['GET', 'POST'])
@admin_required
def add_category():
    """Add category"""
    if request.method == 'POST':
        category = Category(
            name=request.form.get('name'),
            description=request.form.get('description')
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html')

@app.route('/locations')
@login_required
def locations():
    """List locations"""
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/add', methods=['GET', 'POST'])
@admin_required
def add_location():
    """Add location"""
    if request.method == 'POST':
        location = Location(
            name=request.form.get('name'),
            address=request.form.get('address')
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_location.html')

@app.route('/reports')
@login_required
def reports():
    """Generate reports"""
    # Inventory by location
    locations = Location.query.all()
    inventory_by_location = []
    
    for location in locations:
        total_items = sum(item.quantity for item in location.items)
        total_value = sum(item.quantity * item.price for item in location.items)
        inventory_by_location.append({
            'location': location.name,
            'total_items': total_items,
            'total_value': total_value
        })
    
    # Low stock items
    low_stock = Item.query.filter(Item.quantity <= Item.min_quantity).all()
    
    return render_template('reports.html', 
                         inventory_by_location=inventory_by_location,
                         low_stock=low_stock)

if __name__ == '__main__':
    app.run(debug=True)