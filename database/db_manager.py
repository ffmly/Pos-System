import sqlite3
import os

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
            return self.cursor
        except sqlite3.Error as e:
            print(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            return None
    
    def disconnect(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def commit(self):
        """حفظ التغييرات"""
        if self.conn:
            self.conn.commit()
    
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
            description TEXT
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
            price REAL NOT NULL,
            cost_price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            min_quantity INTEGER DEFAULT 5,
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
            customer_name TEXT,
            customer_phone TEXT,
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
        
        # جدول تفاصيل المبيعات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            discount REAL DEFAULT 0,
            total REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # إنشاء مستخدم افتراضي إذا لم يكن هناك مستخدمين
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
            INSERT INTO users (username, password, full_name, role)
            VALUES ('admin', 'admin123', 'المدير', 'admin')
            ''')
            
        # إنشاء فئة افتراضية
        self.cursor.execute("SELECT COUNT(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES ('عام', 'الفئة الافتراضية للمنتجات')
            ''')
        
        self.commit()