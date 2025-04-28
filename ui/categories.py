from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QDialog, QFormLayout,
                            QDialogButtonBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from models.category import Category

class CategoryDialog(QDialog):
    def __init__(self, parent=None, category_data=None):
        super().__init__(parent)
        self.parent = parent
        self.category_data = category_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add Category' if not self.category_data else 'Edit Category')
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Name
        self.name_input = QLineEdit()
        if self.category_data:
            self.name_input.setText(self.category_data['name'])
        layout.addRow('Name:', self.name_input)

        # Description
        self.description_input = QTextEdit()
        if self.category_data:
            self.description_input.setText(self.category_data['description'])
        self.description_input.setMaximumHeight(100)
        layout.addRow('Description:', self.description_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_category)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow('', button_layout)

        self.setLayout(layout)

    def save_category(self):
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, 'Error', 'Category name is required')
            return

        if self.parent.parent.db_manager.connect():
            category_data = {
                'name': name,
                'description': description
            }

            if self.category_data:  # Update existing category
                category_data['id'] = self.category_data['id']
                success = self.parent.parent.db_manager.update_category(category_data)
            else:  # Add new category
                success = self.parent.parent.db_manager.add_category(name, description)
            
            self.parent.parent.db_manager.disconnect()
            
            if success:
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to save category')

class CategoriesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Add category section
        add_section = QHBoxLayout()
        
        # Category name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Category Name")
        add_section.addWidget(self.name_input)
        
        # Add button
        add_button = QPushButton("Add Category")
        add_button.clicked.connect(self.add_category)
        add_section.addWidget(add_button)
        
        layout.addLayout(add_section)

        # Categories table
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(3)
        self.categories_table.setHorizontalHeaderLabels(["ID", "Name", "Description"])
        self.categories_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.categories_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        layout.addWidget(self.categories_table)

        self.setLayout(layout)
        
        # Load initial data
        self.load_categories()

    def add_category(self):
        """Add a new category"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a category name")
            return

        if self.parent.db_manager.add_category(name):
            self.name_input.clear()
            self.load_categories()
            QMessageBox.information(self, "Success", "Category added successfully")
        else:
            QMessageBox.warning(self, "Error", "Failed to add category")

    def load_categories(self):
        """Load categories from database"""
        try:
            categories = self.parent.db_manager.get_categories()
            self.categories_table.setRowCount(len(categories))
            
            for row, category in enumerate(categories):
                # ID
                self.categories_table.setItem(row, 0, QTableWidgetItem(str(category[0])))
                
                # Name
                self.categories_table.setItem(row, 1, QTableWidgetItem(category[1]))
                
                # Description
                self.categories_table.setItem(row, 2, QTableWidgetItem(category[2] or ""))
            
            self.categories_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error loading categories: {e}")
            QMessageBox.warning(self, "Error", "Failed to load categories")