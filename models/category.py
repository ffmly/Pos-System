from database.db_manager import DatabaseManager

class Category:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def add_category(self, name, description=None):
        """إضافة فئة جديدة"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            ''', (name, description))
            self.db_manager.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"خطأ في إضافة الفئة: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def update_category(self, category_id, name, description=None):
        """تحديث بيانات فئة"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            UPDATE categories
            SET name = ?, description = ?
            WHERE id = ?
            ''', (name, description, category_id))
            self.db_manager.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"خطأ في تحديث الفئة: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def delete_category(self, category_id):
        """حذف فئة"""
        try:
            cursor = self.db_manager.connect()
            
            # تحديث المنتجات المرتبطة بهذه الفئة لتكون بدون فئة
            cursor.execute('''
            UPDATE products
            SET category_id = NULL
            WHERE category_id = ?
            ''', (category_id,))
            
            # حذف الفئة
            cursor.execute('''
            DELETE FROM categories
            WHERE id = ?
            ''', (category_id,))
            
            self.db_manager.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"خطأ في حذف الفئة: {e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def get_category(self, category_id):
        """الحصول على بيانات فئة بواسطة المعرف"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT * FROM categories
            WHERE id = ?
            ''', (category_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"خطأ في الحصول على بيانات الفئة: {e}")
            return None
        finally:
            self.db_manager.disconnect()
    
    def get_all_categories(self):
        """الحصول على جميع الفئات"""
        try:
            cursor = self.db_manager.connect()
            cursor.execute('''
            SELECT * FROM categories
            ORDER BY name
            ''')
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"خطأ في الحصول على الفئات: {e}")
            return []
        finally:
            self.db_manager.disconnect()