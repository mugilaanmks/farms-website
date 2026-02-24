import streamlit as st
import sqlite3
from PIL import Image
import io

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect("products.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    details TEXT,
    image BLOB
)
""")
conn.commit()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="MKS Farms", layout="wide")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<h1 style='text-align:center; color:green;'>MKS Farms 🌾</h1>
<p style='text-align:center;'>Fresh Products Direct from Farm</p>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Products", "Contact", "Admin"])

# -----------------------------
# PRODUCTS PAGE
# -----------------------------
if menu == "Products":
    st.subheader("Available Products")

    c.execute("SELECT * FROM products")
    data = c.fetchall()

    if len(data) == 0:
        st.info("No products available")

    for row in data:
        st.markdown("---")
        if row[4]:
            image = Image.open(io.BytesIO(row[4]))
            st.image(image, width=200)

        st.write(f"**{row[1]}**")
        st.write(row[3])
        st.write(f"Price: ₹{row[2]} per kg")
        st.markdown("[Order on WhatsApp](https://wa.me/919629262696)")

# -----------------------------
# CONTACT PAGE
# -----------------------------
elif menu == "Contact":
    st.write("Owner: Mugilaan")
    st.write("Phone: 9629262696")
    st.markdown("[Location](https://maps.app.goo.gl/EKp8WGnhraNXeuzHA)")
    st.markdown("[WhatsApp](https://wa.me/919629262696)")

# -----------------------------
# ADMIN PANEL
# -----------------------------
elif menu == "Admin":
    st.subheader("Admin Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if user == "admin" and pwd == "mks123":
        st.success("Admin Logged In")

        # Add Product
        st.markdown("### Add Product")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=1)
        details = st.text_area("Details")
        image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        if st.button("Add Product"):
            img_bytes = image.read() if image else None
            c.execute("INSERT INTO products (name, price, details, image) VALUES (?, ?, ?, ?)",
                      (name, price, details, img_bytes))
            conn.commit()
            st.success("Product Added")

        # Manage Products
        st.markdown("### Manage Products")
        c.execute("SELECT * FROM products")
        data = c.fetchall()

        for row in data:
            st.markdown("---")
            st.write(f"ID: {row[0]} | {row[1]} - ₹{row[2]}")

            new_price = st.number_input(f"New Price for {row[1]}", value=row[2], key=f"price{row[0]}")

            if st.button("Update Price", key=f"update{row[0]}"):
                c.execute("UPDATE products SET price=? WHERE id=?", (new_price, row[0]))
                conn.commit()
                st.success("Updated")

            if st.button("Delete", key=f"delete{row[0]}"):
                c.execute("DELETE FROM products WHERE id=?", (row[0],))
                conn.commit()
                st.warning("Deleted")
                st.experimental_rerun()