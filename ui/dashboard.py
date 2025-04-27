from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

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
        
        user_label = QLabel(f'Logged in as: {self.parent.current_user["full_name"]}')
        user_label.setStyleSheet('color: white; font-size: 16px;')
        welcome_layout.addWidget(user_label)
        
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
        summary_frame = QFrame()
        summary_frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        ''')
        summary_layout = QGridLayout(summary_frame)
        
        # Summary cards
        summary_items = [
            ('Total Sales', '0', '#4CAF50'),
            ('Products', '0', '#2196F3'),
            ('Low Stock', '0', '#FFC107'),
            ('Categories', '0', '#9C27B0')
        ]
        
        for i, (title, value, color) in enumerate(summary_items):
            card = QFrame()
            card.setStyleSheet(f'''
                QFrame {{
                    background-color: {color};
                    border-radius: 5px;
                    padding: 15px;
                }}
            ''')
            card_layout = QVBoxLayout(card)
            
            value_label = QLabel(value)
            value_label.setStyleSheet('color: white; font-size: 24px; font-weight: bold;')
            card_layout.addWidget(value_label)
            
            title_label = QLabel(title)
            title_label.setStyleSheet('color: white; font-size: 14px;')
            card_layout.addWidget(title_label)
            
            summary_layout.addWidget(card, i // 2, i % 2)
        
        layout.addWidget(summary_frame)

        # Set layout
        self.setLayout(layout)

    def update_summary(self):
        """Update summary information"""
        if self.parent.db_manager.connect():
            # Get total sales
            self.parent.db_manager.cursor.execute('''
                SELECT COUNT(*) as count, COALESCE(SUM(final_amount), 0) as total 
                FROM sales 
                WHERE DATE(created_at) = DATE('now')
            ''')
            sales_data = self.parent.db_manager.cursor.fetchone()
            
            # Get products count
            self.parent.db_manager.cursor.execute('SELECT COUNT(*) FROM products')
            products_count = self.parent.db_manager.cursor.fetchone()[0]
            
            # Get low stock items
            self.parent.db_manager.cursor.execute('''
                SELECT COUNT(*) FROM products 
                WHERE quantity <= min_quantity
            ''')
            low_stock_count = self.parent.db_manager.cursor.fetchone()[0]
            
            # Get categories count
            self.parent.db_manager.cursor.execute('SELECT COUNT(*) FROM categories')
            categories_count = self.parent.db_manager.cursor.fetchone()[0]
            
            self.parent.db_manager.disconnect()
            
            # Update labels
            self.findChild(QLabel, 'total_sales').setText(f'{sales_data["total"]:.2f}')
            self.findChild(QLabel, 'products_count').setText(str(products_count))
            self.findChild(QLabel, 'low_stock_count').setText(str(low_stock_count))
            self.findChild(QLabel, 'categories_count').setText(str(categories_count))