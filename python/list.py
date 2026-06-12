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
#ERROR HERE DOESNT CREATE THE TABLE
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

def login():
    print("====================SYSTOCKS LOGIN====================")
    username = input("Username: ").lower()
    password = input("Password: ").lower()

    cursor.execute("SELECT role FROM users WHERE LOWER(username) = LOWER(?) AND LOWER(password) = LOWER(?)", (username, password))
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
            product TEXT
            quantity INTEGER,
            price REAL,
            toal REAL,
            dat TEXT)
            """)









#SALES =================================================================================







#FUNCTIONS ================================================================

def view_products():
    cursor.execute("SELECT * FROM product ORDER BY product") #gathers and red the data 
    results = cursor.fetchall()
    

    print("=========================================")

    for row in results:
        print(row[1], "-", row[3], "left")
        
        if row[3] <= 10:
            print("Low Stock Alert:", row[1])

def add_product(products):
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


def remove_product(products):
    print("=========================================")
    remove = input("Input product to remove (0 to back): ")
    if remove == "0":
        return
    cursor.execute("DELETE FROM product WHERE LOWER(product) = LOWER(?)", (remove,)) #to delete command LOWER or UPPER for replacement
    conn.commit()


# WE HAVE ERROR HERE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def reduce_quan(products):
    print("=========================================")
    name = input("Input product name (0 to back): ")
    if name == "0":
        return
    
    cursor.execute("SELECT stock FROM product WHERE LOWER(product) = LOWER(?)", (name,))
    result = cursor.fetchone()

    if result is None:
        print("Product not found.")
        return

        current_stock = result[0]
        reduce = int(input("How many products to be bought? (0 to back): "))
        if reduce == 0:
            return


        if reduce <= product["Stock"]:
            product["Stock"] = product["Stock"] - reduce
            cursor.execute("UPDATE product SET stock = ? WHERE LOWER(product) = LOWER(?)", (product["Stock"], name))
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
        print("0. Exit")
        print("=========================================")
        choice = input("Enter choice: ")
        
        if choice == "1":
            clear()
            view_products()
            
        elif choice == "2":
            clear()
            add_product(products)
            
        elif choice == "3":
            clear()
            remove_product(products)

        elif choice == "4":
            clear()
            reduce_quan(products)

        elif choice == "0":
            clear()
            print("Goodbye")
    
    elif role == "staff":

        print("=========================================")
        print("SYSTOCKS - STAFF")
        print("=========================================")
        print("1. View Products")
        print("2. Reduce Quantity")
        print("0. Exit")
        print("=========================================")
        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            view_products()

        elif choice == "4":
            clear()
            reduce_quan(products)

        elif choice == "0":
            clear()
            print("Goodbye")


#MENU ============================================================================







