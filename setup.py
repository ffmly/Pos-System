"""
Setup script for the POS system.
"""

from setuptools import setup, find_packages

setup(
    name="pos-system",
    version="1.0.0",
    description="نظام نقاط البيع",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        'PyQt5==5.15.9',
        'PyQt5-Qt5==5.15.2',
        'PyQt5-sip==12.11.0',
        'qrcode==7.3.1',
        'reportlab==3.6.12',
        'python-barcode==0.13.1',
        'Pillow==9.5.0',
        'python-dateutil==2.8.2',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
) 