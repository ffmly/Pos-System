import sqlite3
import os
import time
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_path = 'pos.db'
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def initialize_database(self):
        """Initialize the database connection and create tables"""
        try:
            # Try to connect to existing database first
            if os.path.exists(self.db_path):
                try:
                    self.conn = sqlite3.connect(self.db_path)
                    self.cursor = self.conn.cursor()
                    # Check if tables exist
                    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
                    if not self.cursor.fetchone():
                        self.create_tables()
                    return True
                except sqlite3.Error:
                    # If connection fails, try to delete and recreate
                    self.disconnect()
                    time.sleep(1)  # Wait a bit before trying to delete
                    try:
                        os.remove(self.db_path)
                    except:
                        pass  # Ignore if file can't be deleted
            else:
                # Create new database
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                self.create_tables()
            
            print("Database initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False

    def connect(self):
        """Connect to the database"""
        try:
            if not self.conn:
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                print("Successfully connected to database")
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close the database connection"""
        if self.conn:
            try:
                self.conn.close()
                print("Successfully disconnected from database")
            except:
                print("Error closing database connection")
            self.conn = None
            self.cursor = None

    def ensure_connection(self):
        """Ensure database connection is active"""
        if not self.conn:
            return self.connect()
        return True

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Categories table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Products table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    barcode TEXT UNIQUE,
                    price REAL NOT NULL,
                    cost REAL NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    min_quantity INTEGER DEFAULT 5,
                    category_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')

            # Sales table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    total_amount REAL NOT NULL,
                    discount REAL DEFAULT 0,
                    tax REAL DEFAULT 0,
                    final_amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Sale items table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')

            # Create default admin user if not exists
            self.cursor.execute("SELECT COUNT(*) FROM users")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    INSERT INTO users (username, password, full_name, role)
                    VALUES (?, ?, ?, ?)
                ''', ('admin', 'admin123', 'Administrator', 'admin'))
                print("Created default admin user")

            # Create default category if not exists
            self.cursor.execute("SELECT COUNT(*) FROM categories")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    INSERT INTO categories (name, description)
                    VALUES (?, ?)
                ''', ('General', 'Default category for products'))
                print("Created default category")

            self.conn.commit()
            print("Tables created successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False

    def authenticate_user(self, username, password):
        """Authenticate a user"""
        try:
            # First check if the user exists
            self.cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            user = self.cursor.fetchone()
            
            if user and user[2] == password:  # user[2] is the password field
                return {
                    'id': user[0],
                    'username': user[1],
                    'full_name': user[3],
                    'role': user[4]
                }
            return None
        except sqlite3.Error as e:
            print(f"Authentication error: {e}")
            return None

    def get_categories(self):
        """Get all categories"""
        try:
            if not self.ensure_connection():
                return []

            self.cursor.execute("SELECT * FROM categories ORDER BY name")
            categories = self.cursor.fetchall()
            print(f"Retrieved {len(categories)} categories")
            return categories
        except sqlite3.Error as e:
            print(f"Error getting categories: {e}")
            return []

    def add_category(self, name, description=""):
        """Add a new category"""
        try:
            if not self.ensure_connection():
                return False

            # Check if category already exists
            self.cursor.execute(
                "SELECT id FROM categories WHERE name = ?",
                (name,)
            )
            if self.cursor.fetchone():
                print(f"Category '{name}' already exists")
                return False

            # Add the category
            self.cursor.execute(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                (name, description)
            )
            self.conn.commit()
            print(f"Successfully added category: {name}")
            return True
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            return False

    def get_products(self, category_id=None):
        """Get all products or products by category"""
        try:
            if not self.ensure_connection():
                return []

            if category_id:
                self.cursor.execute(
                    "SELECT * FROM products WHERE category_id = ? ORDER BY name",
                    (category_id,)
                )
            else:
                self.cursor.execute("SELECT * FROM products ORDER BY name")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting products: {e}")
            return []

    def add_product(self, name, description, barcode, price, cost, quantity, category_id, min_quantity=5):
        """Add a new product"""
        try:
            if not self.ensure_connection():
                return False

            self.cursor.execute(
                """INSERT INTO products 
                   (name, description, barcode, price, cost, quantity, category_id, min_quantity)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, description, barcode, price, cost, quantity, category_id, min_quantity)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")
            return False

    def update_product_quantity(self, product_id, quantity):
        """Update product quantity"""
        try:
            if not self.ensure_connection():
                return False

            self.cursor.execute(
                "UPDATE products SET quantity = quantity + ? WHERE id = ?",
                (quantity, product_id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product quantity: {e}")
            return False

    def get_sales(self, start_date=None, end_date=None):
        """Get all sales or sales within a date range"""
        try:
            if not self.ensure_connection():
                return []

            query = """
                SELECT s.*, u.full_name as user_name 
                FROM sales s 
                LEFT JOIN users u ON s.user_id = u.id
            """
            params = []
            
            if start_date and end_date:
                query += " WHERE s.created_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            query += " ORDER BY s.created_at DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting sales: {e}")
            return []

    def get_sale_items(self, sale_id):
        """Get items for a specific sale"""
        try:
            if not self.ensure_connection():
                return []

            self.cursor.execute("""
                SELECT si.*, p.name as product_name 
                FROM sale_items si 
                LEFT JOIN products p ON si.product_id = p.id 
                WHERE si.sale_id = ?
            """, (sale_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting sale items: {e}")
            return []

    def create_sale(self, invoice_number, total_amount, discount, tax, final_amount, payment_method, user_id):
        """Create a new sale"""
        try:
            if not self.ensure_connection():
                return None

            self.cursor.execute(
                """INSERT INTO sales 
                   (invoice_number, total_amount, discount, tax, final_amount, payment_method, user_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (invoice_number, total_amount, discount, tax, final_amount, payment_method, user_id)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating sale: {e}")
            return None

    def add_sale_item(self, sale_id, product_id, quantity, price, total):
        """Add an item to a sale"""
        try:
            if not self.ensure_connection():
                return False

            self.cursor.execute(
                """INSERT INTO sale_items 
                   (sale_id, product_id, quantity, price, total)
                   VALUES (?, ?, ?, ?, ?)""",
                (sale_id, product_id, quantity, price, total)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding sale item: {e}")
            return False

    def get_sale_by_id(self, sale_id):
        """Get a specific sale by ID"""
        try:
            if not self.ensure_connection():
                return None

            self.cursor.execute("""
                SELECT s.*, u.full_name as user_name 
                FROM sales s 
                LEFT JOIN users u ON s.user_id = u.id 
                WHERE s.id = ?
            """, (sale_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting sale: {e}")
            return None

    def get_sales_summary(self, start_date=None, end_date=None):
        """Get sales summary (total sales, total items, average sale)"""
        try:
            if not self.ensure_connection():
                return {
                    'total_sales': 0,
                    'total_amount': 0,
                    'average_sale': 0
                }

            query = """
                SELECT 
                    COUNT(*) as total_sales,
                    COALESCE(SUM(final_amount), 0) as total_amount,
                    COALESCE(AVG(final_amount), 0) as average_sale
                FROM sales
            """
            params = []
            
            if start_date and end_date:
                query += " WHERE created_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return {
                'total_sales': result[0] or 0,
                'total_amount': result[1] or 0,
                'average_sale': result[2] or 0
            }
        except sqlite3.Error as e:
            print(f"Error getting sales summary: {e}")
            return {
                'total_sales': 0,
                'total_amount': 0,
                'average_sale': 0
            }

    def get_low_stock_products(self):
        """Get products with quantity below minimum"""
        try:
            if not self.ensure_connection():
                return []

            self.cursor.execute("""
                SELECT p.*, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.quantity <= p.min_quantity
                ORDER BY p.quantity ASC
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting low stock products: {e}")
            return []

    def commit(self):
        """حفظ التغييرات"""
        if self.conn:
            self.conn.commit()

    def execute_query(self, query, params=None):
        """تنفيذ استعلام"""
        try:
            if self.connect():
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                self.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return False

    def fetch_one(self, query, params=None):
        """جلب سجل واحد"""
        try:
            if self.connect():
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                return self.cursor.fetchone()
            return None
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return None

    def fetch_all(self, query, params=None):
        """جلب جميع السجلات"""
        try:
            if self.connect():
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                return self.cursor.fetchall()
            return []
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return []

    # User management methods
    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    # Customer management methods
    def add_customer(self, customer_data):
        try:
            self.cursor.execute('''
            INSERT INTO customers (name, phone, email, address)
            VALUES (?, ?, ?, ?)
            ''', (
                customer_data.get('name'),
                customer_data.get('phone'),
                customer_data.get('email'),
                customer_data.get('address')
            ))
            self.commit()
            return True
        except sqlite3.Error:
            return False

    def get_customers(self):
        self.cursor.execute('SELECT * FROM customers ORDER BY name')
        return self.cursor.fetchall()

    # Settings management methods
    def get_settings(self):
        self.cursor.execute('SELECT * FROM settings WHERE id = 1')
        return self.cursor.fetchone()

    def update_settings(self, settings_data):
        try:
            self.cursor.execute('''
            UPDATE settings SET 
                store_name = ?,
                store_address = ?,
                store_phone = ?,
                store_email = ?,
                tax_percentage = ?,
                logo_path = ?,
                receipt_footer = ?
            WHERE id = 1
            ''', (
                settings_data.get('store_name'),
                settings_data.get('store_address'),
                settings_data.get('store_phone'),
                settings_data.get('store_email'),
                settings_data.get('tax_percentage'),
                settings_data.get('logo_path'),
                settings_data.get('receipt_footer')
            ))
            self.commit()
            return True
        except sqlite3.Error:
            return False

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.disconnect()