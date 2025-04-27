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
        self.category_model = Category()
        
        self.setup_ui()
        self.load_categories()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # عنوان الصفحة
        title_label = QLabel("إدارة الفئات")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # أزرار الإجراءات
        actions_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("إضافة فئة جديدة")
        self.add_btn.clicked.connect(self.add_category)
        
        self.refresh_btn = QPushButton("تحديث")
        self.refresh_btn.clicked.connect(self.load_categories)
        
        actions_layout.addWidget(self.add_btn)
        actions_layout.addWidget(self.refresh_btn)
        actions_layout.addStretch()
        
        main_layout.addLayout(actions_layout)
        
        # جدول الفئات
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(4)
        self.categories_table.setHorizontalHeaderLabels([
            "الرقم", "اسم الفئة", "الوصف", "الإجراءات"
        ])
        self.categories_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(self.categories_table)
    
    def load_categories(self):
        """تحميل الفئات"""
        categories = self.category_model.get_all_categories()
        
        self.categories_table.setRowCount(0)
        
        for row, category in enumerate(categories):
            self.categories_table.insertRow(row)
            
            # إضافة بيانات الفئة
            self.categories_table.setItem(row, 0, QTableWidgetItem(str(category['id'])))
            self.categories_table.setItem(row, 1, QTableWidgetItem(category['name']))
            self.categories_table.setItem(row, 2, QTableWidgetItem(category.get('description', '')))
            
            # إضافة أزرار الإجراءات
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("تعديل")
            edit_btn.clicked.connect(lambda _, c=category: self.edit_category(c))
            
            delete_btn = QPushButton("حذف")
            delete_btn.clicked.connect(lambda _, c=category: self.delete_category(c))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            
            self.categories_table.setCellWidget(row, 3, actions_widget)
    
    def add_category(self):
        """إضافة فئة جديدة"""
        dialog = CategoryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories()
    
    def edit_category(self, category):
        """تعديل فئة"""
        dialog = CategoryDialog(self, category)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories()
    
    def delete_category(self, category):
        """حذف فئة"""
        # Check if category has products
        if self.parent.parent.db_manager.connect():
            products = self.parent.parent.db_manager.get_products(category['id'])
            self.parent.parent.db_manager.disconnect()
            
            if products:
                QMessageBox.warning(
                    self, 'Error',
                    'Cannot delete category that has products. Please remove or reassign the products first.'
                )
                return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Are you sure you want to delete category '{category['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.parent.parent.db_manager.connect():
                if self.parent.parent.db_manager.delete_category(category['id']):
                    self.load_categories()
                else:
                    QMessageBox.warning(self, 'Error', 'Failed to delete category')
                self.parent.parent.db_manager.disconnect()