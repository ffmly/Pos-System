# Point of Sale (POS) System

A comprehensive Point of Sale system built with Python and PyQt5. This system helps businesses manage their sales, inventory, and reporting needs efficiently.

## Features

- User Authentication and Role-based Access Control
- Product Management with Barcode Support
- Category Management
- Sales Management with Invoice Generation
- Inventory Tracking with Low Stock Alerts
- Comprehensive Reporting System
- Customer Management
- Modern and User-friendly Interface

## Requirements

- Python 3.8 or higher
- PyQt5
- SQLite3
- Additional dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pos-system.git
cd pos-system
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python main.py
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Login with default credentials:
   - Username: admin
   - Password: admin123

3. Navigate through different sections:
   - Dashboard: Overview of sales and inventory
   - Sales: Create and manage sales transactions
   - Products: Manage products and inventory
   - Categories: Organize products into categories
   - Reports: Generate various business reports

## Directory Structure

```
pos-system/
├── database/           # Database management and schema
├── ui/                 # User interface components
├── models/            # Data models
├── utils/             # Utility functions
├── resources/         # Static resources (images, icons)
├── data/              # Database and other data files
├── main.py            # Application entry point
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt5 for the GUI framework
- SQLite for the database engine
- Icons and images from various open-source projects

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 