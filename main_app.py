import sys
import os 
import csv
from datetime import datetime

from inventory_manager import (
    show_inventory_catalog, lookup_item_by_id, lookup_item_by_name,
    generate_next_item_id, register_new_item, modify_item_details,
    extract_item_price, extract_item_stock
)
from transaction_processor import (
    record_new_transaction, display_transaction_records,
    search_transactions_by_date, search_transactions_by_product_name,
    search_transactions_by_product_name_and_date,
    display_overall_monthly_sales_graphs,
    display_product_monthly_sales_graphs,
    display_product_total_sales_bar_chart
)
def standardize_csv_data(file_obj, required_fields): #before loading
    try:
        csv_reader = csv.DictReader(file_obj)
        standardized_records = []
        for entry in csv_reader:
            sanitized_entry = {}
            for header, val in entry.items():
                if header is not None:
                    processed_header = header.strip().lower().replace('\ufeff', '')
                    if processed_header in required_fields:
                        sanitized_entry[processed_header] = val.strip() if isinstance(val, str) else val
            if any(field in sanitized_entry for field in required_fields):
                standardized_records.append(sanitized_entry)
        return standardized_records

    except Exception as err:
        raise Exception(f"Data standardization failed: {err}")

def persist_system_data(transactions_file, inventory_file, transaction_records, inventory_records):
    print("\n======")
    try:
        transaction_columns = ['date', 'time', 'id', 'quantity', 'payment']
        with open(transactions_file, 'w', newline='', encoding='utf-8') as file_stream:
            csv_writer = csv.DictWriter(file_stream, fieldnames=transaction_columns)
            csv_writer.writeheader()
            csv_writer.writerows(transaction_records)
        print(f"Transaction history written '{transactions_file}'.")
    except Exception as err:
        print(f"file save failed: {err}")

    try:
        inventory_columns = ['id', 'name', 'price', 'stock']
        with open(inventory_file, 'w', newline='', encoding='utf-8') as file_stream:
            csv_writer = csv.DictWriter(file_stream, fieldnames=inventory_columns)
            csv_writer.writeheader()
            csv_writer.writerows(inventory_records)
        print(f"Inventory database written to '{inventory_file}'.")
    except Exception as err:
        print(f"Inventory file save failed: {err}")

def initialize_system_data(transactions_file, inventory_file, credentials_file): #loading the data , #standardize
    transaction_records = []
    inventory_records = []
    credential_database = {}
    
    TRANSACTION_FIELDS = ['date', 'time', 'id', 'quantity', 'payment'] 
    INVENTORY_FIELDS = ['id', 'name', 'price', 'stock']
    CREDENTIAL_FIELDS = ['username', 'password', 'type']
    try:
        if os.path.exists(inventory_file) and os.stat(inventory_file).st_size > 0:
            with open(inventory_file, 'r', newline='', encoding='utf-8-sig') as file_stream:
                inventory_records = standardize_csv_data(file_stream, INVENTORY_FIELDS)
        else:
            print(f"Inventory file '{inventory_file}' not found or is empty. Starting with empty inventory.")
    except Exception as err:
        print(f"Failed to read inventory file '{inventory_file}': {err}. Starting with empty inventory.")
    try:
        if os.path.exists(transactions_file) and os.stat(transactions_file).st_size > 0:
            with open(transactions_file, 'r', newline='', encoding='utf-8-sig') as file_stream:
                transaction_records = standardize_csv_data(file_stream, TRANSACTION_FIELDS)
    except Exception as err:
        print(f"Failed to read transactions file '{transactions_file}': {err}. Starting with no transactions.")

    try:
        with open(credentials_file, 'r', newline='', encoding='utf-8-sig') as file_stream:
            credential_list = standardize_csv_data(file_stream, CREDENTIAL_FIELDS)
            for entry in credential_list:
                username = entry.get('username')
                if username:
                    credential_database[username] = {
                        'password': entry.get('password'), 
                        'type': entry.get('type')
                    }


    except FileNotFoundError:
        print(f"CRITICAL: Credentials file '{credentials_file}' is missing. System cannot start without authentication data.")
        sys.exit(1)
    except Exception as err:
        print(f"Failed to read credentials file '{credentials_file}': {err}")
        sys.exit(1)

    return transaction_records, inventory_records, credential_database
def authenticate_user(credential_database):
    print("\n=== User Authentication System ===")
    
    if not credential_database:
        print("Authentication database is empty. Terminating.")
        return None, None
        
    RETRY_LIMIT = 3
    for attempt_number in range(RETRY_LIMIT):
        user_input = input("Username: ").strip()
        pass_input = input("Password: ").strip()
        
        if ((user_input in credential_database) and (credential_database[user_input]['password'] == pass_input)):
            access_level = credential_database[user_input]['type']
            print(f"\nAuthentication successful! Greetings, {user_input} [Role: {access_level}].")
            return user_input, access_level
        else:
            print("Authentication failed. Please try again.")
            
    print("Login attempt limit exceeded. Exiting system.")
    sys.exit(0)

def staff_interface(transaction_records, inventory_records):
    while True:
        print("\n╔═════════════════════════════════════╗")
        print("║          STAFF DASHBOARD            ║")
        print("╠═════════════════════════════════════╣")
        print("║ 1. Process Transaction              ║")
        print("║ 2. View Product Catalog             ║")
        print("║ 3. Search Sales by Date             ║")
        print("║ 4. Search Sales by Product Name     ║")
        print("║ 5. Search Sales by Product & Date   ║")
        print("║ 6. Sign Out & Save                  ║")
        print("╚═════════════════════════════════════╝")
        
        selection = input("Select option: ").strip()
        
        if selection == '1':
            record_new_transaction(transaction_records, inventory_records, lookup_item_by_id, extract_item_price, extract_item_stock, show_inventory_catalog)
        elif selection == '2':
            show_inventory_catalog(inventory_records)
        elif selection == '3':
            search_transactions_by_date(transaction_records)
        elif selection == '4':
            search_transactions_by_product_name(transaction_records, inventory_records, lookup_item_by_name)
        elif selection == '5':
            search_transactions_by_product_name_and_date(transaction_records, inventory_records, lookup_item_by_name)
        elif selection == '6':
            return
        else:
            print("Invalid selection.")

def supervisor_interface(transaction_records, inventory_records):
    while True:
        print("\n╔═════════════════════════════════════╗")
        print("║        SUPERVISOR DASHBOARD         ║")
        print("╠═════════════════════════════════════╣")
        print("║ 1. Process Transaction              ║")
        print("║ 2. Register New Product             ║")
        print("║ 3. Modify Product Details           ║")
        print("║ 4. View Product Catalog             ║")
        print("║ 5. Search Sales by Date             ║")
        print("║ 6. Search Sales by Product Name     ║")
        print("║ 7. Search Sales by Product & Date   ║")
        print("║ 8. Display Overall Monthly Sales    ║")
        print("║ 9. Display Product Monthly Sales    ║")
        print("║ 10. Display Product Total Sales     ║")
        print("║ 11. Sign Out & Save                 ║")
        print("╚═════════════════════════════════════╝")
        
        selection = input("Select option: ").strip()
        
        if selection == '1':
            record_new_transaction(transaction_records, inventory_records, lookup_item_by_id, extract_item_price, extract_item_stock, show_inventory_catalog)
        elif selection == '2':
            register_new_item(inventory_records, generate_next_item_id)
        elif selection == '3':
            modify_item_details(inventory_records, show_inventory_catalog, lookup_item_by_id, lookup_item_by_name)
        elif selection == '4':
            show_inventory_catalog(inventory_records)
        elif selection == '5':
            search_transactions_by_date(transaction_records)
        elif selection == '6':
            search_transactions_by_product_name(transaction_records, inventory_records, lookup_item_by_name)
        elif selection == '7':
            search_transactions_by_product_name_and_date(transaction_records, inventory_records, lookup_item_by_name)
        elif selection == '8':
            display_overall_monthly_sales_graphs(transaction_records)
        elif selection == '9':
            display_product_monthly_sales_graphs(transaction_records, inventory_records, show_inventory_catalog, lookup_item_by_id)
        elif selection == '10':
            display_product_total_sales_bar_chart(transaction_records, inventory_records, lookup_item_by_id)
        elif selection == '11':
            return
        else:
            print("Invalid selection.")



def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    transactions_file = sys.argv[1]
    inventory_file = sys.argv[2]

    transaction_records, inventory_records, credential_database = initialize_system_data(
        transactions_file, 
        inventory_file, 
        "users.csv"
    )
    while True:
        user_input, access_level = authenticate_user(credential_database)
        
        if access_level == 'manager':
            supervisor_interface(transaction_records, inventory_records)
        elif access_level == 'assistant':
            staff_interface(transaction_records, inventory_records)
        else:
            print("Unknown access level. Exiting.")
            sys.exit(1)

        print(f"\n>>> Goodbye, {user_input}! <<<")
        persist_system_data(transactions_file, inventory_file, transaction_records, inventory_records) 
        break 

if __name__ == "__main__":
    main()