import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from database.db_manager import DatabaseManager
from ui.login import LoginWindow
from ui.dashboard import DashboardWidget
from ui.sales import SalesWidget
from ui.products import ProductsWidget
from ui.categories import CategoriesWidget
from ui.reports import ReportsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.init_ui()
        self.show_login()

    def init_ui(self):
        self.setWindowTitle("Point of Sale System")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Initialize tab widgets
        self.dashboard = DashboardWidget(self)
        self.sales = SalesWidget(self)
        self.products = ProductsWidget(self)
        self.categories = CategoriesWidget(self)
        self.reports = ReportsWidget(self)
        
        # Add tabs
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.sales, "Sales")
        self.tabs.addTab(self.products, "Products")
        self.tabs.addTab(self.categories, "Categories")
        self.tabs.addTab(self.reports, "Reports")
        
        # Set window style
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background-color: #e0e0e0;
            }
        ''')

    def show_login(self):
        self.login_window = LoginWindow(self.db_manager)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.show()

    def on_login_successful(self, user_data):
        self.current_user = user_data
        self.show()
        self.update_ui_for_user()

    def update_ui_for_user(self):
        # Update UI based on user role
        if self.current_user['role'] != 'admin':
            # Hide admin-only tabs
            self.tabs.removeTab(self.tabs.indexOf(self.reports))
            self.tabs.removeTab(self.tabs.indexOf(self.categories))

    def set_current_tab(self, index):
        """Change current tab"""
        if 0 <= index < self.tabs.count():
            self.tabs.setCurrentIndex(index)

    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self, 'Confirm Exit',
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    
    sys.exit(app.exec_())