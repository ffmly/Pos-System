from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from utils.styles import LOGIN_STYLE

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)  # Signal to emit user data on successful login

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login - POS System')
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon('resources/images/pos_icon.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('resources/logo.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title_label = QLabel('Welcome Back')
        title_label.setProperty('class', 'title')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel('Username')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # Set layout
        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet(LOGIN_STYLE)

        # Set focus to username input
        self.username_input.setFocus()

        # Connect enter key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Login Failed', 'Please enter both username and password.')
            return

        if self.db_manager.connect():
            user = self.db_manager.authenticate_user(username, password)
            self.db_manager.disconnect()

            if user:
                user_data = dict(user)
                self.login_successful.emit(user_data)
                self.close()
            else:
                QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')
                self.password_input.clear()
                self.password_input.setFocus()
        else:
            QMessageBox.critical(self, 'Error', 'Could not connect to database')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.handle_login()
        else:
            super().keyPressEvent(event) 