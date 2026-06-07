#Day 1- prodduct list with low stock a
import sqlite3
conn = sqlite3.connect("magic.db") #a some type of fstream
cursor = conn.cursor() #a pen where ables you to write commands

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

def view_products():
    cursor.execute("SELECT * FROM product ORDER BY product") #gathers and red the data 
    results = cursor.fetchall()
    

    print("=========================================")

    for row in results:
        print(row[1], "-", row[3], "left")
        
        if row[3] <= 10:
            print("Low Stock Alert:", row[1])

def add_product():
    print("=========================================")
    name = input("Input Product Name: ").capitalize()
    price = float(input("Input Product Price: "))
    stock = int(input("Input Product Quantity: "))
    new_product = {"Product": name, "Price": price, "Stock": stock}
    cursor.execute("INSERT INTO product (product, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()


def remove_product(products):
    print("=========================================")
    remove = input("Input product to remove: ")
    for product in products:
            if product["Product"].lower() == remove.lower():
                cursor.execute("DELETE FROM product WHERE LOWER(product) = LOWER(?)", (remove,)) #to delete command LOWER or UPPER for replacement
                conn.commit()

def reduce_quan(products):
    print("=========================================")
    name = input("Input product name: ")
    for product in products:
            if product["Product"].lower() == name.lower():
                reduce = int(input("How many products to be bought?: "))


                if reduce <= product["Stock"]:
                    product["Stock"] = product["Stock"] - reduce

                else:
                    print("Above Threshold!")
                
                cursor.execute("UPDATE product SET stock = ? WHERE LOWER(product) = LOWER(?)", (product["Stock"], name))
                conn.commit()
                

            




choice = ""
while choice != "0":
    print("=========================================")
    print("1. View Products")
    print("2. Add Product")
    print("3. Remove Product")
    print("4. Reduce Quantity")
    print("0. Exit")
    print("=========================================")
    choice = input("Enter choice: ")
    


    if choice == "1":
        view_products()

    elif choice == "2":
        add_product()
        
    elif choice == "3":
        remove_product(products)

    elif choice == "4":
        reduce_quan(products)

    elif choice == "0":
        print("Goodbye")
