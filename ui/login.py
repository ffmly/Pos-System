from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)  # Signal to emit user data on successful login

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login - POS System')
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('resources/logo.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title_label = QLabel('Point of Sale System')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(title_label)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.login_button.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_button)

        # Set layout
        self.setLayout(layout)

        # Set window style
        self.setStyleSheet('''
            QWidget {
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        ''')

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        if self.db_manager.connect():
            user = self.db_manager.authenticate_user(username, password)
            self.db_manager.disconnect()

            if user:
                user_data = dict(user)
                self.login_successful.emit(user_data)
                self.close()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid username or password')
                self.password_input.clear()
        else:
            QMessageBox.critical(self, 'Error', 'Could not connect to database') 