import datetime
import random
import locale

# تعيين الإعدادات المحلية للعملة
try:
    locale.setlocale(locale.LC_ALL, 'ar_SA.UTF-8')  # للغة العربية
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # إذا لم تكن العربية متاحة
    except:
        pass  # استخدام الإعدادات الافتراضية

def format_currency(amount):
    """تنسيق المبلغ كعملة"""
    try:
        return locale.currency(amount, grouping=True)
    except:
        return f"{amount:.2f} ر.س"  # تنسيق بديل

def generate_invoice_number():
    """توليد رقم فاتورة فريد"""
    today = datetime.datetime.now()
    date_part = today.strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"INV-{date_part}-{random_part}"

def format_date(date_obj):
    """تنسيق التاريخ"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")
        except:
            return date_obj
    
    try:
        return date_obj.strftime("%Y-%m-%d %H:%M")
    except:
        return str(date_obj)