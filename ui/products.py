from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QDialog, QFormLayout,
                            QDialogButtonBox, QTextEdit, QComboBox, QDoubleSpinBox,
                            QSpinBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap

from models.product import Product
from models.category import Category

class ProductDialog(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.parent = parent
        self.product_data = product_data
        self.category_model = Category()
        self.init_ui()
        
    def init_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("إضافة/تعديل منتج")
        self.setMinimumWidth(500)
        
        layout = QFormLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # نموذج البيانات
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
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setMinimum(0)
        self.purchase_price_input.setMaximum(999999.99)
        self.purchase_price_input.setDecimals(2)
        
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setMinimum(0)
        self.selling_price_input.setMaximum(999999.99)
        self.selling_price_input.setDecimals(2)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(999999)
        
        self.min_quantity_input = QSpinBox()
        self.min_quantity_input.setMinimum(0)
        self.min_quantity_input.setMaximum(999999)
        self.min_quantity_input.setValue(5)  # قيمة افتراضية
        
        # إضافة الحقول إلى النموذج
        layout.addRow("الباركود:", self.barcode_input)
        layout.addRow("اسم المنتج:", self.name_input)
        layout.addRow("الوصف:", self.description_input)
        layout.addRow("الفئة:", self.category_combo)
        layout.addRow("سعر الشراء:", self.purchase_price_input)
        layout.addRow("سعر البيع:", self.selling_price_input)
        layout.addRow("الكمية:", self.quantity_input)
        layout.addRow("الحد الأدنى للكمية:", self.min_quantity_input)
        
        # إضافة الصورة
        image_layout = QHBoxLayout()
        self.image_path_input = QLineEdit()
        self.image_path_input.setReadOnly(True)
        image_button = QPushButton("اختر صورة")
        image_button.clicked.connect(self.browse_image)
        image_layout.addWidget(self.image_path_input)
        image_layout.addWidget(image_button)
        layout.addRow("الصورة:", image_layout)
        
        # أزرار الإجراءات
        button_layout = QHBoxLayout()
        save_button = QPushButton("حفظ")
        save_button.clicked.connect(self.save_product)
        cancel_button = QPushButton("إلغاء")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow("", button_layout)
        
        self.setLayout(layout)
        
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
            
            self.purchase_price_input.setValue(self.product_data['purchase_price'])
            self.selling_price_input.setValue(self.product_data['selling_price'])
            self.quantity_input.setValue(self.product_data['quantity'])
            self.min_quantity_input.setValue(self.product_data['min_quantity'])
            self.image_path_input.setText(self.product_data.get('image_path', ''))
    
    def get_product_data(self):
        """الحصول على بيانات المنتج من الحقول"""
        category_id = self.category_combo.currentData()
        
        return {
            'barcode': self.barcode_input.text(),
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText(),
            'category_id': category_id,
            'purchase_price': self.purchase_price_input.value(),
            'selling_price': self.selling_price_input.value(),
            'quantity': self.quantity_input.value(),
            'min_quantity': self.min_quantity_input.value(),
            'image_path': self.image_path_input.text()
        }

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'اختر صورة', '',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        if file_name:
            self.image_path_input.setText(file_name)

    def save_product(self):
        """حفظ المنتج"""
        # التحقق من البيانات
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم المنتج")
            return
        
        if self.selling_price_input.value() <= 0:
            QMessageBox.warning(self, "تنبيه", "سعر البيع يجب أن يكون أكبر من 0")
            return

        # إعداد بيانات المنتج
        product_data = self.get_product_data()
        
        if self.parent.parent.db_manager.connect():
            if self.product_data:  # تحديث منتج موجود
                product_data['id'] = self.product_data['id']
                success = self.parent.parent.db_manager.update_product(product_data)
            else:  # إضافة منتج جديد
                success = self.parent.parent.db_manager.add_product(product_data)
            
            self.parent.parent.db_manager.disconnect()
            
            if success:
                QMessageBox.information(self, "نجاح", "تمت إضافة المنتج بنجاح")
                self.accept()
            else:
                QMessageBox.critical(self, "خطأ", "فشل في حفظ المنتج")


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
            "الباركود", "اسم المنتج", "الفئة", "سعر الشراء", "سعر البيع",
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
            self.products_table.setItem(row, 3, QTableWidgetItem(f"{product['purchase_price']:.2f}"))
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{product['selling_price']:.2f}"))
            
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
                QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم المنتج")
                return
            
            # تحديث المنتج
            result = self.product_model.update_product(product_data)
            
            if result:
                QMessageBox.information(self, "نجاح", "تم تحديث المنتج بنجاح")
                self.load_products()
            else:
                QMessageBox.critical(self, "خطأ", "فشل في تحديث المنتج")
    
    def delete_product(self, product):
        """حذف منتج"""
        reply = QMessageBox.question(
            self, 'تأكيد الحذف',
            f"هل أنت متأكد أنك تريد حذف المنتج '{product['name']}'؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.parent.parent.db_manager.connect():
                if self.parent.parent.db_manager.delete_product(product['id']):
                    self.load_products()
                else:
                    QMessageBox.warning(self, 'خطأ', 'فشل في حذف المنتج')
                self.parent.parent.db_manager.disconnect()