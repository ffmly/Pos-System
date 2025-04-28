from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from datetime import datetime, timedelta

from utils.styles import DASHBOARD_CARD_STYLE

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Welcome section
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet('''
            QFrame {
                background-color: #4CAF50;
                border-radius: 10px;
                padding: 20px;
            }
        ''')
        welcome_layout = QVBoxLayout(welcome_frame)
        
        welcome_label = QLabel('Welcome to POS System')
        welcome_label.setStyleSheet('color: white; font-size: 24px; font-weight: bold;')
        welcome_layout.addWidget(welcome_label)
        
        self.user_label = QLabel('Please log in')
        self.user_label.setStyleSheet('color: white; font-size: 16px;')
        welcome_layout.addWidget(self.user_label)
        
        layout.addWidget(welcome_frame)

        # Quick access buttons
        quick_access_frame = QFrame()
        quick_access_frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        ''')
        quick_access_layout = QGridLayout(quick_access_frame)
        
        # Create quick access buttons
        buttons = [
            ('New Sale', 'sales', 'Create a new sale'),
            ('Products', 'products', 'Manage products'),
            ('Categories', 'categories', 'Manage categories'),
            ('Reports', 'reports', 'View reports')
        ]
        
        for i, (text, tab, tooltip) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: #f0f0f0;
                    border: none;
                    padding: 15px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            ''')
            btn.clicked.connect(lambda checked, t=tab: self.parent.set_current_tab(
                self.parent.tabs.indexOf(getattr(self.parent, t))
            ))
            quick_access_layout.addWidget(btn, i // 2, i % 2)
        
        layout.addWidget(quick_access_frame)

        # Summary section
        summary_layout = QHBoxLayout()
        
        # Total Sales Card
        self.total_sales_card = QFrame()
        self.total_sales_card.setStyleSheet(DASHBOARD_CARD_STYLE)
        total_sales_layout = QVBoxLayout(self.total_sales_card)
        
        total_sales_title = QLabel("Total Sales")
        total_sales_title.setProperty("class", "title")
        total_sales_layout.addWidget(total_sales_title)
        
        self.total_sales_count = QLabel("0")
        self.total_sales_count.setProperty("class", "value")
        total_sales_layout.addWidget(self.total_sales_count)
        
        summary_layout.addWidget(self.total_sales_card)
        
        # Total Revenue Card
        self.total_revenue_card = QFrame()
        self.total_revenue_card.setStyleSheet(DASHBOARD_CARD_STYLE)
        total_revenue_layout = QVBoxLayout(self.total_revenue_card)
        
        total_revenue_title = QLabel("Total Revenue")
        total_revenue_title.setProperty("class", "title")
        total_revenue_layout.addWidget(total_revenue_title)
        
        self.total_revenue_count = QLabel("$0.00")
        self.total_revenue_count.setProperty("class", "value")
        total_revenue_layout.addWidget(self.total_revenue_count)
        
        summary_layout.addWidget(self.total_revenue_card)
        
        # Average Sale Card
        self.average_sale_card = QFrame()
        self.average_sale_card.setStyleSheet(DASHBOARD_CARD_STYLE)
        average_sale_layout = QVBoxLayout(self.average_sale_card)
        
        average_sale_title = QLabel("Average Sale")
        average_sale_title.setProperty("class", "title")
        average_sale_layout.addWidget(average_sale_title)
        
        self.average_sale_count = QLabel("$0.00")
        self.average_sale_count.setProperty("class", "value")
        average_sale_layout.addWidget(self.average_sale_count)
        
        summary_layout.addWidget(self.average_sale_card)
        
        layout.addLayout(summary_layout)

        # Low Stock Products Table
        low_stock_label = QLabel("Low Stock Products")
        low_stock_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(low_stock_label)
        
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(5)
        self.low_stock_table.setHorizontalHeaderLabels([
            "Product", "Category", "Current Stock", "Minimum Stock", "Status"
        ])
        self.low_stock_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.low_stock_table)

        # Set layout
        self.setLayout(layout)

        # Update data
        self.update_summary()
        self.update_low_stock()

    def update_summary(self):
        """Update dashboard summary"""
        try:
            # Get sales data for the last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            sales_data = self.parent.db_manager.get_sales_summary(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            # Update summary cards
            self.total_sales_count.setText(str(sales_data['total_sales']))
            self.total_revenue_count.setText(f"${sales_data['total_amount']:.2f}")
            self.average_sale_count.setText(f"${sales_data['average_sale']:.2f}")
            
        except Exception as e:
            print(f"Error updating dashboard summary: {e}")

    def update_low_stock(self):
        """Update low stock products table"""
        try:
            low_stock_products = self.parent.db_manager.get_low_stock_products()
            
            self.low_stock_table.setRowCount(len(low_stock_products))
            
            for row, product in enumerate(low_stock_products):
                # Product name
                self.low_stock_table.setItem(row, 0, QTableWidgetItem(product[1]))
                
                # Category
                self.low_stock_table.setItem(row, 1, QTableWidgetItem(product[9] or "No Category"))
                
                # Current stock
                self.low_stock_table.setItem(row, 2, QTableWidgetItem(str(product[6])))
                
                # Minimum stock
                self.low_stock_table.setItem(row, 3, QTableWidgetItem(str(product[7])))
                
                # Status
                status = "Critical" if product[6] == 0 else "Low"
                status_item = QTableWidgetItem(status)
                status_item.setForeground(Qt.red if status == "Critical" else Qt.darkYellow)
                self.low_stock_table.setItem(row, 4, status_item)
            
            self.low_stock_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error updating low stock products: {e}")