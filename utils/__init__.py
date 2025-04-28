"""
Utilities Package
Contains helper functions and utilities for the POS system.
"""

from .helpers import (
    format_currency,
    format_date,
    validate_barcode,
    format_phone,
    format_time,
    sanitize_input,
    calculate_discount,
    calculate_tax
)

from .styles import (
    MAIN_STYLE,
    DASHBOARD_CARD_STYLE,
    LOGIN_STYLE,
    COLORS
)

from .notifications import NotificationSystem

__all__ = [
    'format_currency',
    'format_date',
    'validate_barcode',
    'format_phone',
    'format_time',
    'sanitize_input',
    'calculate_discount',
    'calculate_tax',
    'MAIN_STYLE',
    'DASHBOARD_CARD_STYLE',
    'LOGIN_STYLE',
    'COLORS',
    'NotificationSystem'
] 