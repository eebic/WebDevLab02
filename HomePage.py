# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Jenna's Lab 02 Dashboard Homepage",  # Updated title
    page_icon="📊",                         # Changed icon to fit the dashboard theme
)

# WELCOME PAGE TITLE
st.title("Welcome to Jenna's Data Dashboard! 📊")

# INTRODUCTORY TEXT
st.write("""
This Streamlit application collects data, stores it in both CSV and JSON formats, 
and visualizes it through interactive graphs. Use the sidebar on the left to navigate
between pages.

### How to use this app:
- **Survey Page**: Input new data entries (timestamp, name, category, value) into our CSV file.
- **Visuals Page**: View and interact with dynamic and static graphs based on the collected data.

This project was created for **CS 1301 Lab 02**.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png", caption="Welcome to my Lab 02 Dashboard!")
