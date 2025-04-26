from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QMessageBox,
                            QToolBar, QStatusBar, QLabel, QWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from ui.dashboard import DashboardWidget
from ui.products import ProductsWidget
from ui.categories import CategoriesWidget
from ui.sales import SalesWidget
from ui.reports import ReportsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام نقاط البيع")
        self.setMinimumSize(1024, 768)
        
        # إعداد واجهة المستخدم
        self.setup_ui()
        
    def setup_ui(self):
        # إنشاء شريط الأدوات
        self.toolbar = QToolBar("شريط الأدوات الرئيسي")
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        
        # إنشاء شريط الحالة
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # إضافة معلومات المستخدم إلى شريط الحالة
        self.user_label = QLabel("المستخدم: المدير")
        self.statusbar.addPermanentWidget(self.user_label)
        
        # إنشاء القائمة الرئيسية
        self.setup_menu()
        
        # إنشاء علامات التبويب
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        
        # إضافة علامات التبويب
        self.dashboard_widget = DashboardWidget(self)
        self.products_widget = ProductsWidget(self)
        self.categories_widget = CategoriesWidget(self)
        self.sales_widget = SalesWidget(self)
        self.reports_widget = ReportsWidget(self)
        
        self.tabs.addTab(self.dashboard_widget, "لوحة التحكم")
        self.tabs.addTab(self.sales_widget, "المبيعات")
        self.tabs.addTab(self.products_widget, "المنتجات")
        self.tabs.addTab(self.categories_widget, "الفئات")
        self.tabs.addTab(self.reports_widget, "التقارير")
        
        # تعيين علامات التبويب كعنصر مركزي
        self.setCentralWidget(self.tabs)
        
        # إضافة أزرار شريط الأدوات
        self.add_toolbar_buttons()
        
    def setup_menu(self):
        """إعداد القائمة الرئيسية"""
        # قائمة الملف
        file_menu = self.menuBar().addMenu("ملف")
        
        # إجراء الخروج
        exit_action = QAction("خروج", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # قائمة المساعدة
        help_menu = self.menuBar().addMenu("مساعدة")
        
        # إجراء حول
        about_action = QAction("حول البرنامج", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def add_toolbar_buttons(self):
        """إضافة أزرار شريط الأدوات"""
        # زر المبيعات
        sales_action = QAction("مبيعات جديدة", self)
        sales_action.triggered.connect(lambda: self.tabs.setCurrentIndex(1))
        self.toolbar.addAction(sales_action)
        
        # زر المنتجات
        products_action = QAction("المنتجات", self)
        products_action.triggered.connect(lambda: self.tabs.setCurrentIndex(2))
        self.toolbar.addAction(products_action)
        
        # زر التقارير
        reports_action = QAction("التقارير", self)
        reports_action.triggered.connect(lambda: self.tabs.setCurrentIndex(4))
        self.toolbar.addAction(reports_action)
        
        # فاصل
        self.toolbar.addSeparator()
        
        # زر الخروج
        exit_action = QAction("خروج", self)
        exit_action.triggered.connect(self.close)
        self.toolbar.addAction(exit_action)
        
    def show_about(self):
        """عرض معلومات حول البرنامج"""
        QMessageBox.about(self, "حول البرنامج",
                         "نظام نقاط البيع (POS)\n"
                         "الإصدار 1.0\n\n"
                         "تم تطويره باستخدام Python و PyQt5")

    def set_current_tab(self, index):
        """تغيير التبويب الحالي"""
        if 0 <= index < self.tabs.count():
            self.tabs.setCurrentIndex(index)