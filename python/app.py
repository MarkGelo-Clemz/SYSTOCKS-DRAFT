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
    df = pd.DataFrame(results, columns=["ID", "Product", "Price", "Stock"])
    st.dataframe(df)

elif page == "Add Products":
    
    name = st.text_input("Input Product Name (0 to back): ").capitalize()

    if st.button("Check Product"):
        cursor.execute("SELECT COUNT(*) FROM product WHERE LOWER(product) = LOWER(?)", (name,))
        count = cursor.fetchone()[0] #grabs result just 1

        if count == 1:
            st.warning("Product already exists")
            add = st.number_input("How many stock to add? (0 to back): ")

            if st.button("Add Stock"):
                cursor.execute("UPDATE product SET stock = stock + ? WHERE LOWER(product) = LOWER(?)", (add, name))
                conn.commit()
                st.success("Stock Updated!")

        else:
            st.info("New Product! Fill in details:")
            price = st.number_input("Input Product Price: ")
            stock = st.number_input("Input Product Quantity: ")

            if st.button("Add Product"):
                cursor.execute("INSERT INTO product (product, price, stock) VALUES (?, ?, ?)", (name, price, stock))
                conn.commit()
                st.success("Product Added!")



elif page == "Remove Products":
    remove = st.text_input("Input product to remove (0 to back): ")
    
    confirm = input("Are you sure you want to remove " + remove + "? (y/n)").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM product WHERE LOWER(product) = LOWER(?)", (remove,)) #to delete command LOWER or UPPER for replacement
        conn.commit()
        


    