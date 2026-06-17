import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("magic.db")
cursor = conn.cursor()

st.title("SYSTOCKS")
st.write("Welcome to SYSTOCKS")


st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose", ["View Products", "Add Products", "Remove Products"])

if page == "View Products":
    cursor.execute("SELECT * FROM product ORDER BY product") #gathers and red the data 
    results = cursor.fetchall()
    
    

    print("=========================================")

    for row in results:
        print(row[1], "-", row[2], "-", row[3], "left")
        
        if row[3] <= 10:
            print("Low Stock Alert:", row[1])

elif page == "Add Products":
    print("=========================================")
    name = input("Input Product Name (0 to back): ").capitalize()
    

    cursor.execute("SELECT COUNT(*) FROM product WHERE LOWER(product) = LOWER(?)", (name,))
    count = cursor.fetchone()[0] #grabs result just 1


    if count == 1:
        print("Product already exists")
        add = int(input("How many stock to add? (0 to back): "))
        
        cursor.execute("UPDATE product SET stock = stock + ? WHERE LOWER(product) = LOWER(?)", (add, name))
        conn.commit()

    else:
        price = float(input("Input Product Price: "))
        stock = int(input("Input Product Quantity: "))
        cursor.execute("INSERT INTO product (product, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()

elif page == "Remove Products":
    print("=========================================")
    remove = input("Input product to remove (0 to back): ")
    
    confirm = input("Are you sure you want to remove " + remove + "? (y/n)").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM product WHERE LOWER(product) = LOWER(?)", (remove,)) #to delete command LOWER or UPPER for replacement
        conn.commit()
        


    