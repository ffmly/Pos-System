from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                            QHeaderView, QComboBox, QDoubleSpinBox, QMessageBox,
                            QDialog, QFormLayout, QSpinBox, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from models.product import Product
from models.sale import Sale
from models.sale_item import SaleItem
import datetime
import uuid

class ProductSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_model = Product()
        self.selected_product = None
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("بحث عن منتج")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout(self)
        
        # حقل البحث
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن منتج...")
        self.search_input.textChanged.connect(self.search_products)
        
        search_layout.addWidget(QLabel("البحث:"))
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # جدول المنتجات
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels([
            "الباركود", "اسم المنتج", "الفئة", "السعر", "الكمية"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SingleSelection)
        self.products_table.doubleClicked.connect(self.select_product)
        
        layout.addWidget(self.products_table)
        
        # أزرار الإجراءات
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.select_product)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        # تحميل المنتجات
        self.search_products()
    
    def search_products(self):
        """البحث عن المنتجات"""
        search_term = self.search_input.text()
        products = self.product_model.get_all_products(search_term)
        
        self.products_table.setRowCount(0)
        
        for row, product in enumerate(products):
            self.products_table.insertRow(row)
            
            # إضافة بيانات المنتج
            self.products_table.setItem(row, 0, QTableWidgetItem(product.get('barcode', '')))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.products_table.setItem(row, 2, QTableWidgetItem(product.get('category_name', '')))
            self.products_table.setItem(row, 3, QTableWidgetItem(f"{product['price']:.2f}"))
            
            # تلوين الكمية إذا كانت أقل من الحد الأدنى
            quantity_item = QTableWidgetItem(str(product['quantity']))
            if product['quantity'] <= product['min_quantity']:
                quantity_item.setBackground(Qt.red)
                quantity_item.setForeground(Qt.white)
            
            self.products_table.setItem(row, 4, quantity_item)
            
            # تخزين بيانات المنتج في العنصر
            for col in range(5):
                self.products_table.item(row, col).setData(Qt.UserRole, product)
    
    def select_product(self):
        """اختيار منتج"""
        selected_items = self.products_table.selectedItems()
        if selected_items:
            self.selected_product = selected_items[0].data(Qt.UserRole)
            self.accept()
        else:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار منتج")


class SalesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.product_model = Product()
        self.sale_model = Sale()
        self.sale_item_model = SaleItem()
        
        # تهيئة المتغيرات
        self.current_items = []  # قائمة المنتجات في الفاتورة الحالية
        self.total_amount = 0.0  # إجمالي المبلغ
        self.discount = 0.0      # الخصم
        self.tax = 0.0          # الضريبة
        self.final_amount = 0.0  # المبلغ النهائي
        
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # القسم العلوي - البحث وإضافة المنتجات
        top_section = QHBoxLayout()
        
        # حقل الباركود
        barcode_layout = QVBoxLayout()
        barcode_label = QLabel("الباركود:")
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("ادخل الباركود أو ابحث عن المنتج")
        self.barcode_input.returnPressed.connect(self.add_product_by_barcode)
        barcode_layout.addWidget(barcode_label)
        barcode_layout.addWidget(self.barcode_input)
        
        # زر البحث عن المنتج
        search_btn = QPushButton("بحث")
        search_btn.clicked.connect(self.show_product_search)
        
        top_section.addLayout(barcode_layout)
        top_section.addWidget(search_btn)
        
        main_layout.addLayout(top_section)
        
        # جدول المنتجات
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels([
            "الباركود", "اسم المنتج", "السعر", "الكمية", 
            "الخصم", "الإجمالي", "حذف"
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.items_table)
        
        # القسم السفلي - تفاصيل الفاتورة
        bottom_section = QHBoxLayout()
        
        # معلومات العميل
        customer_group = QVBoxLayout()
        customer_label = QLabel("معلومات العميل")
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("اسم العميل")
        self.customer_phone = QLineEdit()
        self.customer_phone.setPlaceholderText("رقم الهاتف")
        
        # طريقة الدفع
        payment_label = QLabel("طريقة الدفع:")
        self.payment_method = QComboBox()
        self.payment_method.addItems(["نقدي", "بطاقة ائتمان", "تحويل بنكي"])
        
        customer_group.addWidget(customer_label)
        customer_group.addWidget(self.customer_name)
        customer_group.addWidget(self.customer_phone)
        customer_group.addWidget(payment_label)
        customer_group.addWidget(self.payment_method)
        
        # تفاصيل المبلغ
        amount_group = QVBoxLayout()
        
        # الإجمالي
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("الإجمالي:"))
        self.total_label = QLabel("0.00")
        total_layout.addWidget(self.total_label)
        
        # الخصم
        discount_layout = QHBoxLayout()
        discount_layout.addWidget(QLabel("الخصم:"))
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setMinimum(0)
        self.discount_input.setMaximum(999999.99)
        self.discount_input.valueChanged.connect(self.update_totals)
        discount_layout.addWidget(self.discount_input)
        
        # الضريبة
        tax_layout = QHBoxLayout()
        tax_layout.addWidget(QLabel("الضريبة (%):"))
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setMinimum(0)
        self.tax_input.setMaximum(100)
        self.tax_input.setValue(15)  # ضريبة القيمة المضافة الافتراضية
        self.tax_input.valueChanged.connect(self.update_totals)
        tax_layout.addWidget(self.tax_input)
        
        # المبلغ النهائي
        final_layout = QHBoxLayout()
        final_layout.addWidget(QLabel("المبلغ النهائي:"))
        self.final_label = QLabel("0.00")
        final_layout.addWidget(self.final_label)
        
        amount_group.addLayout(total_layout)
        amount_group.addLayout(discount_layout)
        amount_group.addLayout(tax_layout)
        amount_group.addLayout(final_layout)
        
        # أزرار العمليات
        actions_group = QVBoxLayout()
        save_btn = QPushButton("حفظ الفاتورة")
        save_btn.clicked.connect(self.save_invoice)
        clear_btn = QPushButton("مسح الفاتورة")
        clear_btn.clicked.connect(self.clear_invoice)
        
        actions_group.addWidget(save_btn)
        actions_group.addWidget(clear_btn)
        
        bottom_section.addLayout(customer_group)
        bottom_section.addLayout(amount_group)
        bottom_section.addLayout(actions_group)
        
        main_layout.addLayout(bottom_section)
    
    def add_product_by_barcode(self):
        """إضافة منتج باستخدام الباركود"""
        barcode = self.barcode_input.text().strip()
        if not barcode:
            return
        
        # البحث عن المنتج
        product = self.product_model.get_product_by_barcode(barcode)
        if not product:
            QMessageBox.warning(self, "خطأ", "المنتج غير موجود")
            return
        
        self.add_product_to_invoice(product)
        self.barcode_input.clear()
    
    def show_product_search(self):
        """عرض نافذة البحث عن المنتجات"""
        dialog = ProductSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_product:
            self.add_product_to_invoice(dialog.selected_product)
    
    def add_product_to_invoice(self, product):
        """إضافة منتج إلى الفاتورة"""
        # التحقق من المخزون
        if product['quantity'] <= 0:
            QMessageBox.warning(self, "تنبيه", f"المنتج '{product['name']}' غير متوفر في المخزون")
            return
        
        # التحقق مما إذا كان المنتج موجودًا بالفعل في الفاتورة
        for i, item in enumerate(self.current_items):
            if item['product_id'] == product['id']:
                # زيادة الكمية
                if item['quantity'] + 1 > product['quantity']:
                    QMessageBox.warning(self, "تنبيه", f"الكمية المطلوبة غير متوفرة في المخزون")
                    return
                
                item['quantity'] += 1
                item['total'] = item['price'] * item['quantity'] * (1 - item['discount'] / 100)
                
                # تحديث الجدول
                self.items_table.item(i, 3).setText(str(item['quantity']))
                self.items_table.item(i, 5).setText(f"{item['total']:.2f}")
                
                self.update_totals()
                return
        
        # إضافة منتج جديد
        item = {
            'product_id': product['id'],
            'barcode': product.get('barcode', ''),
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'discount': 0,
            'total': product['price']
        }
        
        self.current_items.append(item)
        
        # إضافة صف جديد في الجدول
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        
        # إضافة بيانات المنتج
        self.items_table.setItem(row, 0, QTableWidgetItem(item['barcode']))
        self.items_table.setItem(row, 1, QTableWidgetItem(item['name']))
        self.items_table.setItem(row, 2, QTableWidgetItem(f"{item['price']:.2f}"))
        self.items_table.setItem(row, 3, QTableWidgetItem(str(item['quantity'])))
        
        # إضافة حقل الخصم
        discount_spin = QDoubleSpinBox()
        discount_spin.setMinimum(0)
        discount_spin.setMaximum(100)
        discount_spin.setValue(item['discount'])
        discount_spin.valueChanged.connect(lambda value, row=row: self.update_item_discount(row, value))
        self.items_table.setCellWidget(row, 4, discount_spin)
        
        self.items_table.setItem(row, 5, QTableWidgetItem(f"{item['total']:.2f}"))
        
        # إضافة زر الحذف
        delete_btn = QPushButton("حذف")
        delete_btn.clicked.connect(lambda _, row=row: self.remove_item(row))
        self.items_table.setCellWidget(row, 6, delete_btn)
        
        self.update_totals()
    
    def update_item_discount(self, row, value):
        """تحديث خصم المنتج"""
        if row < 0 or row >= len(self.current_items):
            return
        
        self.current_items[row]['discount'] = value
        price = self.current_items[row]['price']
        quantity = self.current_items[row]['quantity']
        discount = self.current_items[row]['discount']
        
        # حساب الإجمالي بعد الخصم
        total = price * quantity * (1 - discount / 100)
        self.current_items[row]['total'] = total
        
        # تحديث الجدول
        self.items_table.item(row, 5).setText(f"{total:.2f}")
        
        self.update_totals()
    
    def remove_item(self, row):
        """حذف منتج من الفاتورة"""
        if row < 0 or row >= len(self.current_items):
            return
        
        # حذف العنصر من القائمة
        self.current_items.pop(row)
        
        # حذف الصف من الجدول
        self.items_table.removeRow(row)
        
        # تحديث الإجماليات
        self.update_totals()
    
    def update_totals(self):
        """تحديث إجماليات الفاتورة"""
        # حساب إجمالي المبلغ
        self.total_amount = sum(item['total'] for item in self.current_items)
        
        # الحصول على قيمة الخصم
        self.discount = self.discount_input.value()
        
        # الحصول على نسبة الضريبة
        tax_rate = self.tax_input.value()
        
        # حساب قيمة الضريبة
        subtotal = self.total_amount - self.discount
        if subtotal < 0:
            subtotal = 0
        
        self.tax = subtotal * (tax_rate / 100)
        
        # حساب المبلغ النهائي
        self.final_amount = subtotal + self.tax
        
        # تحديث العناصر
        self.total_label.setText(f"{self.total_amount:.2f}")
        self.final_label.setText(f"{self.final_amount:.2f}")
    
    def save_invoice(self):
        """حفظ الفاتورة"""
        if not self.current_items:
            QMessageBox.warning(self, "تنبيه", "لا توجد منتجات في الفاتورة")
            return
        
        try:
            # إنشاء فاتورة جديدة
            sale_data = {
                'customer_name': self.customer_name.text(),
                'customer_phone': self.customer_phone.text(),
                'total_amount': self.total_amount,
                'discount': self.discount,
                'tax': self.tax,
                'final_amount': self.final_amount,
                'payment_method': self.payment_method.currentText(),
                'status': 'completed'
            }
            
            # حفظ الفاتورة
            sale_id = self.sale_model.add_sale(sale_data)
            
            if not sale_id:
                raise Exception("فشل في حفظ الفاتورة")
            
            # حفظ عناصر الفاتورة
            for item in self.current_items:
                item_data = {
                    'sale_id': sale_id,
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'discount': item['discount'],
                    'total': item['total']
                }
                
                # حفظ عنصر الفاتورة
                self.sale_item_model.add_sale_item(**item_data)
                
                # تحديث المخزون
                self.product_model.update_stock(item['product_id'], -item['quantity'])
            
            QMessageBox.information(self, "نجاح", f"تم حفظ الفاتورة بنجاح. رقم الفاتورة: {sale_id}")
            
            # مسح الفاتورة الحالية
            self.clear_invoice()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ الفاتورة: {str(e)}")
    
    def clear_invoice(self):
        """مسح الفاتورة الحالية"""
        self.current_items = []
        self.items_table.setRowCount(0)
        self.customer_name.clear()
        self.customer_phone.clear()
        self.discount_input.setValue(0)
        self.tax_input.setValue(15)
        self.update_totals()