from database.db_manager import DatabaseManager
import datetime

class Inventory:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_inventory_status(self):
        """الحصول على حالة المخزون الحالية"""
        query = """
        SELECT 
            p.id, p.name, p.barcode, p.quantity, p.min_quantity,
            c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY p.quantity
        """
        return self.db.fetch_all(query)
    
    def get_low_stock_products(self):
        """الحصول على المنتجات منخفضة المخزون"""
        query = """
        SELECT 
            p.id, p.name, p.barcode, p.quantity, p.min_quantity,
            c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.quantity <= p.min_quantity
        ORDER BY p.quantity
        """
        return self.db.fetch_all(query)
    
    def update_stock(self, product_id, new_quantity, notes=""):
        """تحديث كمية المخزون"""
        try:
            conn, cursor = self.db.connect()
            
            # الحصول على الكمية الحالية
            cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
            current_quantity = cursor.fetchone()[0]
            
            # حساب التغيير في الكمية
            quantity_change = new_quantity - current_quantity
            
            # تحديث المخزون
            cursor.execute(
                "UPDATE products SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_quantity, product_id)
            )
            
            # تسجيل عملية تحديث المخزون
            cursor.execute(
                """
                INSERT INTO inventory_log 
                (product_id, previous_quantity, new_quantity, change_amount, notes, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (product_id, current_quantity, new_quantity, quantity_change, notes)
            )
            
            conn.commit()
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"خطأ في تحديث المخزون: {e}")
            return False
        finally:
            self.db.close()
    
    def get_inventory_history(self, product_id=None, start_date=None, end_date=None, limit=100):
        """الحصول على سجل تغييرات المخزون"""
        query = """
        SELECT 
            il.*, p.name as product_name, p.barcode
        FROM inventory_log il
        JOIN products p ON il.product_id = p.id
        """
        
        conditions = []
        params = []
        
        if product_id:
            conditions.append("il.product_id = ?")
            params.append(product_id)
        
        if start_date:
            conditions.append("il.created_at >= ?")
            params.append(start_date)
        
        if end_date:
            conditions.append("il.created_at <= ?")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY il.created_at DESC LIMIT ?"
        params.append(limit)
        
        return self.db.fetch_all(query, params)