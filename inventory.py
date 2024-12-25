#!/usr/bin/env python3

import pandas as pd
import os
import hashlib
import getpass
import sys
from fpdf import FPDF

# Constants
SALES_TAX = 0.075
INVENTORY_FILE = "inventory.xlsx"
SOLD_CARS_FILE = "sold_cars.xlsx"
USERS_FILE = "users.xlsx"

# Initialize data
inventory = []  # List of cars in inventory
sold_cars = []  # List of sold cars
expenditures = 0.0  # Total expenditures
users = {}  # Dictionary of users and hashed passwords

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    global inventory, sold_cars, users
    if os.path.exists(INVENTORY_FILE):
        inventory = pd.read_excel(INVENTORY_FILE).to_dict('records')
    if os.path.exists(SOLD_CARS_FILE):
        sold_cars = pd.read_excel(SOLD_CARS_FILE).to_dict('records')
    if os.path.exists(USERS_FILE):
        user_data = pd.read_excel(USERS_FILE).to_dict('records')
        users = {user["Username"]: user["Password"] for user in user_data}

def save_data():
    pd.DataFrame(inventory).to_excel(INVENTORY_FILE, index=False)
    pd.DataFrame(sold_cars).to_excel(SOLD_CARS_FILE, index=False)
    user_data = [{"Username": username, "Password": password} for username, password in users.items()]
    pd.DataFrame(user_data).to_excel(USERS_FILE, index=False)

def register_user():
    print("Register a new user")
    while True:
        username = input("Enter a new username: ")
        if username in users:
            print("Username already exists. Please choose another.")
        else:
            password = getpass.getpass("Enter a password: ")
            confirm_password = getpass.getpass("Confirm your password: ")
            if password == confirm_password:
                users[username] = hash_password(password)
                save_data()
                print("User  registered successfully!\n")
                break
            else:
                print("Passwords do not match. Please try again.")

def user_login():
    print("Welcome! Please log in or register to access the program.")
    while True:
        option = input("Do you want to (1) Log in or (2) Register or (3) Quit? Enter 1, 2, or 3: ")
        if option == "1":
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            hashed_password = hash_password(password)

            if username in users and users[username] == hashed_password:
                print("Login successful!\n")
                break
            else:
                print("Invalid credentials. Please try again.\n")
        elif option == "2":
            register_user()
        elif option == "3":
            print("You chose to exit. Goodbye!")
            sys.exit()  # Exits the function immediately
        else:
            print("Invalid option. Please enter 1, 2, or 3.")

def add_inventory():
    while True:
        name = input("Enter vehicle name: ")
        vehicle_type = input("Enter vehicle type: ")
        vin = input("Enter VIN (full or last 6 digits): ")
        faults = input("Does the vehicle have faults? (Yes/No): ")

        issues = ""
        if faults.lower() == "yes":
            issues = input("Enter the issues with the vehicle: ")

        price = float(input("Enter the price of the vehicle: "))

        inventory.append({
            "Name": name,
            "Type": vehicle_type,
            "VIN": vin,
            "Faults": issues,
            "Price": price,
            "Sold": False
        })
        save_data()
        print("Inventory updated successfully.")

        go_back = input("Would you like to add another vehicle or go back? (add/back): ")
        if go_back.lower() == "back":
            break

def add_expenditure():
    global expenditures
    while True:
        amount = float(input("Enter the amount spent: "))
        expenditures += amount
        print("Expenditure updated.")

        go_back = input("Would you like to add another expenditure or go back? (add/back): ")
        if go_back.lower() == "back":
            break

def sell_car():
    while True:
        vin = input("Enter the VIN (full or last 6 digits) of the car to mark as sold: ")
        car = next((c for c in inventory if vin in c["VIN"] and not c["Sold"]), None)

        if car:
            sales_price = float(input("Enter the sales price: "))
            tax = sales_price * SALES_TAX
            profit = sales_price - car["Price"] - tax

            car["Sold"] = True
            sold_cars.append({
                **car,
                "SalesPrice": sales_price,
                "Tax": tax,
                "Profit": profit
            })
            save_data()
            print("Car marked as sold and database updated.")
        else:
            print("Car not found or already sold.")

        go_back = input("Would you like to mark another car as sold or go back? (sell/back): ")
        if go_back.lower() == "back":
            break

def import_inventory():
    global inventory
    while True:
        file_path = input("Enter the file path of the Excel file to import: ")

        try:
            imported_data = pd.read_excel(file_path).to_dict('records')
            
            # Merge the imported data with existing inventory
            inventory.extend(imported_data)
            save_data()  # Save the updated inventory to the default file
            print(f"Successfully imported {len(imported_data)} vehicles into inventory.")
        except Exception as e:
            print(f"Error importing file: {e}")

        go_back = input("Would you like to import another file or go back? (import/back): ")
        if go_back.lower() == "back":
            break

def export_to_csv(data, filename):
    pd.DataFrame(data).to_csv(filename, index=False)
    print(f"Data exported to {filename}")

def export_to_pdf(data, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for row in data:
        line = ", ".join([f"{k}: {v}" for k, v in row.items()])
        pdf.cell(0, 10, line, ln=True)

    pdf.output(filename)
    print(f"Data exported to {filename}")

def print_reports():
    while True:
        option = input("Print by (1) VIN, (2) Total Sales, or (3) Export Data: ")

        if option == "1":
            vin = input("Enter VIN (full or last 6 digits): ")
            car = next((c for c in inventory if vin in c["VIN"]), None)
            if car:
                print(car)
            else:
                print("Car not found.")
        elif option == "2":
            total_sales = sum(c["SalesPrice"] for c in sold_cars)
            total_tax = sum(c["Tax"] for c in sold_cars)
            total_profit = sum(c["Profit"] for c in sold_cars)

            print(f"Total Sales: ${total_sales:.2f}")
            print(f"Total Tax: ${total_tax:.2f}")
            print(f"Total Profit: ${total_profit:.2f}")
        elif option == "3":
            data_option = input("Export (1) Inventory, (2) Sold Cars, or (3) Reports: ")

            if data_option == "1":
                filename = input("Enter filename (e.g., inventory.csv): ")
                export_to_csv(inventory, filename)
            elif data_option == "2":
                filename = input("Enter filename (e.g., sold_cars.csv): ")
                export_to_csv(sold_cars, filename)
            elif data_option == "3":
                filename = input("Enter filename (e.g., report.pdf): ")
                export_to_pdf(sold_cars, filename)

        go_back = input("Would you like to print another report or go back? (print/back): ")
        if go_back.lower() == "back":
            break

def view_inventory(show_all=False):
    while True:
        if show_all:
            for car in inventory:
                print(car)
        else:
            for car in inventory:
                if not car["Sold"]:
                    print(car)

        go_back = input("Would you like to view again or go back? (view/back): ")
        if go_back.lower() == "back":
            break

def main():
    load_data()
    user_login()

    while True:
        print("\nWelcome User")
        print("What would you like to do?:")
        print("1. Add Inventory")
        print("2. Add Expenditures")
        print("3. Print Reports")
        print("4. Sold Cars")
        print("5. View Current Inventory")
        print("6. View All Inventory")
        print("7. Import Inventory from Excel")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_inventory()
        elif choice == "2":
            add_expenditure()
        elif choice == "3":
            print_reports()
        elif choice == "4":
            sell_car()
        elif choice == "5":
            view_inventory()
        elif choice == "6":
            view_inventory(show_all=True)
        elif choice == "7":
            import_inventory()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()