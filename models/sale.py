from database.db_manager import DatabaseManager
import datetime
import random
import string

class Sale:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def generate_invoice_number(self):
        """توليد رقم فاتورة فريد"""
        # توليد رقم فاتورة بتنسيق: INV-YYYYMMDD-XXXX
        today = datetime.datetime.now().strftime('%Y%m%d')
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"INV-{today}-{random_chars}"
    
    def add_sale(self, customer_name, customer_phone, total_amount, discount, tax, final_amount, payment_method, user_id):
        """إضافة فاتورة جديدة"""
        try:
            cursor = self.db_manager.connect()
            
            # توليد رقم فاتورة فريد
            invoice_number = self.generate_invoice_number()
            
            cursor.execute('''
            INSERT INTO sales (invoice_number, customer_name, customer_phone, total_amount, discount, tax, final_amount, payment_method, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, customer_name, customer_phone, total_amount, discount, tax, final_amount, payment_method, user_id))
            
            self.db_manager.commit()
            sale_id = cursor.lastrowid
            return sale_id
        except Exception as e:
            print(f"خطأ في إضافة الفاتورة: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def get_sale(self, sale_id):
        """الحصول على بيانات فاتورة بواسطة المعرف"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT * FROM sales WHERE id = ?
            ''', (sale_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"خطأ في الحصول على بيانات الفاتورة: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def get_sales(self, start_date=None, end_date=None, customer_name=None):
        """الحصول على قائمة الفواتير مع إمكانية التصفية"""
        try:
            cursor = self.db_manager.connect()
            
            query = "SELECT * FROM sales"
            params = []
            conditions = []
            
            if start_date:
                conditions.append("DATE(created_at) >= ?")
                params.append(start_date)
            
            if end_date:
                conditions.append("DATE(created_at) <= ?")
                params.append(end_date)
            
            if customer_name:
                conditions.append("customer_name LIKE ?")
                params.append(f"%{customer_name}%")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"خطأ في الحصول على الفواتير: {e}")
            return []
        finally:
            self.db_manager.disconnect()
    
    def get_sales_report(self, start_date, end_date):
        """الحصول على تقرير المبيعات خلال فترة زمنية محددة"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT 
                COUNT(*) as total_sales,
                SUM(total_amount) as total_amount,
                SUM(discount) as total_discount,
                SUM(tax) as total_tax,
                SUM(final_amount) as total_final_amount,
                payment_method,
                COUNT(DISTINCT DATE(created_at)) as days_count
            FROM sales
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY payment_method
            ''', (start_date, end_date))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"خطأ في الحصول على تقرير المبيعات: {e}")
            return []
        finally:
            self.db_manager.disconnect()
    
    def get_today_sales_stats(self):
        """الحصول على إحصائيات المبيعات اليومية"""
        try:
            cursor = self.db_manager.connect()
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
            SELECT 
                COUNT(*) as count,
                SUM(final_amount) as total_amount
            FROM sales
            WHERE DATE(created_at) = ?
            ''', (today,))
            
            result = cursor.fetchone()
            if result and result['count'] > 0:
                return dict(result)
            else:
                return {'count': 0, 'total_amount': 0.0}
        except Exception as e:
            print(f"خطأ في الحصول على إحصائيات المبيعات اليومية: {e}")
            return {'count': 0, 'total_amount': 0.0}
        finally:
            self.db_manager.disconnect()