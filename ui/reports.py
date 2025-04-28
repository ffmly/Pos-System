from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                            QComboBox, QDateEdit, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta

from models.sale import Sale
from models.product import Product
from models.sale_item import SaleItem

class ReportsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.sale_model = Sale()
        self.product_model = Product()
        self.sale_item_model = SaleItem()
        
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # عنوان الصفحة
        title_label = QLabel("التقارير")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # مجموعة خيارات التقرير
        options_group = QGroupBox("خيارات التقرير")
        options_layout = QFormLayout()
        
        # نوع التقرير
        self.report_type = QComboBox()
        self.report_type.addItems([
            'Sales Report',
            'Products Report',
            'Low Stock Report',
            'Categories Report'
        ])
        self.report_type.currentIndexChanged.connect(self.load_report)
        
        # تاريخ البداية
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        
        # تاريخ النهاية
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        
        # المنتج (للتقارير المتعلقة بالمنتجات)
        self.product_combo = QComboBox()
        self.product_combo.addItem("كل المنتجات", None)
        
        # تحميل المنتجات
        products = self.product_model.get_all_products()
        for product in products:
            self.product_combo.addItem(product['name'], product['id'])
        
        options_layout.addRow("نوع التقرير:", self.report_type)
        options_layout.addRow("من تاريخ:", self.start_date)
        options_layout.addRow("إلى تاريخ:", self.end_date)
        options_layout.addRow("المنتج:", self.product_combo)
        
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)
        
        # أزرار الإجراءات
        actions_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("إنشاء التقرير")
        self.generate_btn.clicked.connect(self.generate_report)
        
        self.print_btn = QPushButton("طباعة")
        self.print_btn.clicked.connect(self.print_report)
        
        actions_layout.addWidget(self.generate_btn)
        actions_layout.addWidget(self.print_btn)
        
        main_layout.addLayout(actions_layout)
        
        # جدول التقرير
        self.report_table = QTableWidget()
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(self.report_table)
        
        # ملخص التقرير
        self.summary_label = QLabel()
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setStyleSheet('''
            QLabel {
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 5px;
                margin: 10px;
            }
        ''')
        main_layout.addWidget(self.summary_label)
        
        # تهيئة التقرير الافتراضي
        self.load_report()
    
    def load_report(self):
        report_type = self.report_type.currentText()
        
        if report_type == 'Sales Report':
            self.load_sales_report()
        elif report_type == 'Products Report':
            self.load_products_report()
        elif report_type == 'Low Stock Report':
            self.load_low_stock_report()
        elif report_type == 'Categories Report':
            self.load_categories_report()
    
    def load_sales_report(self):
        self.report_table.setRowCount(0)
        self.report_table.setColumnCount(8)
        self.report_table.setHorizontalHeaderLabels([
            'Date', 'Invoice', 'Customer', 'Items', 'Total', 'Discount', 'Tax', 'Final'
        ])
        
        if self.parent.db_manager.connect():
            start_date = self.start_date.date().toString(Qt.ISODate)
            end_date = self.end_date.date().toString(Qt.ISODate)
            
            # Get sales data
            sales = self.parent.db_manager.get_sales(start_date, end_date)
            
            self.report_table.setRowCount(len(sales))
            
            total_sales = 0
            total_items = 0
            total_discount = 0
            total_tax = 0
            
            for i, sale in enumerate(sales):
                # Get sale items
                items = self.parent.db_manager.get_sale_items(sale['id'])
                items_count = sum(item['quantity'] for item in items)
                
                self.report_table.insertRow(i)
                
                self.report_table.setItem(i, 0, QTableWidgetItem(str(sale['created_at'])))
                self.report_table.setItem(i, 1, QTableWidgetItem(sale['invoice_number']))
                self.report_table.setItem(i, 2, QTableWidgetItem(sale['customer_name'] or '-'))
                self.report_table.setItem(i, 3, QTableWidgetItem(str(items_count)))
                self.report_table.setItem(i, 4, QTableWidgetItem(f"{sale['total_amount']:.2f}"))
                self.report_table.setItem(i, 5, QTableWidgetItem(f"{sale['discount']:.2f}"))
                self.report_table.setItem(i, 6, QTableWidgetItem(f"{sale['tax']:.2f}"))
                self.report_table.setItem(i, 7, QTableWidgetItem(f"{sale['final_amount']:.2f}"))
                
                total_sales += sale['final_amount']
                total_items += items_count
                total_discount += sale['discount']
                total_tax += sale['tax']
            
            self.parent.db_manager.disconnect()
            
            # Update summary
            summary = f"""
                <h3>Sales Summary</h3>
                <p>
                    Period: {start_date} to {end_date}<br>
                    Total Sales: {total_sales:.2f}<br>
                    Total Items Sold: {total_items}<br>
                    Total Discounts: {total_discount:.2f}<br>
                    Total Tax: {total_tax:.2f}
                </p>
            """
            self.summary_label.setText(summary)
    
    def load_products_report(self):
        self.report_table.setRowCount(0)
        self.report_table.setColumnCount(7)
        self.report_table.setHorizontalHeaderLabels([
            'Product', 'Category', 'Cost', 'Price', 'Stock', 'Min Stock', 'Value'
        ])
        
        if self.parent.db_manager.connect():
            products = self.parent.db_manager.get_products()
            
            self.report_table.setRowCount(len(products))
            
            total_value = 0
            total_items = 0
            
            for i, product in enumerate(products):
                self.report_table.insertRow(i)
                
                self.report_table.setItem(i, 0, QTableWidgetItem(product['name']))
                self.report_table.setItem(i, 1, QTableWidgetItem(self.get_category_name(product['category_id'])))
                self.report_table.setItem(i, 2, QTableWidgetItem(f"{product['purchase_price']:.2f}"))
                self.report_table.setItem(i, 3, QTableWidgetItem(f"{product['selling_price']:.2f}"))
                self.report_table.setItem(i, 4, QTableWidgetItem(str(product['quantity'])))
                self.report_table.setItem(i, 5, QTableWidgetItem(str(product['min_quantity'])))
                
                value = product['quantity'] * product['purchase_price']
                self.report_table.setItem(i, 6, QTableWidgetItem(f"{value:.2f}"))
                
                total_value += value
                total_items += product['quantity']
            
            self.parent.db_manager.disconnect()
            
            # Update summary
            summary = f"""
                <h3>Products Summary</h3>
                <p>
                    Total Products: {len(products)}<br>
                    Total Items in Stock: {total_items}<br>
                    Total Stock Value: {total_value:.2f}
                </p>
            """
            self.summary_label.setText(summary)
    
    def load_low_stock_report(self):
        self.report_table.setRowCount(0)
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels([
            'Product', 'Category', 'Stock', 'Min Stock', 'Status'
        ])
        
        if self.parent.db_manager.connect():
            products = self.parent.db_manager.get_products()
            low_stock_products = [p for p in products if p['quantity'] <= p['min_quantity']]
            
            self.report_table.setRowCount(len(low_stock_products))
            
            for i, product in enumerate(low_stock_products):
                self.report_table.insertRow(i)
                
                self.report_table.setItem(i, 0, QTableWidgetItem(product['name']))
                self.report_table.setItem(i, 1, QTableWidgetItem(self.get_category_name(product['category_id'])))
                self.report_table.setItem(i, 2, QTableWidgetItem(str(product['quantity'])))
                self.report_table.setItem(i, 3, QTableWidgetItem(str(product['min_quantity'])))
                
                status = 'Out of Stock' if product['quantity'] == 0 else 'Low Stock'
                status_item = QTableWidgetItem(status)
                status_item.setForeground(Qt.red)
                self.report_table.setItem(i, 4, status_item)
            
            self.parent.db_manager.disconnect()
            
            # Update summary
            summary = f"""
                <h3>Low Stock Summary</h3>
                <p>
                    Total Low Stock Items: {len(low_stock_products)}<br>
                    Out of Stock Items: {len([p for p in low_stock_products if p['quantity'] == 0])}
                </p>
            """
            self.summary_label.setText(summary)
    
    def load_categories_report(self):
        self.report_table.setRowCount(0)
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels([
            'Category', 'Products', 'Total Stock', 'Total Value'
        ])
        
        if self.parent.db_manager.connect():
            categories = self.parent.db_manager.get_categories()
            
            self.report_table.setRowCount(len(categories))
            
            total_products = 0
            total_stock = 0
            total_value = 0
            
            for i, category in enumerate(categories):
                # Get products in this category
                products = self.parent.db_manager.get_products(category['id'])
                products_count = len(products)
                stock_count = sum(p['quantity'] for p in products)
                stock_value = sum(p['quantity'] * p['purchase_price'] for p in products)
                
                self.report_table.insertRow(i)
                
                self.report_table.setItem(i, 0, QTableWidgetItem(category['name']))
                self.report_table.setItem(i, 1, QTableWidgetItem(str(products_count)))
                self.report_table.setItem(i, 2, QTableWidgetItem(str(stock_count)))
                self.report_table.setItem(i, 3, QTableWidgetItem(f"{stock_value:.2f}"))
                
                total_products += products_count
                total_stock += stock_count
                total_value += stock_value
            
            self.parent.db_manager.disconnect()
            
            # Update summary
            summary = f"""
                <h3>Categories Summary</h3>
                <p>
                    Total Categories: {len(categories)}<br>
                    Total Products: {total_products}<br>
                    Total Stock: {total_stock}<br>
                    Total Value: {total_value:.2f}
                </p>
            """
            self.summary_label.setText(summary)
    
    def get_category_name(self, category_id):
        """Get category name by ID"""
        if self.parent.db_manager.connect():
            category = self.parent.db_manager.fetch_one(
                "SELECT name FROM categories WHERE id = ?",
                (category_id,)
            )
            self.parent.db_manager.disconnect()
            return category['name'] if category else 'Unknown'
        return 'Unknown'
    
    def generate_report(self):
        """Generate report based on current settings"""
        report_type = self.report_type.currentText()
        start_date = self.start_date.date().toString(Qt.ISODate)
        end_date = self.end_date.date().toString(Qt.ISODate)
        product_id = self.product_combo.currentData()
        
        if report_type == 'Sales Report':
            self.generate_sales_report(start_date, end_date)
        elif report_type == 'Products Report':
            self.generate_stock_report(product_id)
        elif report_type == 'Low Stock Report':
            self.generate_low_stock_report()
        elif report_type == 'Categories Report':
            self.generate_categories_report()
    
    def generate_sales_report(self, start_date, end_date):
        """Generate sales report"""
        # Implementation will be added later
        pass
    
    def generate_stock_report(self, product_id):
        """Generate stock report"""
        # Implementation will be added later
        pass
    
    def generate_low_stock_report(self):
        """Generate low stock report"""
        # Implementation will be added later
        pass
    
    def generate_categories_report(self):
        """Generate categories report"""
        # Implementation will be added later
        pass
    
    def print_report(self):
        """Print current report"""
        # Implementation will be added later
        pass