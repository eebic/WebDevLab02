# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os
from datetime import datetime  # Used for adding timestamps to entries

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Record your totally serious, highly scientific daily metrics below. The fate of data science depends on it.")

# Ensure 'data.csv' exists before appending data
csv_path = os.path.join(os.path.dirname(__file__), "..", "data.csv")
csv_path = os.path.abspath(csv_path)
if not os.path.exists(csv_path):
    df_init = pd.DataFrame(columns=["timestamp", "name", "category", "value"])
    df_init.to_csv(csv_path, index=False)

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
with st.form("survey_form", clear_on_submit=True):
    # Create input widgets for the user to enter data.
    name = st.text_input("Your name (or secret alias):", value="Jenna")
    category = st.selectbox(
        "Select what you're tracking today:",
        [
            "Hours Spent Debugging 🧠",
            "Cans of Celsius vs. Lines of Code ☕💻",
            "Tabs Opened in Chrome 🌐",
            "Times You Checked BuzzPort 🐝",
            "Emails Ignored 📩",
            "Moments of Academic Enlightenment 💡",
            "Procrastination Level (1–10) ⏰",
            "Spotify Playlists Created 🎧",
            "Unfinished Canvas Assignments 📢",
            "Other (because life can't be boxed in) ✨"
        ]
    )
    value = st.number_input("Enter a value:", min_value=0.0, step=1.0)

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- FILLED-IN LOGIC ---
        # 1. Create a new row of data from 'name', 'category', and 'value'.
        # 2. Add a timestamp and append this new row to the 'data.csv' file.
        now = datetime.now().isoformat(timespec="seconds")
        new_entry = pd.DataFrame([{
            "timestamp": now,
            "name": name,
            "category": category,
            "value": value
        }])
        new_entry.to_csv(csv_path, mode="a", header=not os.path.getsize(csv_path) > 0, index=False)

        # Friendly success message
        st.success("✅ Entry logged! Your contribution to the chaos of data has been immortalized.")
        st.write(f"**Name:** {name} | **Category:** {category} | **Value:** {value}")

# DATA DISPLAY
# This section shows the current contents of the CSV file.
st.divider()  # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(csv_path)
    # Display the DataFrame as a table (shows the most recent 10 entries).
    st.dataframe(current_data_df.tail(10), use_container_width=True)
else:
    st.warning("No data yet — log your first observation and claim eternal bragging rights.")
