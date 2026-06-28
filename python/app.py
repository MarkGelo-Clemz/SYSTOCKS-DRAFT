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
    
    name = st.text_input("Input Product Name: ").capitalize()

    if st.button("Check Product"):
        cursor.execute("SELECT COUNT(*) FROM product WHERE LOWER(product) = LOWER(?)", (name,))
        count = cursor.fetchone()[0] #grabs result just 1
        st.session_state["count"] = count #save
        st.session_state["pname"] = name


    if "count" in st.session_state:
        if st.session_state["count"] == 1:
            st.warning("Product already exists")
            add = st.number_input("How many stock to add? (0 to back): ")

            if st.button("Add Stock"):
                cursor.execute("UPDATE product SET stock = stock + ? WHERE LOWER(product) = LOWER(?)", (add, name))
                conn.commit()
                st.write("Stock Updated!")
                st.session_state.clear()
                st.rerun

        else:
            st.info("New Product! Fill in details!")
            price = st.number_input("Input Product Price: ")
            stock = st.number_input("Input Product Quantity: ")

            if st.button("Add Product"):
                cursor.execute("INSERT INTO product (product, price, stock) VALUES (?, ?, ?)", (name, price, stock))
                conn.commit()
                st.write("Product Added!")
                st.session_state.clear()
                st.rerun


elif page == "Remove Products":
    remove = st.text_input("Input product to remove: ")
    if st.button("Remove Product"):
        st.session_state["remove_name"] = remove
    
    if "remove_name" in st.session_state:
        st.warning("Are you sure you want to remove " + remove)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes"):
                cursor.execute("DELETE FROM product WHERE LOWER(product) = LOWER(?)", (st.session_state["remove_name"],)) #to delete command LOWER or UPPER for replacement
                conn.commit()
                st.session_state.clear()
                st.info("Product Succesfully Removed!")

        with col2:
            if st.button("Cancel"):
                st.session_state.clear()
                st.rerun()
        


    