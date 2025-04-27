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


class SaleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('New Sale')
        self.setMinimumWidth(800)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Customer info
        customer_frame = QFormLayout()
        
        self.customer_name = QLineEdit()
        customer_frame.addRow('Customer Name:', self.customer_name)
        
        self.customer_phone = QLineEdit()
        customer_frame.addRow('Phone:', self.customer_phone)
        
        layout.addLayout(customer_frame)

        # Product selection
        product_layout = QHBoxLayout()
        
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText('Scan barcode or enter product code')
        self.barcode_input.returnPressed.connect(self.add_product_by_barcode)
        product_layout.addWidget(self.barcode_input)
        
        self.product_combo = QComboBox()
        self.load_products()
        product_layout.addWidget(self.product_combo)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(9999)
        self.quantity_input.setValue(1)
        product_layout.addWidget(self.quantity_input)
        
        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_product)
        product_layout.addWidget(add_button)
        
        layout.addLayout(product_layout)

        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels([
            'Product', 'Price', 'Quantity', 'Total', 'Stock', 'Remove'
        ])
        self.items_table.verticalHeader().setVisible(False)
        layout.addWidget(self.items_table)

        # Totals
        totals_layout = QFormLayout()
        
        self.subtotal_label = QLabel('0.00')
        totals_layout.addRow('Subtotal:', self.subtotal_label)
        
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setMaximum(9999999.99)
        self.discount_input.valueChanged.connect(self.calculate_total)
        totals_layout.addRow('Discount:', self.discount_input)
        
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setMaximum(100)
        self.tax_input.setValue(15)  # Default tax rate
        self.tax_input.valueChanged.connect(self.calculate_total)
        totals_layout.addRow('Tax (%):', self.tax_input)
        
        self.total_label = QLabel('0.00')
        totals_layout.addRow('Total:', self.total_label)
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(['Cash', 'Card', 'Other'])
        totals_layout.addRow('Payment Method:', self.payment_method)
        
        layout.addLayout(totals_layout)

        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('Complete Sale')
        save_button.clicked.connect(self.complete_sale)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_products(self):
        if self.parent.parent.db_manager.connect():
            products = self.parent.parent.db_manager.get_products()
            self.parent.parent.db_manager.disconnect()
            
            self.product_combo.clear()
            for product in products:
                self.product_combo.addItem(product['name'], product)

    def add_product_by_barcode(self):
        barcode = self.barcode_input.text().strip()
        if not barcode:
            return
            
        if self.parent.parent.db_manager.connect():
            product = self.parent.parent.db_manager.get_product_by_barcode(barcode)
            self.parent.parent.db_manager.disconnect()
            
            if product:
                self.add_product_to_table(product)
                self.barcode_input.clear()
            else:
                QMessageBox.warning(self, 'Error', 'Product not found')

    def add_product(self):
        product = self.product_combo.currentData()
        if product:
            self.add_product_to_table(product)

    def add_product_to_table(self, product):
        quantity = self.quantity_input.value()
        
        if quantity > product['quantity']:
            QMessageBox.warning(self, 'Error', 'Insufficient stock')
            return
            
        # Check if product already in table
        for row in range(self.items_table.rowCount()):
            if self.items_table.item(row, 0).data(Qt.UserRole)['id'] == product['id']:
                current_qty = int(self.items_table.item(row, 2).text())
                new_qty = current_qty + quantity
                
                if new_qty > product['quantity']:
                    QMessageBox.warning(self, 'Error', 'Insufficient stock')
                    return
                    
                self.items_table.item(row, 2).setText(str(new_qty))
                self.items_table.item(row, 3).setText(f"{new_qty * product['selling_price']:.2f}")
                self.calculate_total()
                return

        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        
        # Product name
        name_item = QTableWidgetItem(product['name'])
        name_item.setData(Qt.UserRole, product)
        self.items_table.setItem(row, 0, name_item)
        
        # Price
        self.items_table.setItem(row, 1, QTableWidgetItem(f"{product['selling_price']:.2f}"))
        
        # Quantity
        self.items_table.setItem(row, 2, QTableWidgetItem(str(quantity)))
        
        # Total
        total = quantity * product['selling_price']
        self.items_table.setItem(row, 3, QTableWidgetItem(f"{total:.2f}"))
        
        # Stock
        self.items_table.setItem(row, 4, QTableWidgetItem(str(product['quantity'])))
        
        # Remove button
        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(lambda: self.remove_item(row))
        self.items_table.setCellWidget(row, 5, remove_button)
        
        self.calculate_total()

    def remove_item(self, row):
        self.items_table.removeRow(row)
        self.calculate_total()

    def calculate_total(self):
        subtotal = 0
        for row in range(self.items_table.rowCount()):
            subtotal += float(self.items_table.item(row, 3).text())
        
        self.subtotal_label.setText(f"{subtotal:.2f}")
        
        discount = self.discount_input.value()
        tax = subtotal * (self.tax_input.value() / 100)
        
        total = subtotal - discount + tax
        self.total_label.setText(f"{total:.2f}")

    def complete_sale(self):
        if self.items_table.rowCount() == 0:
            QMessageBox.warning(self, 'Error', 'No items in sale')
            return

        # Prepare sale data
        sale_data = {
            'invoice_number': str(uuid.uuid4())[:8].upper(),
            'customer_name': self.customer_name.text().strip(),
            'customer_phone': self.customer_phone.text().strip(),
            'total_amount': float(self.subtotal_label.text()),
            'discount': self.discount_input.value(),
            'tax': float(self.subtotal_label.text()) * (self.tax_input.value() / 100),
            'final_amount': float(self.total_label.text()),
            'payment_method': self.payment_method.currentText(),
            'user_id': self.parent.parent.current_user['id']
        }

        # Prepare items data
        items = []
        for row in range(self.items_table.rowCount()):
            product = self.items_table.item(row, 0).data(Qt.UserRole)
            quantity = int(self.items_table.item(row, 2).text())
            unit_price = float(self.items_table.item(row, 1).text())
            
            items.append({
                'product_id': product['id'],
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': quantity * unit_price
            })

        if self.parent.parent.db_manager.connect():
            # Create sale
            sale_id = self.parent.parent.db_manager.create_sale(sale_data)
            if sale_id:
                # Add sale items
                if self.parent.parent.db_manager.add_sale_items(sale_id, items):
                    QMessageBox.information(self, 'Success', 'Sale completed successfully')
                    self.accept()
                else:
                    QMessageBox.critical(self, 'Error', 'Failed to add sale items')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to create sale')
            
            self.parent.parent.db_manager.disconnect()


class SalesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Toolbar
        toolbar = QHBoxLayout()
        
        new_sale_button = QPushButton('New Sale')
        new_sale_button.clicked.connect(self.new_sale)
        toolbar.addWidget(new_sale_button)
        
        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.load_sales)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Sales table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'Invoice', 'Customer', 'Total', 'Discount', 'Tax',
            'Final Amount', 'Payment', 'Date'
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.setLayout(layout)
        
        # Load initial data
        self.load_sales()

    def load_sales(self):
        if self.parent.db_manager.connect():
            sales = self.parent.db_manager.get_sales()
            self.parent.db_manager.disconnect()
            
            self.table.setRowCount(len(sales))
            
            for i, sale in enumerate(sales):
                self.table.setItem(i, 0, QTableWidgetItem(sale['invoice_number']))
                self.table.setItem(i, 1, QTableWidgetItem(sale['customer_name'] or '-'))
                self.table.setItem(i, 2, QTableWidgetItem(f"{sale['total_amount']:.2f}"))
                self.table.setItem(i, 3, QTableWidgetItem(f"{sale['discount']:.2f}"))
                self.table.setItem(i, 4, QTableWidgetItem(f"{sale['tax']:.2f}"))
                self.table.setItem(i, 5, QTableWidgetItem(f"{sale['final_amount']:.2f}"))
                self.table.setItem(i, 6, QTableWidgetItem(sale['payment_method']))
                self.table.setItem(i, 7, QTableWidgetItem(str(sale['created_at'])))

    def new_sale(self):
        dialog = SaleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_sales()