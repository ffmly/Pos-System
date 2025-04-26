from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

from models.product import Product
from models.sale import Sale

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.product_model = Product()
        self.sale_model = Sale()
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # عنوان لوحة التحكم
        title_label = QLabel("لوحة التحكم")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # بطاقات الإحصائيات
        stats_layout = QHBoxLayout()
        
        # بطاقة إجمالي المبيعات اليوم
        self.today_sales_card = self.create_stat_card("إجمالي مبيعات اليوم", "0.00", "ر.س")
        stats_layout.addWidget(self.today_sales_card)
        
        # بطاقة عدد الفواتير اليوم
        self.today_invoices_card = self.create_stat_card("عدد الفواتير اليوم", "0", "فاتورة")
        stats_layout.addWidget(self.today_invoices_card)
        
        # بطاقة إجمالي المنتجات
        self.total_products_card = self.create_stat_card("إجمالي المنتجات", "0", "منتج")
        stats_layout.addWidget(self.total_products_card)
        
        # بطاقة المنتجات منخفضة المخزون
        self.low_stock_card = self.create_stat_card("منتجات منخفضة المخزون", "0", "منتج")
        stats_layout.addWidget(self.low_stock_card)
        
        main_layout.addLayout(stats_layout)
        
        # أزرار الوصول السريع
        shortcuts_layout = QGridLayout()
        
        # زر المبيعات الجديدة
        new_sale_btn = self.create_shortcut_button("مبيعات جديدة", self.open_sales_tab)
        shortcuts_layout.addWidget(new_sale_btn, 0, 0)
        
        # زر إضافة منتج
        add_product_btn = self.create_shortcut_button("إضافة منتج", self.open_products_tab)
        shortcuts_layout.addWidget(add_product_btn, 0, 1)
        
        # زر التقارير
        reports_btn = self.create_shortcut_button("التقارير", self.open_reports_tab)
        shortcuts_layout.addWidget(reports_btn, 0, 2)
        
        # زر المنتجات منخفضة المخزون
        low_stock_btn = self.create_shortcut_button("المنتجات منخفضة المخزون", self.show_low_stock)
        shortcuts_layout.addWidget(low_stock_btn, 1, 0)
        
        # زر الفئات
        categories_btn = self.create_shortcut_button("إدارة الفئات", self.open_categories_tab)
        shortcuts_layout.addWidget(categories_btn, 1, 1)
        
        # زر تحديث البيانات
        refresh_btn = self.create_shortcut_button("تحديث البيانات", self.load_data)
        shortcuts_layout.addWidget(refresh_btn, 1, 2)
        
        main_layout.addLayout(shortcuts_layout)
        
        # إضافة مساحة فارغة
        main_layout.addStretch()
    
    def create_stat_card(self, title, value, unit):
        """إنشاء بطاقة إحصائية"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #f5f5f5; border-radius: 8px;")
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        
        unit_label = QLabel(unit)
        unit_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(unit_label)
        
        # حفظ مرجع لعنصر القيمة للتحديث لاحقًا
        card.value_label = value_label
        
        return card
    
    def create_shortcut_button(self, text, callback):
        """إنشاء زر وصول سريع"""
        button = QPushButton(text)
        button.setMinimumHeight(80)
        button.clicked.connect(callback)
        return button
    
    def load_data(self):
        """تحميل البيانات وتحديث الإحصائيات"""
        try:
            # إحصائيات المبيعات اليومية
            today_sales = self.sale_model.get_today_sales_stats()
            if today_sales:
                self.today_sales_card.value_label.setText(f"{today_sales['total_amount']:.2f}")
                self.today_invoices_card.value_label.setText(str(today_sales['count']))
            
            # إجمالي المنتجات
            products = self.product_model.get_all_products()
            self.total_products_card.value_label.setText(str(len(products)))
            
            # المنتجات منخفضة المخزون
            low_stock = self.product_model.get_low_stock_products()
            self.low_stock_card.value_label.setText(str(len(low_stock)))
            
        except Exception as e:
            print(f"خطأ في تحميل البيانات: {e}")
    
    def open_sales_tab(self):
        """فتح صفحة المبيعات"""
        if self.parent:
            self.parent.set_current_tab(1)  # افتراض أن صفحة المبيعات هي التبويب رقم 1
    
    def open_products_tab(self):
        """فتح صفحة المنتجات"""
        if self.parent:
            self.parent.set_current_tab(2)  # افتراض أن صفحة المنتجات هي التبويب رقم 2
    
    def open_reports_tab(self):
        """فتح صفحة التقارير"""
        if self.parent:
            self.parent.set_current_tab(4)  # افتراض أن صفحة التقارير هي التبويب رقم 4
    
    def open_categories_tab(self):
        """فتح صفحة الفئات"""
        if self.parent:
            self.parent.set_current_tab(3)  # افتراض أن صفحة الفئات هي التبويب رقم 3
    
    def show_low_stock(self):
        """عرض المنتجات منخفضة المخزون"""
        if self.parent:
            self.parent.set_current_tab(2)  # افتراض أن صفحة المنتجات هي التبويب رقم