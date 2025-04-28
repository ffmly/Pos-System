from PyQt5.QtCore import Qt

# Color palette
COLORS = {
    'primary': '#007bff',
    'primary_dark': '#0056b3',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'gray': '#6c757d',
    'white': '#ffffff',
    'border': '#dee2e6'
}

# Font settings
FONTS = {
    'default': 'Segoe UI, Arial, sans-serif',
    'heading': 'Segoe UI, Arial, sans-serif',
    'monospace': 'Consolas, Monaco, monospace'
}

MAIN_STYLE = f'''
    QMainWindow {{
        background-color: {COLORS['light']};
        font-family: {FONTS['default']};
    }}
    
    QTabWidget::pane {{
        border: none;
        background-color: {COLORS['white']};
        border-radius: 8px;
        padding: 15px;
    }}
    
    QTabBar::tab {{
        background-color: {COLORS['light']};
        color: {COLORS['dark']};
        border: none;
        padding: 12px 25px;
        margin-right: 4px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-weight: bold;
        font-size: 14px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {COLORS['border']};
    }}
    
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
        min-width: 80px;
        font-size: 14px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['dark']};
    }}
    
    QPushButton[class="success"] {{
        background-color: {COLORS['success']};
    }}
    
    QPushButton[class="warning"] {{
        background-color: {COLORS['warning']};
    }}
    
    QPushButton[class="danger"] {{
        background-color: {COLORS['danger']};
    }}
    
    QLineEdit, QComboBox, QSpinBox {{
        padding: 8px;
        border: 2px solid {COLORS['border']};
        border-radius: 4px;
        background-color: {COLORS['white']};
        min-height: 20px;
        font-size: 14px;
    }}
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
        border-color: {COLORS['primary']};
    }}
    
    QTableWidget {{
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        background-color: {COLORS['white']};
        gridline-color: {COLORS['border']};
        font-size: 14px;
    }}
    
    QTableWidget::item {{
        padding: 8px;
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['light']};
        padding: 8px;
        border: none;
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        font-weight: bold;
        font-size: 14px;
    }}
    
    QLabel {{
        color: {COLORS['dark']};
        font-size: 14px;
    }}
    
    QStatusBar {{
        background-color: {COLORS['light']};
        color: {COLORS['dark']};
        border-top: 1px solid {COLORS['border']};
        font-size: 12px;
    }}
    
    QMenuBar {{
        background-color: {COLORS['light']};
        border-bottom: 1px solid {COLORS['border']};
        font-size: 14px;
    }}
    
    QMenuBar::item {{
        padding: 8px 12px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    QMenu {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        font-size: 14px;
    }}
    
    QMenu::item {{
        padding: 6px 25px 6px 20px;
    }}
    
    QMenu::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
    }}
    
    QMessageBox {{
        font-size: 14px;
    }}
    
    QMessageBox QLabel {{
        font-size: 14px;
    }}
    
    QMessageBox QPushButton {{
        min-width: 100px;
    }}
'''

DASHBOARD_CARD_STYLE = f'''
    QFrame {{
        background-color: {COLORS['white']};
        border-radius: 8px;
        padding: 15px;
        border: 1px solid {COLORS['border']};
    }}
    
    QLabel {{
        color: {COLORS['dark']};
        font-size: 14px;
    }}
    
    QLabel[class="title"] {{
        font-size: 16px;
        font-weight: bold;
        color: {COLORS['primary']};
        margin-bottom: 8px;
    }}
    
    QLabel[class="value"] {{
        font-size: 24px;
        font-weight: bold;
        color: {COLORS['dark']};
    }}
    
    QLabel[class="subtitle"] {{
        color: {COLORS['gray']};
        font-size: 12px;
    }}
'''

LOGIN_STYLE = f'''
    QWidget {{
        background-color: {COLORS['white']};
        font-family: {FONTS['default']};
    }}
    
    QLabel {{
        color: {COLORS['dark']};
        font-size: 14px;
    }}
    
    QLabel[class="title"] {{
        font-size: 24px;
        font-weight: bold;
        color: {COLORS['primary']};
        margin-bottom: 20px;
    }}
    
    QLineEdit {{
        padding: 10px;
        border: 2px solid {COLORS['border']};
        border-radius: 4px;
        font-size: 14px;
        margin-bottom: 10px;
    }}
    
    QLineEdit:focus {{
        border-color: {COLORS['primary']};
    }}
    
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        padding: 12px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
        min-width: 120px;
        margin-top: 10px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    
    QMessageBox {{
        font-size: 14px;
    }}
    
    QMessageBox QLabel {{
        font-size: 14px;
    }}
''' 