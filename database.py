import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")

def init_db(db_path=DB_PATH):
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        rating REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        cost REAL NOT NULL,
        supplier_id INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        signup_date TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        shipping_fee REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)

    # Seed data
    suppliers = [
        ("Global Tech Supplies", "USA", 4.5),
        ("Apex Manufacturing", "Germany", 4.8),
        ("Zenith Goods", "Japan", 4.2),
        ("Meridian Trade", "UK", 4.6)
    ]
    cursor.executemany("INSERT INTO suppliers (name, country, rating) VALUES (?, ?, ?)", suppliers)

    products = [
        ("Wireless Ergonomic Mouse", "Electronics", 49.99, 25.00, 1),
        ("Mechanical Gaming Keyboard", "Electronics", 129.99, 60.00, 1),
        ("UltraWide 34-inch Monitor", "Electronics", 499.99, 300.00, 2),
        ("USB-C Hub 7-in-1", "Accessories", 34.99, 12.00, 1),
        ("Ergonomic Office Chair", "Furniture", 249.99, 120.00, 2),
        ("Standing Desk Adjustable", "Furniture", 399.99, 180.00, 2),
        ("Noise-Canceling Headphones", "Electronics", 199.99, 90.00, 3),
        ("HD Webcam 1080p", "Electronics", 79.99, 35.00, 3),
        ("LED Desk Lamp", "Accessories", 45.99, 18.00, 4),
        ("Laptop Stand Aluminum", "Accessories", 29.99, 10.00, 4)
    ]
    cursor.executemany("INSERT INTO products (name, category, price, cost, supplier_id) VALUES (?, ?, ?, ?, ?)", products)

    customers = [
        ("Alice Smith", "alice@example.com", "New York", "USA", "2025-01-15"),
        ("Bob Jones", "bob@example.com", "London", "UK", "2025-02-10"),
        ("Charlie Brown", "charlie@example.com", "Berlin", "Germany", "2025-03-01"),
        ("Diana Prince", "diana@example.com", "Paris", "France", "2025-03-12"),
        ("Ethan Hunt", "ethan@example.com", "Tokyo", "Japan", "2025-04-05"),
        ("Fiona Gallagher", "fiona@example.com", "Chicago", "USA", "2025-05-20"),
        ("George Clark", "georg@example.com", "Sydney", "Australia", "2025-06-01"),
        ("Hannah Abbott", "hannah@example.com", "Toronto", "Canada", "2025-06-15")
    ]
    cursor.executemany("INSERT INTO customers (name, email, city, country, signup_date) VALUES (?, ?, ?, ?, ?)", customers)

    orders = [
        (1, "2026-01-10", "Completed", 10.0),
        (2, "2026-01-12", "Completed", 15.0),
        (3, "2026-01-15", "Shipped", 0.0),
        (4, "2026-02-01", "Completed", 20.0),
        (5, "2026-02-05", "Pending", 12.0),
        (6, "2026-02-10", "Completed", 10.0),
        (1, "2026-02-15", "Completed", 15.0),
        (7, "2026-03-01", "Completed", 25.0),
        (8, "2026-03-05", "Completed", 10.0),
        (2, "2026-03-10", "Cancelled", 0.0),
        (3, "2026-03-15", "Completed", 15.0),
        (4, "2026-04-01", "Completed", 10.0)
    ]
    cursor.executemany("INSERT INTO orders (customer_id, order_date, status, shipping_fee) VALUES (?, ?, ?, ?)", orders)

    items_with_price = [
        (1, 2, 1, 129.99),
        (1, 1, 2, 49.99),
        (2, 1, 1, 49.99),
        (3, 1, 1, 249.99),
        (4, 2, 1, 129.99),
        (5, 3, 1, 499.99),
        (6, 4, 2, 34.99),
        (7, 5, 1, 249.99),
        (8, 6, 1, 399.99),
        (9, 7, 2, 199.99),
        (10, 8, 1, 79.99),
        (11, 9, 3, 45.99),
        (12, 10, 2, 29.99)
    ]
    cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)", items_with_price)

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {db_path}")

if __name__ == "__main__":
    init_db()
