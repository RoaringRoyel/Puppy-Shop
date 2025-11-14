from datetime import datetime 

def extract_item_price(item):
    try:
        return float(item.get('price', 0))
    except (ValueError, TypeError):
        return 0.0

def extract_item_stock(item):
    try:
        return int(float(item.get('stock', 0))) 
    except (ValueError, TypeError):
        return 0

def lookup_item_by_id(inventory_records, item_id):
    for item in inventory_records:
        if str(item.get('id')) == str(item_id):
            return item
    return None

def lookup_item_by_name(inventory_records, item_name_query):
    matching_items = []
    normalized_query = item_name_query.strip().lower()
    if not normalized_query:
        return []

    for item in inventory_records:
        item_name = item.get('name', '').lower()
        if normalized_query in item_name:
            matching_items.append(item)
    return matching_items


def generate_next_item_id(inventory_records):
    if not inventory_records:
        return "1"
    
    highest_id_value = 0
    for item in inventory_records:
        item_id_string = str(item.get('id', ''))
        try:
            if item_id_string.upper().startswith('P') and item_id_string[1:].isdigit():
                highest_id_value = max(highest_id_value, int(item_id_string[1:]))
            elif item_id_string.isdigit():
                 highest_id_value = max(highest_id_value, int(item_id_string))
        except ValueError:
            pass
    return str(highest_id_value + 1)


def show_inventory_catalog(inventory_records):
    """Displays the current inventory catalog."""
    print("\n=== Product Catalog ===")
    if not inventory_records:
        print("Catalog is empty - no items available.")
        return
    print(f"{'ID':<6} {'NAME':<25} {'STOCK':<8} {'PRICE':<10}")
    print("=" * 60)
    for item in inventory_records:
        item_id = item.get('id', 'N/A')
        item_name = item.get('name', 'Unnamed')
        item_stock = item.get('stock', '0')
        item_price = item.get('price', '0.00')
        print(f"{item_id:<6} {item_name:<25} {item_stock:<8} ${float(item_price):<9.2f}")
    print("=" * 60)

def register_new_item(inventory_records, generate_next_id_func):
    auto_id = generate_next_id_func(inventory_records)
    print(f"System-Generated Product ID: {auto_id}")
    item_name = input("Product Name: ").strip()
    if not item_name:
        print("Product name is required.")
        return
    if any(item.get('name', '').lower() == item_name.lower() for item in inventory_records):
        print(f"A product with the name '{item_name}' already exists.")
        return
    try:
        unit_price = float(input("Price per Unit: ").strip())
        if unit_price <= 0:
            print("Price must be a positive value.")
            return
    except ValueError:
        print("Invalid price format. Must be numeric.")
        return
    try:
        initial_stock = int(input("Initial Stock Quantity: ").strip())
        if initial_stock < 0:
            print("Stock quantity cannot be negative.")
            return
    except ValueError:
        print("Error")
        return
    new_inventory_item = {
        'id': auto_id,
        'name': item_name,
        'price': f"{unit_price:.2f}",
        'stock': str(initial_stock)
    }
    inventory_records.append(new_inventory_item)
    print(f"Product '{item_name}' (ID: {auto_id}) has been registered in the system!")

def modify_item_details(inventory_records, show_catalog_func, lookup_id_func, lookup_name_func):
    print("\n=== Product Details Modification ===")
    
    if not inventory_records:
        print("No products available ")
        return

    show_catalog_func(inventory_records)
    
    item_identifier = input("Enter Product ID or Name to Modify: ").strip()
    
    item_to_modify = None
    item_to_modify = lookup_id_func(inventory_records, item_identifier)

    if not item_to_modify:
        matching_items_by_name = lookup_name_func(inventory_records, item_identifier)
        
        if not matching_items_by_name:
            print(f"No product found matching '{item_identifier}' by ID or Name.")
            return
        elif len(matching_items_by_name) > 1:
            print("Multiple products found matching that name:")
            for idx, item in enumerate(matching_items_by_name):
                print(f"  {idx + 1}. ID: {item.get('id')}, Name: {item.get('name')}")
            
            while True:
                try:
                    choice = int(input("Enter the number of the product you want to modify: ").strip())
                    if 1 <= choice <= len(matching_items_by_name):
                        item_to_modify = matching_items_by_name[choice - 1]
                        break
                    else:
                        print("Invalid choice. Please enter a number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else: 
            item_to_modify = matching_items_by_name[0]

    if not item_to_modify: 
        print("Could not identify product for modification.")
        return

    print(f"\n--- Modifying: {item_to_modify['name']} (ID: {item_to_modify['id']}) ---")
    print(f"  Current Price: ${float(item_to_modify.get('price', '0.00')):.2f}")
    print(f"  Current Stock: {item_to_modify.get('stock', '0')}")

    updated_price = input("Enter New Price: ").strip()
    if updated_price:
        try:
            price_value = float(updated_price)
            if price_value <= 0:
                print("Price must be positive. ")
            else:
                item_to_modify['price'] = f"{price_value:.2f}"
                print(f"Price modified to ${item_to_modify['price']}")
        except ValueError:
            print("Invalid price input. ")
            
    updated_stock = input("Enter New Stock Quantity: ").strip()
    if updated_stock:
        try:
            stock_value = int(updated_stock)
            if stock_value < 0:
                print("Stock quantity must be non-negative.")
            else:
                item_to_modify['stock'] = str(stock_value)
                print(f"Stock modified to {item_to_modify['stock']} units")
        except ValueError:
            print("Invalid stock input. Stock modification cancelled.")
    
    print(f"Modification for '{item_to_modify['name']}' complete.")