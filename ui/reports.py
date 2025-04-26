from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                            QComboBox, QDateEdit, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

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
            "تقرير المبيعات", 
            "تقرير المنتجات الأكثر مبيعاً", 
            "تقرير المخزون"
        ])
        self.report_type.currentIndexChanged.connect(self.change_report_type)
        
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
        
        # تهيئة التقرير الافتراضي
        self.change_report_type(0)
    
    def change_report_type(self, index):
        """تغيير نوع التقرير"""
        if index == 0:  # تقرير المبيعات
            self.report_table.setColumnCount(7)
            self.report_table.setHorizontalHeaderLabels([
                "رقم الفاتورة", "التاريخ", "العميل", "الإجمالي", 
                "الخصم", "الضريبة", "المبلغ النهائي"
            ])
            self.product_combo.setEnabled(False)
        
        elif index == 1:  # تقرير المنتجات الأكثر مبيعاً
            self.report_table.setColumnCount(5)
            self.report_table.setHorizontalHeaderLabels([
                "المنتج", "الباركود", "الكمية المباعة", 
                "إجمالي المبيعات", "عدد الفواتير"
            ])
            self.product_combo.setEnabled(True)
        
        elif index == 2:  # تقرير المخزون
            self.report_table.setColumnCount(5)
            self.report_table.setHorizontalHeaderLabels([
                "المنتج", "الباركود", "الكمية المتوفرة", 
                "الحد الأدنى", "الحالة"
            ])
            self.product_combo.setEnabled(True)
    
    def generate_report(self):
        """إنشاء التقرير"""
        report_type = self.report_type.currentIndex()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        product_id = self.product_combo.currentData()
        
        self.report_table.setRowCount(0)
        
        try:
            if report_type == 0:  # تقرير المبيعات
                self.generate_sales_report(start_date, end_date)
            
            elif report_type == 1:  # تقرير المنتجات الأكثر مبيعاً
                self.generate_top_products_report(start_date, end_date, product_id)
            
            elif report_type == 2:  # تقرير المخزون
                self.generate_stock_report(product_id)
        
        except Exception as e:
            print(f"خطأ في إنشاء التقرير: {e}")
    
    def generate_sales_report(self, start_date, end_date):
        """إنشاء تقرير المبيعات"""
        sales = self.sale_model.get_sales_by_date_range(start_date, end_date)
        
        for row, sale in enumerate(sales):
            self.report_table.insertRow(row)
            
            self.report_table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
            self.report_table.setItem(row, 1, QTableWidgetItem(sale['date']))
            self.report_table.setItem(row, 2, QTableWidgetItem(sale.get('customer_name', '')))
            self.report_table.setItem(row, 3, QTableWidgetItem(f"{sale['total_amount']:.2f}"))
            self.report_table.setItem(row, 4, QTableWidgetItem(f"{sale['discount']:.2f}"))
            self.report_table.setItem(row, 5, QTableWidgetItem(f"{sale['tax']:.2f}"))
            self.report_table.setItem(row, 6, QTableWidgetItem(f"{sale['final_amount']:.2f}"))
    
    def generate_top_products_report(self, start_date, end_date, product_id):
        """إنشاء تقرير المنتجات الأكثر مبيعاً"""
        # هذه الدالة تحتاج إلى استعلام معقد نوعاً ما
        # يمكن تنفيذها في نموذج SaleItem
        items = self.sale_item_model.get_sale_items_report(start_date, end_date, product_id)
        
        # تجميع البيانات حسب المنتج
        product_stats = {}
        for item in items:
            if item['product_id'] not in product_stats:
                product_stats[item['product_id']] = {
                    'name': item['product_name'],
                    'barcode': item.get('barcode', ''),
                    'quantity': 0,
                    'total': 0,
                    'invoices': set()
                }
            
            product_stats[item['product_id']]['quantity'] += item['quantity']
            product_stats[item['product_id']]['total'] += item['total']
            product_stats[item['product_id']]['invoices'].add(item['sale_id'])
        
        # ترتيب المنتجات حسب الكمية المباعة
        sorted_products = sorted(
            product_stats.values(), 
            key=lambda x: x['quantity'], 
            reverse=True
        )
        
        for row, product in enumerate(sorted_products):
            self.report_table.insertRow(row)
            
            self.report_table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.report_table.setItem(row, 1, QTableWidgetItem(product['barcode']))
            self.report_table.setItem(row, 2, QTableWidgetItem(str(product['quantity'])))
            self.report_table.setItem(row, 3, QTableWidgetItem(f"{product['total']:.2f}"))
            self.report_table.setItem(row, 4, QTableWidgetItem(str(len(product['invoices']))))
    
    def generate_stock_report(self, product_id):
        """إنشاء تقرير المخزون"""
        products = []
        
        if product_id:
            product = self.product_model.get_product_by_id(product_id)
            if product:
                products = [product]
        else:
            products = self.product_model.get_all_products()
        
        for row, product in enumerate(products):
            self.report_table.insertRow(row)
            
            self.report_table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.report_table.setItem(row, 1, QTableWidgetItem(product.get('barcode', '')))
            
            quantity_item = QTableWidgetItem(str(product['quantity']))
            if product['quantity'] <= product['min_quantity']:
                quantity_item.setBackground(Qt.red)
                quantity_item.setForeground(Qt.white)
            
            self.report_table.setItem(row, 2, quantity_item)
            self.report_table.setItem(row, 3, QTableWidgetItem(str(product['min_quantity'])))
            
            status = "متوفر"
            if product['quantity'] <= 0:
                status = "غير متوفر"
            elif product['quantity'] <= product['min_quantity']:
                status = "منخفض"
            
            self.report_table.setItem(row, 4, QTableWidgetItem(status))
    
    def print_report(self):
        """طباعة التقرير"""
        # هذه الدالة يمكن تنفيذها لاحقاً
        # تحتاج إلى استخدام QPrinter و QPainter
        pass