import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QMessageBox, 
                           QWidget, QVBoxLayout, QMenuBar, QMenu, QAction, 
                           QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from database.db_manager import DatabaseManager
from ui.login import LoginWindow
from ui.dashboard import DashboardWidget
from ui.sales import SalesWidget
from ui.products import ProductsWidget
from ui.categories import CategoriesWidget
from ui.reports import ReportsWidget
from utils.notifications import NotificationSystem
from utils.styles import MAIN_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.notifications = NotificationSystem(self)
        self.init_ui()
        self.hide()  # Hide the main window initially
        self.show_login()

    def init_ui(self):
        self.setWindowTitle("Point of Sale System")
        self.setMinimumSize(1200, 800)
        
        # Set window icon
        self.setWindowIcon(QIcon("resources/images/pos_icon.png"))
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Initialize tab widgets with icons
        self.dashboard = DashboardWidget(self)
        self.sales = SalesWidget(self)
        self.products = ProductsWidget(self)
        self.categories = CategoriesWidget(self)
        self.reports = ReportsWidget(self)
        
        # Add tabs with icons
        self.tabs.addTab(self.dashboard, QIcon("resources/images/dashboard.png"), "Dashboard")
        self.tabs.addTab(self.sales, QIcon("resources/images/sales.png"), "Sales")
        self.tabs.addTab(self.products, QIcon("resources/images/products.png"), "Products")
        self.tabs.addTab(self.categories, QIcon("resources/images/categories.png"), "Categories")
        self.tabs.addTab(self.reports, QIcon("resources/images/reports.png"), "Reports")
        
        # Set application style
        self.setStyleSheet(MAIN_STYLE)

    def create_menu_bar(self):
        """Create the menu bar with actions"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Add actions to file menu
        new_sale_action = QAction(QIcon("resources/images/sales.png"), "New Sale", self)
        new_sale_action.setShortcut("Ctrl+N")
        new_sale_action.triggered.connect(lambda: self.set_current_tab(1))  # Switch to Sales tab
        file_menu.addAction(new_sale_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Add actions to view menu
        dashboard_action = QAction(QIcon("resources/images/dashboard.png"), "Dashboard", self)
        dashboard_action.triggered.connect(lambda: self.set_current_tab(0))
        view_menu.addAction(dashboard_action)
        
        sales_action = QAction(QIcon("resources/images/sales.png"), "Sales", self)
        sales_action.triggered.connect(lambda: self.set_current_tab(1))
        view_menu.addAction(sales_action)
        
        products_action = QAction(QIcon("resources/images/products.png"), "Products", self)
        products_action.triggered.connect(lambda: self.set_current_tab(2))
        view_menu.addAction(products_action)
        
        categories_action = QAction(QIcon("resources/images/categories.png"), "Categories", self)
        categories_action.triggered.connect(lambda: self.set_current_tab(3))
        view_menu.addAction(categories_action)
        
        reports_action = QAction(QIcon("resources/images/reports.png"), "Reports", self)
        reports_action.triggered.connect(lambda: self.set_current_tab(4))
        view_menu.addAction(reports_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About POS System",
                         "Point of Sale System\nVersion 1.0\n\n"
                         "A modern POS system built with PyQt5")

    def show_login(self):
        self.login_window = LoginWindow(self.db_manager)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.show()

    def on_login_successful(self, user_data):
        self.current_user = user_data
        self.show()  # Show the main window after successful login
        self.update_ui_for_user()
        self.dashboard.update_summary()  # Update dashboard after login
        self.notifications.show_success("Login Successful", f"Welcome back, {user_data['full_name']}!")

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
        if self.notifications.show_question('Confirm Exit', "Are you sure you want to exit?"):
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    
    sys.exit(app.exec_())