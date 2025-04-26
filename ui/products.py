from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QDialog, QFormLayout,
                            QDialogButtonBox, QTextEdit, QComboBox, QDoubleSpinBox,
                            QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from models.product import Product
from models.category import Category

class ProductDialog(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.product_data = product_data
        self.category_model = Category()
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("إضافة/تعديل منتج")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # نموذج البيانات
        form_layout = QFormLayout()
        
        self.barcode_input = QLineEdit()
        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        
        # قائمة الفئات
        self.category_combo = QComboBox()
        self.category_combo.addItem("بدون فئة", None)
        
        # تحميل الفئات
        categories = self.category_model.get_all_categories()
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])
        
        # أسعار وكميات
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0)
        self.price_input.setMaximum(999999.99)
        self.price_input.setDecimals(2)
        
        self.cost_price_input = QDoubleSpinBox()
        self.cost_price_input.setMinimum(0)
        self.cost_price_input.setMaximum(999999.99)
        self.cost_price_input.setDecimals(2)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(999999)
        
        self.min_quantity_input = QSpinBox()
        self.min_quantity_input.setMinimum(0)
        self.min_quantity_input.setMaximum(999999)
        self.min_quantity_input.setValue(5)  # قيمة افتراضية
        
        # إضافة الحقول إلى النموذج
        form_layout.addRow("الباركود:", self.barcode_input)
        form_layout.addRow("اسم المنتج:", self.name_input)
        form_layout.addRow("الوصف:", self.description_input)
        form_layout.addRow("الفئة:", self.category_combo)
        form_layout.addRow("سعر البيع:", self.price_input)
        form_layout.addRow("سعر التكلفة:", self.cost_price_input)
        form_layout.addRow("الكمية:", self.quantity_input)
        form_layout.addRow("الحد الأدنى للكمية:", self.min_quantity_input)
        
        layout.addLayout(form_layout)
        
        # أزرار الإجراءات
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        # إذا كانت هناك بيانات، قم بملء الحقول
        if self.product_data:
            self.barcode_input.setText(self.product_data.get('barcode', ''))
            self.name_input.setText(self.product_data['name'])
            self.description_input.setText(self.product_data.get('description', ''))
            
            # تحديد الفئة
            if self.product_data.get('category_id'):
                index = self.category_combo.findData(self.product_data['category_id'])
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)
            
            self.price_input.setValue(self.product_data['price'])
            self.cost_price_input.setValue(self.product_data['cost_price'])
            self.quantity_input.setValue(self.product_data['quantity'])
            self.min_quantity_input.setValue(self.product_data['min_quantity'])
    
    def get_product_data(self):
        """الحصول على بيانات المنتج من الحقول"""
        category_id = self.category_combo.currentData()
        
        return {
            'barcode': self.barcode_input.text(),
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText(),
            'category_id': category_id,
            'price': self.price_input.value(),
            'cost_price': self.cost_price_input.value(),
            'quantity': self.quantity_input.value(),
            'min_quantity': self.min_quantity_input.value()
        }


class ProductsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.product_model = Product()
        self.category_model = Category()
        
        self.setup_ui()
        self.load_products()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # عنوان الصفحة
        title_label = QLabel("إدارة المنتجات")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # قسم البحث والإضافة
        search_section = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن منتج...")
        self.search_input.textChanged.connect(self.load_products)
        
        add_btn = QPushButton("إضافة منتج جديد")
        add_btn.clicked.connect(self.add_product)
        
        search_section.addWidget(QLabel("البحث:"))
        search_section.addWidget(self.search_input)
        search_section.addWidget(add_btn)
        
        main_layout.addLayout(search_section)
        
        # جدول المنتجات
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels([
            "الباركود", "اسم المنتج", "الفئة", "سعر البيع", "سعر التكلفة",
            "الكمية", "الحد الأدنى", "تعديل", "حذف"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(self.products_table)
        
        # زر تحديث البيانات
        refresh_btn = QPushButton("تحديث البيانات")
        refresh_btn.clicked.connect(self.load_products)
        main_layout.addWidget(refresh_btn)
    
    def load_products(self):
        """تحميل المنتجات"""
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
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{product['cost_price']:.2f}"))
            
            # تلوين الكمية إذا كانت أقل من الحد الأدنى
            quantity_item = QTableWidgetItem(str(product['quantity']))
            if product['quantity'] <= product['min_quantity']:
                quantity_item.setBackground(Qt.red)
                quantity_item.setForeground(Qt.white)
            
            self.products_table.setItem(row, 5, quantity_item)
            self.products_table.setItem(row, 6, QTableWidgetItem(str(product['min_quantity'])))
            
            # أزرار التعديل والحذف
            edit_btn = QPushButton("تعديل")
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            delete_btn = QPushButton("حذف")
            delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            self.products_table.setCellWidget(row, 7, edit_btn)
            self.products_table.setCellWidget(row, 8, delete_btn)
    
    def add_product(self):
        """إضافة منتج جديد"""
        dialog = ProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            
            # التحقق من البيانات
            if not product_data['name']:
                QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم المنتج")
                return
            
            # إضافة المنتج
            result = self.product_model.add_product(product_data)
            
            if result:
                QMessageBox.information(self, "نجاح", "تمت إضافة المنتج بنجاح")
                self.load_products()
            else:
                QMessageBox.critical(self, "خطأ", "فشل في إضافة المنتج")
    
    def edit_product(self, product):
        """تعديل منتج"""
        dialog = ProductDialog(self, product)
        if dialog.exec_() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            
            # التحقق من البيانات
            if not product_data['name']:
                QMessageBox.warning(self, "تنبيه", "