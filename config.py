"""
Configuration settings for the POS system.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database settings
DATABASE = {
    'name': 'pos.db',
    'path': os.path.join(BASE_DIR, 'database', 'pos.db'),
    'backup_dir': os.path.join(BASE_DIR, 'database', 'backups')
}

# Application settings
APP = {
    'name': 'نظام نقاط البيع',
    'version': '1.0.0',
    'company': 'شركتي',
    'default_language': 'ar',
    'default_currency': 'SAR',
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M:%S'
}

# UI settings
UI = {
    'theme': 'light',
    'font_family': 'Arial',
    'font_size': 10,
    'window_size': (1200, 800),
    'min_window_size': (800, 600)
}

# Logging settings
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.path.join(BASE_DIR, 'logs', 'pos.log')
}

# Create necessary directories
os.makedirs(DATABASE['backup_dir'], exist_ok=True)
os.makedirs(os.path.dirname(LOGGING['file']), exist_ok=True) 