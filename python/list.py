#Day 1- prodduct list with low stock a
import sqlite3
import os
import datetime

date = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

conn = sqlite3.connect("magic.db") #a some type of fstream
cursor = conn.cursor() #a pen where ables you to write commands

#clearscreen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



#PRODUCT LISTS =================================================
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS product ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            price REAL,
            stock INTEGER)
            """) #this is like a template for the db



products = [
    {"Product": "Coke", "Price": 25, "Stock": 50},
    {"Product": "Sprite", "Price": 25, "Stock": 50},
    {"Product": "Royal", "Price": 25, "Stock": 50},
    {"Product": "Pepsi", "Price": 25, "Stock": 50},
    {"Product": "Mountain Dew", "Price": 25, "Stock": 50},
    {"Product": "Dr. Pepper", "Price": 25, "Stock": 50},
]


cursor.execute("SELECT COUNT (*) FROM product")
count = cursor.fetchone()[0]
    



if count == 0:
    for product in products:
        cursor.execute("INSERT INTO product (product, price, stock) VALUES (?, ?, ?)",
                    (product["Product"], product["Price"], product["Stock"]))
        
        conn.commit()
#PRODUCT LISTS =================================================





#USERS =================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT)
            """)

users = [
    {"Username": "Staff1", "Password": "1234", "role": "staff"},
    {"Username": "Manager1", "Password": "admin", "role": "manager"},
        ]

cursor.execute("SELECT COUNT (*) FROM users")
count = cursor.fetchone()[0]

if count == 0:
    for user in users:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (user["Username"], user["Password"], user["role"]))
conn.commit()




def change_password():
    print("====================SYSTOCKS ACCOUNT INFORMATION====================")
    username = input("Input current username: ")
    password = input("Input current password: ")

    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result is None:
        print("Invald Credentials!")
        return None
    
    else:
        new_user = input("Input New Username: ")
        new_password = input("Input New Password: ")

        cursor.execute("UPDATE users SET username = ?, password = ? WHERE username = ?", (new_user, new_password, username))
        conn.commit()
        clear()
        print("Credentials updated successfully!")
        

    



def login():
    print("====================SYSTOCKS LOGIN====================")
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result is None:
        print("Invald Credentials!")
        return None
    
    return result[0]


#USERS =================================================






#SALES =================================================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            total REAL,
            date TEXT)
            """)



def view_sales():
    cursor.execute("SELECT * FROM sales ORDER BY date DESC") #gathers and red the data 
    results = cursor.fetchall()
    if len(results) == 0:
        print("No sales yet!")
        return

    print("=========================================")

    for row in results:
        print(row[1], "-", row[2], " ", row[3], "-", row[4], "-", row[5])
    
    print("=========================================")

#SALES =================================================================================





#PRoFIT REPORTS ====================================================================

def view_profit():
    cursor.execute("SELECT SUM(total) FROM sales")
    profit = cursor.fetchone()[0]
    if profit is None:
        print("No sales recorded yet!")
        return

    print("Total Profit: PHP", profit)


def view_inventory():
    cursor.execute("SELECT * FROM product ORDER BY product") #gathers and red the data 
    results = cursor.fetchall()
    if len(results) == 0:
        print("No products yet!")
        return
    

    print("=========================================")

    for row in results:
        if row[3] <= 10:
            status = "LOW STOCK!"

        else:
            status = "OK"

        print(row[1], "-", row[2], "-", row[3], status)

#PRoFIT REPORTS ====================================================================


#SEARCH FUNCTIOn ==============================================================

def search_product():
    search = input("Search Product Name: ")
    cursor.execute("SELECT * FROM product WHERE LOWER(product) = LOWER(?)", (search,))
    searching = cursor.fetchone()

    if searching is None:
            print("Produt Not Found!")
            return
        
    print(searching[1], "-", searching[2], "-", searching[3])


#SEARCH FUNCTIOn ==============================================================


#EDIT product price =============================================================
def edit_price():
    edit = input("Enter Product Name: ")
    cursor.execute("SELECT * FROM product WHERE LOWER(product) = LOWER(?)", (edit,))
    editing= cursor.fetchone()

    if editing is None:
            print("Produt Not Found!")
            return
        
    else:
        new_price = int(input("Input New Price of " + edit + " : "))
        cursor.execute("UPDATE product SET price = ? WHERE LOWER(product) = LOWER(?)", (new_price, edit))
        conn.commit()






#EDIT product price =============================================================



#FUNCTIONS ================================================================

def view_products():
    cursor.execute("SELECT * FROM product ORDER BY product") #gathers and red the data 
    results = cursor.fetchall()
    if len(results) == 0:
        print("No products yet!")
        return
    

    print("=========================================")

    for row in results:
        print(row[1], "-", row[2], "-", row[3], "left")
        
        if row[3] <= 10:
            print("Low Stock Alert:", row[1])

def add_product():
    print("=========================================")
    name = input("Input Product Name (0 to back): ").capitalize()
    if name == "0":
        return

    cursor.execute("SELECT COUNT(*) FROM product WHERE LOWER(product) = LOWER(?)", (name,))
    count = cursor.fetchone()[0] #grabs result just 1


    if count == 1:
        print("Product already exists")
        add = int(input("How many stock to add? (0 to back): "))
        if add == 0:
            return 
        cursor.execute("UPDATE product SET stock = stock + ? WHERE LOWER(product) = LOWER(?)", (add, name))
        conn.commit()

    else:
        price = float(input("Input Product Price: "))
        stock = int(input("Input Product Quantity: "))
        cursor.execute("INSERT INTO product (product, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()


def remove_product():
    print("=========================================")
    remove = input("Input product to remove (0 to back): ")
    if remove == "0":
        return
    
    confirm = input("Are you sure you want to remove " + remove + "? (y/n)").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM product WHERE LOWER(product) = LOWER(?)", (remove,)) #to delete command LOWER or UPPER for replacement
        conn.commit()
        
    elif confirm == 'n':
        return
    
    else:
        print("Invalid Choice!")
        return

def reduce_quan():
    print("=========================================")
    name = input("Input product name (0 to back): ")
    if name == "0":
        return
    
    cursor.execute("SELECT stock, price FROM product WHERE LOWER(product) = LOWER(?)", (name,))
    result = cursor.fetchone()

    if result is None:
        print("Product not found.")
        return

    current_stock = result[0]
    current_price = result[1]
    reduce = int(input("How many products to be bought? (0 to back): "))
    if reduce == 0:
        return
    
        


    if reduce <= current_stock:
        new_stock = current_stock - reduce
        total = current_price * reduce
        cursor.execute("UPDATE product SET stock = ? WHERE LOWER(product) = LOWER(?)", (new_stock, name))
        conn.commit()

        cursor.execute("INSERT INTO sales (product, quantity, price, total, date) VALUES (?, ?, ?, ?, ?)", (name, reduce, current_price, total, date))
        conn.commit()
        print("Stock Updated")

    else:
        print("Above Threshold!")
                
#FUNCTIONS ================================================================
            



#MENU ============================================================================
role = None
while role is None:
    clear()
    role = login()

choice = ""
while choice != "0":

    if role == "manager":
        print("=========================================")
        print("SYSTOCKS - MANAGER")
        print("=========================================")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Reduce Quantity")
        print("5. Change Username & Password")
        print("6. View Sales")
        print("7. View Profit")
        print("8. View Inventory")
        print("9. Search Product")
        print("E. Edit Price")
        print("0. Exit")
        print("=========================================")
        choice = input("Enter choice: ")
        
        if choice == "1":
            clear()
            view_products()
            
        elif choice == "2":
            clear()
            add_product()
            
        elif choice == "3":
            clear()
            remove_product()

        elif choice == "4":
            clear()
            reduce_quan()

        elif choice == "5":
            clear()
            change_password()

        elif choice == "6":
            clear()
            view_sales()

        elif choice == "7":
            clear()
            view_sales()
            view_profit()

        elif choice == "8":
            clear()
            view_inventory()

        elif choice == "9":
            clear()
            search_product()

        elif choice == 'E':
            clear()
            edit_price()

        elif choice == "0":
            clear()
            print("Goodbye")

        else:
            print("Invalid Choice!")
            
    
    elif role == "staff":

        print("=========================================")
        print("SYSTOCKS - STAFF")
        print("=========================================")
        print("1. View Products")
        print("2. Reduce Quantity")
        print("3. Search Product")
        print("0. Exit")
        print("=========================================")
        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            view_products()

        elif choice == "2":
            clear()
            reduce_quan()

        elif choice == "3":
            clear()
            search_product()

        elif choice == "0":
            clear()
            print("Goodbye")


#MENU ============================================================================







