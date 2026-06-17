from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'makeup-store-secret-key-2024'
DB_PATH = os.path.join(os.path.dirname(__file__), 'store.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database by running init_db.py"""
    import init_db
    init_db.init_db()

def luhn_check(card_number):
    """Validate credit card number using Luhn algorithm."""
    card_number = card_number.replace(' ', '').replace('-', '')
    if not card_number.isdigit():
        return False
    if len(card_number) < 13 or len(card_number) > 19:
        return False
    
    sum_digits = 0
    # Process from right to left
    digits = [int(d) for d in card_number]
    digits.reverse()
    
    for i, digit in enumerate(digits):
        # Double every second digit (starting from index 1 which is the 2nd digit)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_digits += digit
    
    return (sum_digits % 10) == 0

def validate_expiration_date(exp_month, exp_year):
    """Validate that expiration date is not in the past."""
    try:
        month = int(exp_month)
        year = int(exp_year)
        if month < 1 or month > 12:
            return False
        if year < 100:
            year += 2000
        now = datetime.now()
        if year < now.year or (year == now.year and month < now.month):
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_cvv(cvv):
    """Validate CVV is 3 or 4 digits."""
    return cvv.isdigit() and len(cvv) in (3, 4)

@app.route('/')
def index():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('index.html', products=products, cart_count=cart_count)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if product is None:
        return redirect(url_for('index'))
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('product.html', product=product, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(request.referrer or url_for('index'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    for key in list(cart.keys()):
        new_qty = request.form.get(f'qty_{key}')
        if new_qty and new_qty.isdigit():
            qty = int(new_qty)
            if qty > 0:
                cart[key] = qty
            else:
                del cart[key]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    conn = get_db()
    for prod_id, qty in cart.items():
        product = conn.execute('SELECT * FROM products WHERE id = ?', (prod_id,)).fetchone()
        if product:
            item_total = product['price'] * qty
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'item_total': item_total
            })
    conn.close()
    cart_count = sum(cart.values())
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=cart_count)

@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))
    conn = get_db()
    products = []
    total = 0
    for prod_id, qty in cart.items():
        product = conn.execute('SELECT * FROM products WHERE id = ?', (prod_id,)).fetchone()
        if product:
            item_total = product['price'] * qty
            total += item_total
            products.append({
                'product': product,
                'quantity': qty,
                'item_total': item_total
            })
    conn.close()
    cart_count = sum(cart.values())
    return render_template('checkout.html', products=products, total=total, cart_count=cart_count)

@app.route('/process_order', methods=['POST'])
def process_order():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))
    
    # Get customer info
    customer_name = request.form.get('name', '').strip()
    customer_email = request.form.get('email', '').strip()
    shipping_address = request.form.get('address', '').strip()
    
    # Validate required fields
    errors = []
    if not customer_name:
        errors.append('Name is required.')
    if not customer_email or '@' not in customer_email:
        errors.append('Valid email is required.')
    if not shipping_address:
        errors.append('Shipping address is required.')
    
    # Get payment info
    card_number = request.form.get('card_number', '').strip()
    exp_month = request.form.get('exp_month', '').strip()
    exp_year = request.form.get('exp_year', '').strip()
    cvv = request.form.get('cvv', '').strip()
    
    # Validate payment info (mathematical validation only - no real payment)
    if not luhn_check(card_number):
        errors.append('Invalid card number (failed Luhn check).')
    if not validate_expiration_date(exp_month, exp_year):
        errors.append('Invalid or expired card expiration date.')
    if not validate_cvv(cvv):
        errors.append('Invalid CVV (must be 3 or 4 digits).')
    
    if errors:
        conn = get_db()
        products = []
        total = 0
        for prod_id, qty in cart.items():
            product = conn.execute('SELECT * FROM products WHERE id = ?', (prod_id,)).fetchone()
            if product:
                item_total = product['price'] * qty
                total += item_total
                products.append({
                    'product': product,
                    'quantity': qty,
                    'item_total': item_total
                })
        conn.close()
        cart_count = sum(cart.values())
        return render_template('checkout.html', products=products, total=total, cart_count=cart_count, errors=errors, form_data=request.form)
    
    # Store order in database
    conn = get_db()
    total = 0
    for prod_id, qty in cart.items():
        product = conn.execute('SELECT * FROM products WHERE id = ?', (prod_id,)).fetchone()
        if product:
            total += product['price'] * qty
    
    # Get last 4 digits of card for display
    card_last_four = card_number.replace(' ', '').replace('-', '')[-4:]
    
    conn.execute(
        'INSERT INTO orders (customer_name, customer_email, shipping_address, total, card_last_four) VALUES (?, ?, ?, ?, ?)',
        (customer_name, customer_email, shipping_address, round(total, 2), card_last_four)
    )
    order_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    
    for prod_id, qty in cart.items():
        product = conn.execute('SELECT * FROM products WHERE id = ?', (prod_id,)).fetchone()
        if product:
            conn.execute(
                'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                (order_id, product['id'], qty, product['price'])
            )
    
    conn.commit()
    conn.close()
    
    # Clear cart
    session['cart'] = {}
    
    return redirect(url_for('order_confirmation', order_id=order_id))

@app.route('/confirmation/<int:order_id>')
def order_confirmation(order_id):
    conn = get_db()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if order is None:
        return redirect(url_for('index'))
    items = conn.execute('''
        SELECT oi.*, p.name, p.brand, p.image_url 
        FROM order_items oi 
        JOIN products p ON oi.product_id = p.id 
        WHERE oi.order_id = ?
    ''', (order_id,)).fetchall()
    conn.close()
    return render_template('confirmation.html', order=order, items=items)

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)