
import os
import time
import pandas as pd
import hashlib
import getpass
from fpdf import FPDF
import Keyboard

# Constants
SALES_TAX = 0.075
INVENTORY_FILE = "inventory.xlsx"
SOLD_CARS_FILE = "sold_cars.xlsx"
USERS_FILE = "users.xlsx"
EXPENDITURES_FILE = "expenditures.xlsx"  # New file for expenditures

# Initialize data
inventory = []  # List of cars in inventory
sold_cars = []  # List of sold cars
expenditures = []  # List to hold expenditure records
users = {}  # Dictionary of users and hashed passwords

# Helper functions
def clear_console():
    """Clear the console for transition."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_transition(message="Loading..."):
    """Display a transition message."""
    clear_console()
    print(message)
    time.sleep(1)  # Simulate a delay for transition

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    global inventory, sold_cars, users, expenditures
    if os.path.exists(INVENTORY_FILE):
        inventory = pd.read_excel(INVENTORY_FILE).to_dict('records')
    if os.path.exists(SOLD_CARS_FILE):
        sold_cars = pd.read_excel(SOLD_CARS_FILE).to_dict('records')
    if os.path.exists(USERS_FILE):
        user_data = pd.read_excel(USERS_FILE).to_dict('records')
        users = {user["Username"]: user["Password"] for user in user_data}
    if os.path.exists(EXPENDITURES_FILE):
        expenditures = pd.read_excel(EXPENDITURES_FILE).to_dict('records')

def save_data():
    pd.DataFrame(inventory).to_excel(INVENTORY_FILE, index=False)
    pd.DataFrame(sold_cars).to_excel(SOLD_CARS_FILE, index=False)
    user_data = [{"Username": username, "Password": password} for username, password in users.items()]
    pd.DataFrame(user_data).to_excel(USERS_FILE, index=False)
    pd.DataFrame(expenditures).to_excel(EXPENDITURES_FILE, index=False)  # Save expenditures

def register_user():
    while True:
        clear_console()
        print("Register a new user")
        username = input("Enter a new username: ").strip()
        if username in users:
            print("Username already exists. Please choose another.")
        else:
            password = getpass.getpass("Enter a password: ")
            confirm_password = getpass.getpass("Confirm your password: ")
            if password == confirm_password:
                users[username] = hash_password(password)
                save_data()
                print("User  registered successfully!")
                time.sleep(1)
                break
            else:
                print("Passwords do not match. Please try again.")
        if input("Cancel registration? (y/n): ").lower() == 'y':
            print("Registration canceled.")
            time.sleep(1)
            break

def user_login():
    while True:
        clear_console()
        print("Welcome! Please log in or register to access the program.")
        option = input("Do you want to (1) Log in or (2) Register? Enter 1 or 2: ")
        if option == "1":
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            hashed_password = hash_password(password)

            if username in users and users[username] == hashed_password:
                print(f"Login successful! Welcome {username}!")
                time.sleep(1)
                main_menu(username)  # Pass the username to the main menu
                break
            else:
                print("Invalid credentials. Please try again.")
                time.sleep(1)
        elif option == "2":
            show_transition("Navigating to Registration...")
            register_user()
        else:
            print(" Invalid option. Please enter 1 or 2.")

def go_back(previous_function, *args):
    """Handle backward navigation with transition."""
    show_transition("Returning to previous menu...")
    previous_function(*args)  # Pass any additional arguments

def add_inventory():
    while True:
        clear_console()
        print("Add Inventory Page")
        print("1. Add a vehicle")
        print("2. Go Back")

        choice = input("Select an option: ")
        if choice == "1":
            stock_number = input("Enter the stock number: ")
            name = input("Enter vehicle name: ")
            vehicle_model = input("Enter the vehicle model: ")
            vehicle_type = input("Enter vehicle type: ")
            vin = input("Enter VIN (full or last 6 digits): ")
            vehicle_year = input("Enter the vehicle year: ")
            mileage = input("Enter the Odometer Mileage: ")
            faults = input("Does the vehicle have faults? (Yes/No): ")

            issues = []
            if faults.lower() == "yes":
                issues = input("Enter the issues with the vehicle (comma-separated): ").split(',')

            price = float(input("Enter the price of the vehicle: "))

            inventory.append({
                "stock_number": stock_number,
                "Name": name,
                "Model": vehicle_model,
                "Type": vehicle_type,
                "Year": vehicle_year,
                "VIN": vin,
                "Mileage": mileage,
                "Faults": issues,
                "Price": price,
                "Sold": False
            })
            save_data()
            print("Vehicle added successfully!")
            time.sleep(1)
        elif choice == "2":
            go_back(main_menu, "User   ")  # Pass the username to go back
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

def update_inventory():
    while True:
        clear_console()
        print("Update Inventory Page")
        vin_input = input("Enter the VIN (full or last 6 digits) of the vehicle to update: ")
        
        # Check for a match with either the full VIN or the last 6 digits
        car = next((c for c in inventory if vin_input in c["VIN"][-6:] or vin_input == c["VIN"]), None)

        if car:
            print("Current details:")
            print(car)
            print("What would you like to update?")
            print("1. Name")
            print("2. Model")
            print("3. Type")
            print("4. Year")
            print("5. Mileage")
            print("6. Faults")
            print("7. Price")
            print("8. Remove Fault")
            print("9. Go Back")

            choice = input("Select an option: ")
            if choice == "1":
                new_name = input("Enter new vehicle name: ")
                car["Name"] = new_name
                print("Vehicle name updated successfully!")
            elif choice == "2":
                new_model = input("Enter new vehicle model: ")
                car["Model"] = new_model
                print("Vehicle model updated successfully!")
            elif choice == "3":
                new_type = input("Enter new vehicle type: ")
                car["Type"] = new_type
                print("Vehicle type updated successfully!")
            elif choice == "4":
                new_year = input("Enter new vehicle year: ")
                car["Year"] = new_year
                print("Vehicle year updated successfully!")
            elif choice == "5":
                new_mileage = input("Enter new mileage: ")
                car["Mileage"] = new_mileage
                print("Mileage updated successfully!")
            elif choice == "6":
                new_faults = input("Enter new faults (if any, comma-separated): ")
                car["Faults"] = new_faults.split(',') if new_faults else []
                print("Faults updated successfully!")
            elif choice == "7":
                while True:
                    try:
                        new_price = float(input("Enter new price: "))
                        car["Price"] = new_price
                        print("Price updated successfully!")
                        break
                    except ValueError:
                        print("Invalid input. Please enter a numeric value for the price.")
            elif choice == "8":
                if "Faults" in car and car["Faults"]:
                    print("Current faults:", car["Faults"])
                    fault_to_remove = input("Enter the fault to remove: ")
                    if fault_to_remove in car["Faults"]:
                        car["Faults"].remove(fault_to_remove)
                        print("Fault removed successfully!")
                    else:
                        print("Fault not found.")
                else:
                    print("No faults to remove.")
            elif choice == "9":
                break
            else:
                print("Invalid choice. Please try again.")

            # Ask if the user wants to edit the vehicle again
            edit_again = input("Do you want to edit this vehicle again? (y/n): ")
            if edit_again.lower() != 'y':
                break
        else:
            print("Vehicle not found. Please try again.")
            time.sleep(1)

def add_expenditure():
    while True:
        clear_console()
        print("Add Expenditure Page")
        print("1. Add an expenditure for a car")
        print("2. Add a miscellaneous expenditure")
        print("3. Print Expenditure Report")
        print("4. Go Back")

        choice = input("Select an option: ")
        if choice == "1":
            vin = input("Enter the VIN (full or last 6 digits) of the vehicle: ")
            car = next((c for c in inventory if vin in c["VIN"][-6:] or vin == c["VIN"]), None)

            if car:
                amount = float(input("Enter the amount spent: "))
                expenditures.append({
                    "Type": "Car",
                    "VIN": car["VIN"],
                    "Amount": amount,
                    "Description": input("Enter a description for the expenditure: ")
                })
                print("Expenditure for the car updated.")
            else:
                print("Car not found.")
            time.sleep(1)
        elif choice == "2":
            amount = float(input("Enter the amount spent: "))
            expenditures.append({
                "Type": "Miscellaneous",
                "Amount": amount,
                "Description": input("Enter a description for the expenditure: ")
            })
            print("Miscellaneous expenditure updated.")
            time.sleep(1)
        elif choice == "3":
            print_expenditure_report()  # Call the report function
        elif choice == "4":
            go_back(main_menu, "User    ")  # Pass the username to go back
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

def print_expenditure_report():
    clear_console()
    print("Expenditure Report")
    print("1. View All Expenditures")
    print("2. Go Back")

    choice = input("Select an option: ")
    if choice == "1":
        if expenditures:
            for exp in expenditures:
                print(f"Type: {exp['Type']}, VIN: {exp['VIN']}, Amount: ${exp['Amount']:.2f}, Description: {exp['Description']}")
            save_choice = input("\nSave this report as a PDF? (y/n): ").lower()
            if save_choice == "y":
                save_report_to_pdf("Expenditure Report", [f"Type: {exp['Type']}, VIN: {exp['VIN']}, Amount: ${exp['Amount']:.2f}, Description: {exp['Description']}" for exp in expenditures], "expenditure_report.pdf")
        else:
            print("No expenditures found.")
    elif choice == "2":
        go_back(add_expenditure, "User    ")  # Go back to the add expenditure menu
    else:
        print("Invalid choice. Please try again.")
        time.sleep(1)

def sell_car():
    while True:
        clear_console()
        print("Sell Car Page")
        print("1. Mark a car as sold")
        print("2. Go Back")

        choice = input("Select an option: ")
        if choice == "1":
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
                time.sleep(1)
            else:
                print("Car not found or already sold.")
                time.sleep(1)
        elif choice == "2":
            go_back(main_menu, "User    ")  # Pass the username to go back
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

def import_inventory():
    global inventory
    while True:
        clear_console()
        print("Import Inventory Page")
        file_path = input("Enter the file path of the Excel file to import: ")

        try:
            imported_data = pd.read_excel(file_path).to_dict('records')
            inventory.extend(imported_data)
            save_data()
            print(f"Successfully imported {len(imported_data)} vehicles into inventory.")
        except Exception as e:
            print(f"Error importing file: {e}")

        if input("Go back? (y/n): ").lower() == 'y':
            break

def print_reports():
    while True:
        clear_console()
        print("Print Reports Page")
        print("1. View All Inventory")
        print("2. Report by VIN")
        print("3. Report by Total Sales")
        print("4. Go Back")

        choice = input("Select an option: ")
        if choice == "1":
            if os.path.exists(INVENTORY_FILE):
                inventory_data = pd.read_excel(INVENTORY_FILE).to_dict('records')
                if not inventory_data:
                    print("No vehicles found in inventory.")
                else:
                    report_content = []
                    total_value = 0.0
                    for idx, car in enumerate(inventory_data, start=1):
                        report_content.append(
                            f"{idx}.\n"
                            f"Name: {car.get('Name', 'N/A')}\n"
                            f"Model: {car.get('Model', 'N/A')}\n"
                            f"Type: {car.get('Type', 'N/A')}\n"
                            f"Year: {car.get('Year', 'N/A')}\n"
                            f"VIN: {car.get('VIN', 'N/A')}\n"
                            f"Mileage: {car.get('Mileage', 'N/A')}\n"
                            f"Faults: {', '.join(car.get('Faults', []))}\n"
                            f"Price: ${car.get('Price', 0.0):.2f}\n"
                            f"Sold: {car.get('Sold', False)}\n"
                        )
                        total_value += car.get('Price', 0.0)
                    print("\n".join(report_content))
                    print(f"Total Inventory Value: ${total_value:.2f}")
                    save_choice = input("\nSave this report as a PDF? (y/n): ").lower()
                    if save_choice == "y":
                        save_report_to_pdf("Inventory Report", report_content, "inventory_report.pdf")
            else:
                print("Inventory file not found.")
            input("\nPress Enter to return to the reports menu.")
        elif choice == "2":
            vin = input("Enter VIN (full or last 6 digits): ").strip()
            inventory_data = pd.read_excel(INVENTORY_FILE).to_dict('records')
            car = next((c for c in inventory if vin in c["VIN"][-6:] or vin == c["VIN"]), None)
            if car:
                report_content = [
                    f"Name: {car.get('Name', 'N/A')}\n",
                    f"Model: {car.get('Model', 'N/A')}\n",
                    f"Type: {car.get('Type', 'N/A')}\n",
                    f"Year: {car.get('Year', 'N/A')}\n",
                    f"VIN: {car.get('VIN', 'N/A')}\n",
                    f"Mileage: {car.get('Mileage', 'N/A')}\n",
                    f"Faults: {', '.join(car.get('Faults', []))}\n",
                    f"Price: ${car.get('Price', 0.0):.2f}\n",
                    f"Sold: {car.get('Sold', False)}"
                ]
                print("".join(report_content))
                save_choice = input("\nSave this report as a PDF? (y/n): ").lower()
                if save_choice == "y":
                    save_report_to_pdf(f"Report for VIN {vin}", report_content, "vin_report.pdf")
            else:
                print("No vehicle found with the provided VIN.")
            input("\nPress Enter to return to the reports menu.")
        elif choice == "3":
            sold_data = pd.read_excel(SOLD_CARS_FILE).to_dict('records')
            total_sales = sum(car.get("SalesPrice", 0.0) for car in sold_data)
            total_tax = sum(car.get("Tax", 0.0) for car in sold_data)
            total_profit = sum(car.get("Profit", 0.0) for car in sold_data)

            report_content = [
                f"Total Sales: ${total_sales:.2f}\n",
                f"Total Tax: ${total_tax:.2f}\n",
                f"Total Profit: ${total_profit:.2f}"
            ]
            print("\n".join(report_content))
            save_choice = input("\nSave this report as a PDF? (y/n): ").lower()
            if save_choice == "y":
                save_report_to_pdf("Sales Summary Report", report_content, "sales_summary_report.pdf")
            input("\nPress Enter to return to the reports menu.")
        elif choice == "4":
            go_back(main_menu, "User     ")  # Pass the username to go back
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

def view_inventory(show_all=False):
    while True:
        clear_console()
        print("View Inventory Page")

        # Reload inventory from inventory.xlsx
        if os.path.exists(INVENTORY_FILE):
            inventory_data = pd.read_excel(INVENTORY_FILE).to_dict('records')
        else:
            print("No inventory data found.")
            if input("Go back? (y/n): ").lower() == 'y':
                break
            continue

        inventory_to_display = inventory_data if show_all else [car for car in inventory_data if not car.get("Sold", False)]

        if not inventory_to_display:
            print("No vehicles to display.")
        else:
            for idx, car in enumerate(inventory_to_display, start=1):
                print(
                    f"{idx}.\n"
                    f"   Name: {car.get('Name', 'N/A')}\n"
                    f"   Model: {car.get('Model', 'N/A')}\n"
                    f"   Type: {car.get('Type', 'N/A')}\n"
                    f"   Year: {car.get('Year', 'N/A')}\n"
                    f"   VIN: {car.get('VIN', 'N/A')}\n"
                    f"   Mileage: {car.get('Mileage', 'N/A')}\n"
                    f"   Faults: {', '.join(car.get('Faults', []))}\n"
                    f"   Price: ${car.get('Price', 0.0):.2f}\n"
                    f"   Sold: {car.get('Sold', False)}\n"
                )

        if input("Go back? (y/n): ").lower() == 'y':
            break

def save_report_to_pdf(report_title, report_content, filename="report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Times New Roman", size=12)
    
    pdf.set_font("Times New Roman", style="B", size=16)
    pdf.cell(0, 10, report_title, ln=True, align="C")
    pdf.ln(10)  # Add a line break

    pdf.set_font("Arial", size=12)
    for line in report_content:
        pdf.multi_cell(0, 10, line)
    
    output_path = os.path.join(os.getcwd(), filename)
    pdf.output(output_path)
    print(f"\nReport saved as PDF: {output_path}")

def main_menu(username):
    while True:
        clear_console()
        print(f"\nWelcome {username}")
        print("What would you like to do?:")
        print("1. Add Inventory")
        print("2. Update Inventory")
        print("3. Add Expenditures")
        print("4. Print Reports")
        print("5. Sold Cars")
        print("6. View Current Inventory")
        print("7. View All Inventory")
        print("8. Import Inventory from Excel")
        print("9. Sign Out")  # Changed exit to sign out

        choice = input("Enter your choice: ")

        if choice == "1":
            add_inventory()
        elif choice == "2":
            update_inventory()
        elif choice == "3":
            add_expenditure()
        elif choice == "4":
            print_reports()
        elif choice == "5":
            sell_car()
        elif choice == "6":
            view_inventory()
        elif choice == "7":
            view_inventory(show_all=True)
        elif choice == "8":
            import_inventory()
        elif choice == "9":
            show_transition("Signing out...")
            save_data()  # Save data before signing out
            user_login()
            break
        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    load_data()
    user_login()
    main_menu("User  ")  # Enter the main menu with a default username
