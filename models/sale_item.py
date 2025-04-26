import sqlite3
from db.db_manager import DBManager

class SaleItem:
    def __init__(self):
        self.db = DBManager()
    
    def add_sale_item(self, sale_id, product_id, quantity, price, discount, total):
        """إضافة عنصر للفاتورة"""
        query = """
        INSERT INTO sale_items (sale_id, product_id, quantity, price, discount, total)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (sale_id, product_id, quantity, price, discount, total)
        
        return self.db.execute_query(query, params)
    
    def get_sale_items(self, sale_id):
        """الحصول على عناصر فاتورة معينة"""
        query = """
        SELECT si.*, p.name as product_name, p.barcode
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
        """
        
        return self.db.fetch_all(query, (sale_id,))
    
    def get_sale_items_report(self, start_date=None, end_date=None, product_id=None):
        """الحصول على تقرير عن عناصر المبيعات"""
        query = """
        SELECT si.*, p.name as product_name, p.barcode, s.date
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND s.date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND s.date <= ?"
            params.append(end_date)
        
        if product_id:
            query += " AND si.product_id = ?"
            params.append(product_id)
        
        query += " ORDER BY s.date DESC"
        
        return self.db.fetch_all(query, tuple(params))