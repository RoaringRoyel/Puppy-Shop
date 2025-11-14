# All For My Puppy - Sales Management System


---

DBMS provides several advantages for data management and handling complex scenarios. However, in some cases, using DBMS adds unnecessary cost and complexity for small tasks.  
Specially when you have:  
- Limited users  
- Small scale of data  
- Well defined structured  
- Few functionalities  

In such cases, a designer focuses on **usability and cost-effectiveness**. Designing and handling a huge conceptual schema and maintaining a complex database is unnecessary.

In case of **File System:**  
Even though implementation is easy, it comes with limitations:  
- Data Redundancy  
- Data Inconsistency  
- Data Integrity  
- Poor Security  
- Inability to handle transactions  
- No data independence  

Despite these limitations, for this small scale project, the **File System Approach** was chosen due to its simplicity and suitability. Measures were taken to overcome some limitations.

---

## 🐶 Project Overview

**All For My Puppy** is a complete **sales management system** for a pet shop.  
Features include:  

- Managing puppy products  
- Recording sales transactions  
- User login with role-based access  
- Updating all information in CSV files  
- Advanced search for sales by date, product, or time period  
- Graphical analysis (monthly line graphs and bar charts) using `matplotlib`  

Developed in Python using **modular design principles** and approved libraries such as `csv`, `numpy`, and `matplotlib`.

**Interface:** Both **CLI** and **GUI**.

---

## 📂 Files

| File | Description |
|------|-------------|
| `puppy.csv` | Stores product inventory |
| `sales.csv` | Stores sales transactions |
| `users.csv` | Stores user credentials |
| `main_app.py` | Controller (Routes, Authenticates, Loads data) |
| `inventory_manager.py` | Model (Product management & inventory operations) |
| `transaction_processor.py` | Model (Transactions & Analytics) |

---

## ⚙ Functional Requirements

- Load Required Data  
- User Login & Role-based Access  
- Display Menu  
- Enter Sales Records  
- Display Products  

**Manager Role Only:**  
- Add or Modify a Product  
- Search Sales by Date / Name / Time Period  
- Graphical Analysis (Monthly / Product-wise / Total Sales)

---

## 📝 Non-Functional Requirements

- Usability  
- Performance  
- User Interface  
- Data Integrity  
- Redundancy Control  
- Security  
- Readability and Documentation  
- Portability  

---

## 🔧 Handling File System Limitations
**Data Persistancy:**  
- `persist_system_data(transactions_file, inventory_file, transaction_records, inventory_records)` ensures:
  - Ensures all in-memory changes are persisted at logout or program exit
  - Combined with data integrity, guarantees consistent and reliable stored data 
  - Saves all sales transactions to sales.csv
  - Saves all inventory changes to puppy.csv
 
**Data Integrity:**  
- `standardize_csv_data(file_obj, required_fields)` ensures:
  - Headers are normalized  
  - Records missing required fields are rejected  
  - Values are cleared and trimmed  
  - BOM issues handled  

**Redundancy Control:**  
- `register_new_item(inventory_records, generate_next_id_func)`:
  - Prevents duplicate product names  
  - Ensures product IDs are unique (Auto Generated Primary Key)  

**Transactions:**  
- Multiple transactions at the same time create separate entities (timestamps ensure uniqueness)  

---

## 🔄 Data Flow / Project Flow

```text
       +-------------------+
       |     users.csv     |
       +---------+---------+
                 |
          (login info)
                 v
       +-------------------+
       |   main_app.py     |
       |   (Controller)    |
       +--------+----------+
      /         |          \
     v          v           v
+---------------+  +---------------+  +------------------+
| puppy.csv     |  | sales.csv     |  | inventory_manager|
+---------------+  +---------------+  +------------------+
         |                 |                  |
         +--------+--------+------------------+
                  |
          In-memory Data Structures
                  |
                  v
          +-------------------+
          | CLI / GUI Layer    |
          +-------------------+
                  |
                  v
     +-----------------------------+
     | transaction_processor.py    |
     +-----------------------------+
                  |
                  v
       Graphs & Reports (matplotlib)

```
---

## 📈 Graphical Analysis

- Overall monthly sales (line chart for total sales value and number of transactions)  
- Product-specific monthly sales  
- Total sales per product (bar chart)  

---

## 🖥 How to Run

### CLI Version
```bash
python main_app.py sales.csv puppy.csv
```
### GUI Version
```bash
python gui_app.py sales.csv puppy.csv users.csv
```
