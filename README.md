# Car Inventory Management System

A command-line based Python application that allows users to manage a car dealership's inventory, track sales, and generate reports. Built with a focus on modular design, secure authentication, and extensibility.

---

## Features

- **User Authentication**

  - Secure login and registration with SHA-256 password hashing.

- **Inventory Management**

  - Add new vehicles with detailed attributes (Model, Type, VIN, Mileage, Year, Faults, etc.)
  - View current or complete inventory with clear formatting
  - Update mileage, faults, or other details based on VIN

- **Sales Tracking**

  - Mark cars as sold and calculate profits
  - Track and export total sales, tax, and profit reports

- **PDF Report Generation**

  - Export detailed inventory and sales reports to PDF using `fpdf`

- **Data Persistence**

  - Data stored in `.xlsx` files for inventory, sales, and users using `pandas`

---

## Tech Stack

- **Language**: Python 3
- **Libraries**: `pandas`, `fpdf`, `hashlib`, `getpass`, `os`, `time`
- **Storage**: Excel files (`.xlsx`) via `pandas`

---

## How to Run

1. Clone the repo

```bash
git clone https://github.com/yourusername/car-inventory-system.git
cd car-inventory-system
```

2. Install dependencies (you can use a virtual environment)

```bash
pip install pandas fpdf openpyxl
```

3. Run the script

```bash
python inventory.py
```

---

## Folder Structure

```
car-inventory-system/
├── inventory.py          # Main application file
├── inventory.xlsx        # Auto-created inventory database
├── sold_cars.xlsx        # Auto-created sales record
├── users.xlsx            # Auto-created user credentials
└── README.md             # Project documentation
```

---

## Future Improvements

- Add GUI support (e.g. Tkinter or PyQt)
- Integrate with a real database (MySQL/PostgreSQL)
- Role-based access control (Admin vs. Staff)
- REST API version

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Developed by [FrankWiteman]

