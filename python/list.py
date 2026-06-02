#Day 1- prodduct list with low stock alert
products = [
    {"Product": "Coke", "Price": 25, "Stock": 50},
    {"Product": "Sprite", "Price": 25, "Stock": 50},
    {"Product": "Royal", "Price": 25, "Stock": 50},
    {"Product": "Pepsi", "Price": 25, "Stock": 50},
    {"Product": "Mountain Dew", "Price": 25, "Stock": 50},
    {"Product": "Dr. Pepper", "Price": 25, "Stock": 50},
]

def view_products():
    print("=========================================")
    for product in products:
        print(product["Product"], "-", product["Stock"], "left")
        
        if product["Stock"] <= 10:
            print("Low Stock Alert:", product["Product"])

def add_product():
    print("=========================================")
    name = input("Input Product Name: ")
    price = float(input("Input Product Price: "))
    stock = int(input("Input Product Quantity: "))
    new_product = {"Product": name, "Price": price, "Stock": stock}
    products.append(new_product)


def remove_product():
    print("=========================================")
    remove = input("Input product to remove: ")
    for product in products:
            if product["Product"].lower() == remove.lower():
                products.remove(product)



choice = ""
while choice != "4":
    print("=========================================")
    print("1. View Products")
    print("2. Add Product")
    print("3. Remove Product")
    print("4. Exit")
    print("=========================================")
    choice = input("Enter choice: ")
    


    if choice == "1":
        view_products()

    elif choice == "2":
        add_product()
        
    elif choice == "3":
        remove_product()

    elif choice == "4":
        print("Goodbye")
