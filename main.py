import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui.dashboard import DashboardWidget
from ui.sales import SalesWidget
from ui.products import ProductsWidget
from ui.categories import CategoriesWidget
from ui.reports import ReportsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام نقاط البيع")
        self.setMinimumSize(1200, 800)
        
        # إنشاء التبويبات
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # إضافة صفحات التطبيق
        self.dashboard = DashboardWidget(self)
        self.sales = SalesWidget(self)
        self.products = ProductsWidget(self)
        self.categories = CategoriesWidget(self)
        self.reports = ReportsWidget(self)
        
        # إضافة التبويبات
        self.tabs.addTab(self.dashboard, "لوحة التحكم")
        self.tabs.addTab(self.sales, "المبيعات")
        self.tabs.addTab(self.products, "المنتجات")
        self.tabs.addTab(self.categories, "الفئات")
        self.tabs.addTab(self.reports, "التقارير")
        
        # تعيين اتجاه النص من اليمين إلى اليسار
        self.setLayoutDirection(Qt.RightToLeft)
    
    def set_current_tab(self, index):
        """تغيير التبويب الحالي"""
        if 0 <= index < self.tabs.count():
            self.tabs.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # تعيين اتجاه النص من اليمين إلى اليسار للتطبيق بأكمله
    app.setLayoutDirection(Qt.RightToLeft)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())