-- جدول الفئات
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المنتجات
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
);

-- جدول المبيعات
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE,
    total_amount REAL NOT NULL,
    discount REAL DEFAULT 0,
    tax REAL DEFAULT 0,
    final_amount REAL NOT NULL,
    payment_method TEXT DEFAULT 'نقدي',
    customer_name TEXT,
    customer_phone TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول تفاصيل المبيعات
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- جدول المستخدمين
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'موظف',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إدخال مستخدم افتراضي (admin/admin)
INSERT OR IGNORE INTO users (username, password, full_name, role) 
VALUES ('admin', 'admin', 'مدير النظام', 'مدير');

-- جدول إعدادات النظام
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT DEFAULT 'متجري',
    store_address TEXT,
    store_phone TEXT,
    store_email TEXT,
    tax_percentage REAL DEFAULT 15,
    logo_path TEXT,
    receipt_footer TEXT
);

-- إدخال إعدادات افتراضية
INSERT OR IGNORE INTO settings (id, store_name, store_address, store_phone, tax_percentage, receipt_footer) 
VALUES (1, 'متجري', 'العنوان', '0123456789', 15, 'شكراً لزيارتكم');