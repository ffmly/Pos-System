import datetime
import random
import locale
import re

# تعيين الإعدادات المحلية للعملة
try:
    locale.setlocale(locale.LC_ALL, 'ar_SA.UTF-8')  # للغة العربية
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # إذا لم تكن العربية متاحة
    except:
        pass  # استخدام الإعدادات الافتراضية

def format_currency(amount):
    """Format a number as currency"""
    try:
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def generate_invoice_number():
    """توليد رقم فاتورة فريد"""
    today = datetime.datetime.now()
    date_part = today.strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"INV-{date_part}-{random_part}"

def format_date(date):
    """Format a date as YYYY-MM-DD"""
    if isinstance(date, str):
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return date
    return date.strftime("%Y-%m-%d")

def validate_barcode(barcode):
    """Validate a barcode format"""
    if not barcode:
        return False
    
    # Remove any spaces or special characters
    barcode = re.sub(r'[^0-9]', '', barcode)
    
    # Check if it's a valid length (8, 12, 13, or 14 digits)
    if len(barcode) not in [8, 12, 13, 14]:
        return False
    
    # Check if it contains only digits
    if not barcode.isdigit():
        return False
    
    return True

def format_phone(phone):
    """Format a phone number as (XXX) XXX-XXXX"""
    if not phone:
        return ""
    
    # Remove any non-digit characters
    digits = re.sub(r'[^0-9]', '', phone)
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone

def format_time(time):
    """Format a time as HH:MM AM/PM"""
    if isinstance(time, str):
        try:
            time = datetime.datetime.strptime(time, "%H:%M:%S")
        except ValueError:
            return time
    return time.strftime("%I:%M %p")

def sanitize_input(text):
    """Remove potentially harmful characters from input"""
    if not text:
        return ""
    # Remove HTML tags and special characters
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s\-.,]', '', text)
    return text.strip()

def calculate_discount(price, discount_percent):
    """Calculate discounted price"""
    try:
        price = float(price)
        discount_percent = float(discount_percent)
        if discount_percent < 0 or discount_percent > 100:
            return price
        return price * (1 - discount_percent / 100)
    except (ValueError, TypeError):
        return price

def calculate_tax(price, tax_rate):
    """Calculate tax amount"""
    try:
        price = float(price)
        tax_rate = float(tax_rate)
        if tax_rate < 0:
            return 0
        return price * (tax_rate / 100)
    except (ValueError, TypeError):
        return 0