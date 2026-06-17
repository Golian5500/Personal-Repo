import sqlite3
import hashlib
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'store.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT,
            description TEXT
        )
    ''')

    # Orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            shipping_address TEXT NOT NULL,
            total REAL NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            card_last_four TEXT NOT NULL
        )
    ''')

    # Order items table
    c.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Insert sample makeup products if empty
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        products = [
            ('Velvet Matte Lipstick', 'Luxe Beauty', 'Lipstick', 24.99, 'https://via.placeholder.com/200x200/FF6B6B/FFFFFF?text=Lipstick', 'Long-lasting matte lipstick with a velvety finish.'),
            ('Luminous Foundation', 'Glow Cosmetics', 'Foundation', 39.99, 'https://via.placeholder.com/200x200/FADADD/333333?text=Foundation', 'Lightweight foundation for a natural, luminous glow.'),
            ('Midnight Eyeshadow Palette', 'Starlight', 'Eyeshadow', 49.99, 'https://via.placeholder.com/200x200/4A4A6A/FFFFFF?text=Palette', '12-shade eyeshadow palette with rich pigmentation.'),
            ('Volumizing Mascara', 'Lash Queen', 'Mascara', 19.99, 'https://via.placeholder.com/200x200/2C2C2C/FFFFFF?text=Mascara', 'Intense volume and length for dramatic lashes.'),
            ('Creamy Concealer', 'Flawless Finish', 'Concealer', 14.99, 'https://via.placeholder.com/200x200/FFE4B5/333333?text=Concealer', 'Full coverage concealer that blends seamlessly.'),
            ('Setting Spray', 'All Day Wear', 'Setting Spray', 12.99, 'https://via.placeholder.com/200x200/87CEEB/333333?text=Spray', 'Lock in your look with this long-lasting setting spray.'),
            ('Blush Duo', 'Rose Petal', 'Blush', 22.99, 'https://via.placeholder.com/200x200/FFB6C1/333333?text=Blush', 'Two complementary shades for a natural flush.'),
            ('Highlighter Stick', 'Glow Up', 'Highlighter', 18.99, 'https://via.placeholder.com/200x200/FFD700/333333?text=Highlight', 'Buildable cream highlighter for a radiant glow.'),
        ]
        c.executemany('INSERT INTO products (name, brand, category, price, image_url, description) VALUES (?, ?, ?, ?, ?, ?)', products)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()