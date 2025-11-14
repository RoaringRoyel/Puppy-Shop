from datetime import datetime
import calendar
import numpy as np
import matplotlib.pyplot as plt

def display_transaction_records(transactions, title=""):
    print(f"\n=== {title if title else 'Sales Records'} ===")
    if not transactions:
        print("No matching found.")
        return
    print(f"{'DATE':<12} {'TIME':<10} {'PROD_ID':<9} {'QUANTITY':<10} {'AMOUNT':<10}")
    print("=" * 60)
    for t in transactions:
        t_date = t.get('date', 'N/A')
        t_time = t.get('time', 'N/A')
        t_id = t.get('id', 'N/A')
        t_qty = t.get('quantity', '0')
        t_payment = float(t.get('payment', '0.00'))
        print(f"{t_date:<12} {t_time:<10} {t_id:<9} {t_qty:<10} ${t_payment:<9.2f}")
    print("=" * 60)

def record_new_transaction(transaction_records, inventory_records, lookup_item_by_id_func, extract_item_price_func, extract_item_stock_func, show_inventory_catalog_func):
    print("\n======")
    
    if not inventory_records:
        print("Database is empty.")
        return

    show_inventory_catalog_func(inventory_records)
    item_id = input("\nEnter Product ID to purchase: ").strip()
    item = lookup_item_by_id_func(inventory_records, item_id)
    
    if not item:
        print(f"Item ID '{item_id}' not found in inventory.")
        return
    
    unit_cost = extract_item_price_func(item)
    available_quantity = extract_item_stock_func(item)
    
    try:
        sold_quantity = int(input(f"Enter quantity to purchase for '{item.get('name')}': ").strip())
        if sold_quantity <= 0:
            print("Quantity must be greater than zero. Transaction terminated.")
            return
    except ValueError:
        print("Invalid input. Quantity must be an integer. Transaction terminated.")
        return

    if sold_quantity > available_quantity:
        print(f"Stock insufficient. Transaction terminated.")
        return
    total_amount = round(sold_quantity * unit_cost, 2)
    print(f"\n##### Summary #####")
    print(f"Item: {item['name']}")
    print(f"Quantity: {sold_quantity}")
    print(f"Unit Price: ${unit_cost:.2f}")
    print(f"Transaction Total (Amount Collected): ${total_amount:.2f}")

    current_datetime = datetime.now()
    transaction_date = current_datetime.strftime("%d/%m/%Y") 
    transaction_time = current_datetime.strftime("%H:%M:%S")

    new_transaction = {
        'date': transaction_date,
        'time': transaction_time,
        'id': item_id,
        'quantity': str(sold_quantity), 
        'payment': f"{total_amount:.2f}" 
    }
    transaction_records.append(new_transaction)
    item['stock'] = str(available_quantity - sold_quantity)
    print(f"Transaction recorded successfully! Updated inventory for {item['name']}: {item['stock']} units remaining.")
def search_transactions_by_date(transaction_records):
    print("\n##### Search Sales Records by Date #####")
    search_date_input_str = input("Enter date to search (DD/MM/YYYY): ").strip()
    search_date_obj = None
    try:
        search_date_obj = datetime.strptime(search_date_input_str, "%d/%m/%Y").date()
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return
    search_date_formatted_for_comparison = search_date_obj.strftime("%d/%m/%Y")
    matching_transactions = []
    for t in transaction_records:
        transaction_date_str = t.get('date') 
        if transaction_date_str == search_date_formatted_for_comparison:
            matching_transactions.append(t)
    display_transaction_records(matching_transactions, f"Sales Records for {search_date_formatted_for_comparison}")

def search_transactions_by_product_name(transaction_records, inventory_records, lookup_item_by_name_func):
    print("\n##### Search Sales Records by Product Name ##### ")
    product_name_query = input("Enter product name (partial match allowed): ").strip().lower()

    if not product_name_query:
        print("Product name query cannot be empty.")
        return
    matching_inventory_items = lookup_item_by_name_func(inventory_records, product_name_query)
    if not matching_inventory_items:
        print(f"No products found matching '{product_name_query}'.")
        return
    matching_product_ids = {item['id'] for item in matching_inventory_items}
    matching_transactions = [
        t for t in transaction_records if t.get('id') in matching_product_ids
    ]
    display_transaction_records(matching_transactions, f"Sales Records for Product Name containing '{product_name_query}'")

def search_transactions_by_product_name_and_date(transaction_records, inventory_records, lookup_item_by_name_func):
    print("\n##### Search Sales Records by Product Name and Date Range #####")
    product_name_query = input("Enter product name: ").strip().lower()
    
    start_date_str = input("Enter start date (DD/MM/YYYY): ").strip()
    end_date_str = input("Enter end date (DD/MM/YYYY): ").strip()

    start_date_obj = None
    end_date_obj = None

    try:
        start_date_obj = datetime.strptime(start_date_str, "%d/%m/%Y").date()
        end_date_obj = datetime.strptime(end_date_str, "%d/%m/%Y").date()
        if start_date_obj > end_date_obj:
            print("Start date cannot be after end date. Search cancelled.")
            return
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY. Search cancelled.")
        return

    matching_inventory_items = []
    if product_name_query: 
        matching_inventory_items = lookup_item_by_name_func(inventory_records, product_name_query)
    else: 
        matching_inventory_items = inventory_records 
    
    if not matching_inventory_items and product_name_query:
        print(f"No products found matching '{product_name_query}'. Search cancelled.")
        return
    
    matching_product_ids = {item['id'] for item in matching_inventory_items}

    filtered_transactions = []
    for t in transaction_records:
        transaction_date_str = t.get('date') 
        if transaction_date_str and t.get('id') in matching_product_ids:
            try:
                transaction_date_obj = datetime.strptime(transaction_date_str, "%d/%m/%Y").date()
                
                if start_date_obj <= transaction_date_obj <= end_date_obj:
                    filtered_transactions.append(t)
            except ValueError:
                print(f"Warning: Skipping transaction with malformed date '{transaction_date_str}' (ID: {t.get('id')}).")
                pass
    display_transaction_records(
        filtered_transactions, 
        f"Sales for '{product_name_query if product_name_query else 'All Products'}' between {start_date_str} and {end_date_str}"
    )

def get_month_year_input(prompt_prefix):
    while True:
        month_year_str = input(f"Enter {prompt_prefix} month and year (MM/YYYY): ").strip()
        try:
            month_year_obj = datetime.strptime(month_year_str, "%m/%Y")
            return month_year_obj.year, month_year_obj.month
        except ValueError:
            print("Invalid format. Please use MM/YYYY.")

def display_overall_monthly_sales_graphs(transaction_records):
    print("\n##### Display Overall Monthly Sales Performance #####")
    
    start_year, start_month = get_month_year_input("start")
    end_year, end_month = get_month_year_input("end")

    if not transaction_records:
        print("No transactions available to generate graphs.")
        return
    monthly_data = {}
    for t in transaction_records:
        try:
            transaction_date_str = t.get('date')
            transaction_date_obj = datetime.strptime(transaction_date_str, "%d/%m/%Y")
            
            year = transaction_date_obj.year
            month = transaction_date_obj.month
            
            if (year > start_year or (year == start_year and month >= start_month)) and \
               (year < end_year or (year == end_year and month <= end_month)):
                
                key = (year, month)
                monthly_data.setdefault(key, {'sales_value': 0.0, 'num_sales': 0})
                
                monthly_data[key]['sales_value'] += float(t.get('payment', 0.0))
                monthly_data[key]['num_sales'] += 1
        except (ValueError, TypeError):
            continue

    if not monthly_data:
        print("No sales data found for the specified month range.")
        return
    sorted_months = sorted(monthly_data.keys())
    months_labels = [f"{calendar.month_abbr[m[1]]} {m[0]}" for m in sorted_months]
    sales_values = [monthly_data[m]['sales_value'] for m in sorted_months]
    num_sales = [monthly_data[m]['num_sales'] for m in sorted_months]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Month')
    ax1.set_ylabel('Total Sales Value ($)', color='tab:blue')
    ax1.plot(months_labels, sales_values, color='tab:blue', marker='o', label='Total Sales Value')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()  
    ax2.set_ylabel('Number of Sales', color='tab:red')  
    ax2.plot(months_labels, num_sales, color='tab:red', marker='x', linestyle='--', label='Number of Sales')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'Overall Monthly Sales Performance ({start_month}/{start_year} - {end_month}/{end_year})')
    
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    fig.tight_layout() 
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def display_product_monthly_sales_graphs(transaction_records, inventory_records, show_inventory_catalog_func, lookup_item_by_id_func):
    print("\n##### Display Monthly Sales Performance for a Specific Product #####")
    
    if not inventory_records:
        print("Inventory is empty.")
        return
    show_inventory_catalog_func(inventory_records)
    product_id = input("\nEnter Product ID to analyze: ").strip()
    product = lookup_item_by_id_func(inventory_records, product_id)
    if not product:
        print(f"Product ID '{product_id}' not found.")
        return
    product_name = product.get('name', f"Product {product_id}")
    start_year, start_month = get_month_year_input("start")
    end_year, end_month = get_month_year_input("end")
    monthly_product_data = {}

    for t in transaction_records:
        try:
            if t.get('id') == product_id:
                transaction_date_str = t.get('date')
                transaction_date_obj = datetime.strptime(transaction_date_str, "%d/%m/%Y") 
                
                year = transaction_date_obj.year
                month = transaction_date_obj.month
                
                if (year > start_year or (year == start_year and month >= start_month)) and \
                   (year < end_year or (year == end_year and month <= end_month)):
                    
                    key = (year, month)
                    monthly_product_data.setdefault(key, {'sales_value': 0.0, 'num_sales': 0})
                    
                    monthly_product_data[key]['sales_value'] += float(t.get('payment', 0.0))
                    monthly_product_data[key]['num_sales'] += int(t.get('quantity', 0)) 
        except (ValueError, TypeError):
            continue

    if not monthly_product_data:
        print(f"No sales data found for '{product_name}' in the specified month range.")
        return
    
    sorted_months = sorted(monthly_product_data.keys())
    
    months_labels = [f"{calendar.month_abbr[m[1]]} {m[0]}" for m in sorted_months]
    sales_values = [monthly_product_data[m]['sales_value'] for m in sorted_months]
    num_sales = [monthly_product_data[m]['num_sales'] for m in sorted_months]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Month')
    ax1.set_ylabel('Total Sales Value ($)', color='tab:blue')
    ax1.plot(months_labels, sales_values, color='tab:blue', marker='o', label='Total Sales Value')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()  
    ax2.set_ylabel('Total Quantity Sold', color='tab:red')  
    ax2.plot(months_labels, num_sales, color='tab:red', marker='x', linestyle='--', label='Total Quantity Sold')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'Monthly Sales Performance for {product_name} ({start_month}/{start_year} - {end_month}/{end_year})')
    
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    fig.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def display_product_total_sales_bar_chart(transaction_records, inventory_records, lookup_item_by_id_func):
    print("\n=== Display Total Sales Value Per Product (Bar Chart) ===")
    
    start_date_str = input("Enter start date (DD/MM/YYYY): ").strip()
    end_date_str = input("Enter end date (DD/MM/YYYY): ").strip()

    start_date_obj = None
    end_date_obj = None

    try:
        start_date_obj = datetime.strptime(start_date_str, "%d/%m/%Y").date()
        end_date_obj = datetime.strptime(end_date_str, "%d/%m/%Y").date()
        if start_date_obj > end_date_obj:
            print("Start date cannot be after end date. Chart cancelled.")
            return
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY. Chart cancelled.")
        return
    product_sales_totals = {}

    for t in transaction_records:
        try:
            transaction_date_str = t.get('date')
            transaction_date_obj = datetime.strptime(transaction_date_str, "%d/%m/%Y").date()
            
            if start_date_obj <= transaction_date_obj <= end_date_obj:
                product_id = t.get('id')
                sales_payment = float(t.get('payment', 0.0))
                
                product_sales_totals.setdefault(product_id, 0.0)
                product_sales_totals[product_id] += sales_payment
        except (ValueError, TypeError):
            continue

    if not product_sales_totals:
        print("No sales data found for the specified date range.")
        return

    product_names_and_values = []
    for prod_id, total_value in product_sales_totals.items():
        product = lookup_item_by_id_func(inventory_records, prod_id)
        product_name = product.get('name', f"Unknown Product (ID: {prod_id})") if product else f"Unknown Product (ID: {prod_id})"
        product_names_and_values.append({'name': product_name, 'value': total_value})

    sorted_products = sorted(product_names_and_values, key=lambda x: x['value'], reverse=True)

    product_names = [p['name'] for p in sorted_products]
    total_values = [p['value'] for p in sorted_products]

    plt.figure(figsize=(12, 6))
    plt.bar(product_names, total_values)
    plt.xlabel('Product')
    plt.ylabel('Total Sales Value ($)')
    plt.title(f'Total Sales Value per Product ({start_date_str} - {end_date_str})')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
