"""
UI Components Package
Contains all the user interface components for the POS system.
"""

from .login import LoginWindow
from .dashboard import DashboardWidget
from .sales import SalesWidget
from .products import ProductsWidget
from .categories import CategoriesWidget
from .reports import ReportsWidget

__all__ = [
    'LoginWindow',
    'DashboardWidget',
    'SalesWidget',
    'ProductsWidget',
    'CategoriesWidget',
    'ReportsWidget'
] 