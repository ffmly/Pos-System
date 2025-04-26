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
        self.category_data = category_data
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("إضافة/تعديل فئة")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # نموذج البيانات
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        
        form_layout.addRow("اسم الفئة:", self.name_input)
        form_layout.addRow("الوصف:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # أزرار الإجراءات
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        # إذا كانت هناك بيانات، قم بملء الحقول
        if self.category_data:
            self.name_input.setText(self.category_data['name'])
            self.description_input.setText(self.category_data.get('description', ''))
    
    def get_category_data(self):
        """الحصول على بيانات الفئة من الحقول"""
        return {
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText()
        }

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
            category_data = dialog.get_category_data()
            
            if not category_data['name']:
                QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم الفئة")
                return
            
            try:
                self.category_model.add_category(category_data)
                self.load_categories()
                QMessageBox.information(self, "نجاح", "تمت إضافة الفئة بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء إضافة الفئة: {str(e)}")
    
    def edit_category(self, category):
        """تعديل فئة"""
        dialog = CategoryDialog(self, category)
        if dialog.exec_() == QDialog.Accepted:
            category_data = dialog.get_category_data()
            
            if not category_data['name']:
                QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم الفئة")
                return
            
            try:
                self.category_model.update_category(category['id'], category_data)
                self.load_categories()
                QMessageBox.information(self, "نجاح", "تم تعديل الفئة بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تعديل الفئة: {str(e)}")
    
    def delete_category(self, category):
        """حذف فئة"""
        confirm = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف الفئة '{category['name']}'؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                self.category_model.delete_category(category['id'])
                self.load_categories()
                QMessageBox.information(self, "نجاح", "تم حذف الفئة بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حذف الفئة: {str(e)}")