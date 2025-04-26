from database.db_manager import DatabaseManager

class Product:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def add_product(self, barcode, name, description, category_id, price, cost_price, quantity, min_quantity):
        """إضافة منتج جديد"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            INSERT INTO products (barcode, name, description, category_id, price, cost_price, quantity, min_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (barcode, name, description, category_id, price, cost_price, quantity, min_quantity))
            self.db_manager.commit()
            product_id = cursor.lastrowid
            return product_id
        except Exception as e:
            print(f"خطأ في إضافة المنتج: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def update_product(self, product_id, barcode, name, description, category_id, price, cost_price, quantity, min_quantity):
        """تحديث بيانات منتج"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            UPDATE products
            SET barcode = ?, name = ?, description = ?, category_id = ?, 
                price = ?, cost_price = ?, quantity = ?, min_quantity = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (barcode, name, description, category_id, price, cost_price, quantity, min_quantity, product_id))
            self.db_manager.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"خطأ في تحديث المنتج: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def delete_product(self, product_id):
        """حذف منتج"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.db_manager.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"خطأ في حذف المنتج: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def get_product(self, product_id):
        """الحصول على بيانات منتج بواسطة المعرف"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT p.*, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?
            ''', (product_id,))
            return dict(cursor.fetchone())
        except Exception as e:
            print(f"خطأ في الحصول على بيانات المنتج: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def get_product_by_barcode(self, barcode):
        """الحصول على بيانات منتج بواسطة الباركود"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT p.*, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.barcode = ?
            ''', (barcode,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"خطأ في الحصول على بيانات المنتج بالباركود: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def get_all_products(self, search_term=None, category_id=None):
        """الحصول على جميع المنتجات مع إمكانية البحث والتصفية"""
        try:
            cursor = self.db_manager.connect()
            query = '''
            SELECT p.*, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            '''
            params = []
            
            if search_term or category_id:
                query += " WHERE "
                conditions = []
                
                if search_term:
                    conditions.append("(p.name LIKE ? OR p.barcode LIKE ? OR p.description LIKE ?)")
                    params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
                
                if category_id:
                    conditions.append("p.category_id = ?")
                    params.append(category_id)
                
                query += " AND ".join(conditions)
            
            query += " ORDER BY p.name"
            cursor.execute(query, params)
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"خطأ في الحصول على المنتجات: {e}")
            return []
        finally:
            self.db_manager.disconnect()
    
    def update_stock(self, product_id, quantity_change):
        """تحديث المخزون (إضافة أو خصم)"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            UPDATE products
            SET quantity = quantity + ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (quantity_change, product_id))
            self.db_manager.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"خطأ في تحديث المخزون: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def get_low_stock_products(self):
        """الحصول على المنتجات التي وصلت إلى الحد الأدنى للمخزون"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT p.*, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.quantity <= p.min_quantity
            ORDER BY p.quantity ASC
            ''')
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"خطأ في الحصول على المنتجات منخفضة المخزون: {e}")
            return []
        finally:
            self.db_manager.disconnect()