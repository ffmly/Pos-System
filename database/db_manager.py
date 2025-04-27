import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path=None):
        # تحديد مسار قاعدة البيانات
        self.db_path = db_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pos.db')
        
        # التأكد من وجود مجلد البيانات
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # إنشاء الاتصال وتهيئة قاعدة البيانات
        self.connection = None
        self.cursor = None
        
        # إنشاء جداول قاعدة البيانات إذا لم تكن موجودة
        self.initialize_database()
    
    def connect(self):
        """إنشاء اتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def commit(self):
        """حفظ التغييرات"""
        if self.connection:
            self.connection.commit()
    
    def initialize_database(self):
        if self.connect():
            self.create_tables()
            self.disconnect()
    
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        # جدول المستخدمين
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
        
        # جدول فئات المنتجات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول المنتجات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            purchase_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            min_quantity INTEGER DEFAULT 5,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        ''')
        
        # جدول المبيعات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            total_amount REAL NOT NULL,
            discount REAL DEFAULT 0,
            tax REAL DEFAULT 0,
            final_amount REAL NOT NULL,
            payment_method TEXT DEFAULT 'cash',
            user_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # جدول تفاصيل المبيعات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # جدول المستخدمين
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول الإعدادات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT DEFAULT 'My Store',
            store_address TEXT,
            store_phone TEXT,
            store_email TEXT,
            tax_percentage REAL DEFAULT 15,
            logo_path TEXT,
            receipt_footer TEXT
        )
        ''')
        
        # إنشاء مستخدم افتراضي إذا لم يكن هناك مستخدمين
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
            INSERT INTO users (username, password, full_name, role)
            VALUES ('admin', 'admin123', 'System Administrator', 'admin')
            ''')
            
        # إنشاء فئة افتراضية
        self.cursor.execute("SELECT COUNT(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES ('General', 'Default category for products')
            ''')
        
        # إنشاء إعدادات افتراضية
        self.cursor.execute("SELECT COUNT(*) FROM settings")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
            INSERT INTO settings (store_name, store_address, store_phone, tax_percentage, receipt_footer)
            VALUES ('My Store', 'Store Address', '1234567890', 15, 'Thank you for your business!')
            ''')
        
        self.commit()

    # User management methods
    def authenticate_user(self, username, password):
        self.cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        return self.cursor.fetchone()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    # Category management methods
    def add_category(self, name, description):
        try:
            self.cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            ''', (name, description))
            self.commit()
            return True
        except sqlite3.Error:
            return False

    def get_categories(self):
        self.cursor.execute('SELECT * FROM categories ORDER BY name')
        return self.cursor.fetchall()

    # Product management methods
    def add_product(self, product_data):
        try:
            self.cursor.execute('''
            INSERT INTO products (barcode, name, description, category_id, 
                                purchase_price, selling_price, quantity, min_quantity, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data.get('barcode'),
                product_data.get('name'),
                product_data.get('description'),
                product_data.get('category_id'),
                product_data.get('purchase_price'),
                product_data.get('selling_price'),
                product_data.get('quantity', 0),
                product_data.get('min_quantity', 5),
                product_data.get('image_path')
            ))
            self.commit()
            return True
        except sqlite3.Error:
            return False

    def get_products(self, category_id=None):
        if category_id:
            self.cursor.execute('''
            SELECT * FROM products WHERE category_id = ? ORDER BY name
            ''', (category_id,))
        else:
            self.cursor.execute('SELECT * FROM products ORDER BY name')
        return self.cursor.fetchall()

    def update_product_quantity(self, product_id, quantity):
        try:
            self.cursor.execute('''
            UPDATE products SET quantity = quantity + ? WHERE id = ?
            ''', (quantity, product_id))
            self.commit()
            return True
        except sqlite3.Error:
            return False

    # Sales management methods
    def create_sale(self, sale_data):
        try:
            self.cursor.execute('''
            INSERT INTO sales (invoice_number, customer_id, total_amount, discount, 
                             tax, final_amount, payment_method, user_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale_data.get('invoice_number'),
                sale_data.get('customer_id'),
                sale_data.get('total_amount'),
                sale_data.get('discount', 0),
                sale_data.get('tax', 0),
                sale_data.get('final_amount'),
                sale_data.get('payment_method', 'cash'),
                sale_data.get('user_id'),
                sale_data.get('notes')
            ))
            sale_id = self.cursor.lastrowid
            self.commit()
            return sale_id
        except sqlite3.Error:
            return None

    def add_sale_items(self, sale_id, items):
        try:
            for item in items:
                self.cursor.execute('''
                INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    sale_id,
                    item.get('product_id'),
                    item.get('quantity'),
                    item.get('unit_price'),
                    item.get('total_price')
                ))
                # Update product quantity
                self.update_product_quantity(item.get('product_id'), -item.get('quantity'))
            self.commit()
            return True
        except sqlite3.Error:
            return False

    def get_sales(self, start_date=None, end_date=None):
        query = 'SELECT * FROM sales'
        params = []
        if start_date and end_date:
            query += ' WHERE created_at BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        query += ' ORDER BY created_at DESC'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

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