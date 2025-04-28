from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

class NotificationSystem:
    def __init__(self, parent=None):
        self.parent = parent
        self.tray_icon = None
        self.setup_tray_icon()
    
    def setup_tray_icon(self):
        """Setup system tray icon"""
        self.tray_icon = QSystemTrayIcon(self.parent)
        self.tray_icon.setIcon(QIcon("resources/images/icon.png"))
        
        # Create tray menu
        tray_menu = QMenu()
        
        # Add actions
        show_action = QAction("Show", self.parent)
        show_action.triggered.connect(self.parent.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self.parent)
        quit_action.triggered.connect(self.parent.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def show_error(self, title, message, duration=5000):
        """Show error notification"""
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Critical,
            duration
        )
        QMessageBox.critical(self.parent, title, message)
    
    def show_warning(self, title, message, duration=5000):
        """Show warning notification"""
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Warning,
            duration
        )
        QMessageBox.warning(self.parent, title, message)
    
    def show_info(self, title, message, duration=5000):
        """Show info notification"""
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            duration
        )
        QMessageBox.information(self.parent, title, message)
    
    def show_success(self, title, message, duration=5000):
        """Show success notification"""
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            duration
        )
        QMessageBox.information(self.parent, title, message)
    
    def show_question(self, title, message):
        """Show question dialog"""
        reply = QMessageBox.question(
            self.parent,
            title,
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes 