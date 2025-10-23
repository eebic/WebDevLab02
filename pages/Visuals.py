# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFO
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")

st.divider()
st.header("Load Data")

# --- File paths ---
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
csv_path = os.path.join(base_dir, "data.csv")
json_path = os.path.join(base_dir, "data.json")

# --- Load CSV ---
if os.path.exists(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        df = pd.DataFrame(columns=["timestamp", "name", "category", "value"])
        st.warning("Could not read 'data.csv' — using an empty table instead.")
else:
    df = pd.DataFrame(columns=["timestamp", "name", "category", "value"])
    st.info("'data.csv' not found — create some data on the Survey page.")

# --- Load JSON ---
json_data = {}
if os.path.exists(json_path):
    try:
        with open(json_path) as f:
            json_data = json.load(f)
    except Exception:
        json_data = {}
        st.warning("Could not parse 'data.json'.")
else:
    st.info("'data.json' not found — using an empty dictionary.")

# --- Show preview ---
st.caption("Loaded CSV columns: " + ", ".join(df.columns) if not df.empty else "CSV currently has no rows.")
if not df.empty:
    st.write(f"**Rows loaded:** {len(df)}")
    st.dataframe(df.tail(10), use_container_width=True)
else:
    st.info("No CSV rows yet — add entries on the Survey page, then come back here.")

# GRAPH 1: STATIC GRAPH — Distribution of Values (CSV)

st.divider()
st.header("Graphs")
st.subheader("Graph 1: Static — Distribution of Values (CSV)")

if not df.empty and "value" in df.columns:
    values = pd.to_numeric(df["value"], errors="coerce").dropna()
    if not values.empty:
        binned = pd.cut(values, bins=10)
        hist = (
            binned.value_counts()
            .sort_index()
            .rename_axis("bin")
            .reset_index(name="count")
        )
        hist["bin"] = hist["bin"].astype(str)
        st.bar_chart(hist, x="bin", y="count")
        st.caption("Histogram of all recorded values from **data.csv**.")
    else:
        st.info("No numeric values yet to build a histogram.")
else:
    st.info("Add CSV entries to view the histogram.")

# GRAPH 2: DYNAMIC GRAPH — Average Value by Category (CSV)

st.divider()
st.subheader("Graph 2: Dynamic — Average Value by Category (CSV)")

all_categories = sorted(df["category"].dropna().unique().tolist()) if not df.empty else []
if "chosen_categories" not in st.session_state:
    st.session_state.chosen_categories = all_categories

st.session_state.chosen_categories = st.multiselect(
    "Filter categories (CSV):",
    options=all_categories,
    default=st.session_state.chosen_categories
)

if not df.empty and st.session_state.chosen_categories:
    df_filt = df[df["category"].isin(st.session_state.chosen_categories)]
    if not df_filt.empty:
        avg = df_filt.groupby("category")["value"].mean().reset_index()
        st.bar_chart(avg, x="category", y="value")
        st.caption("Shows the mean `value` recorded per selected category from **data.csv**.")
    else:
        st.info("No rows match the selected categories.")
else:
    st.info("Select one or more categories to draw the chart (or add CSV data on the Survey page).")

# GRAPH 3: DYNAMIC GRAPH — JSON Metrics (fun Survey categories)

st.divider()
st.subheader("Graph 3: Dynamic — JSON Metrics")

# Mapping of Survey categories to their JSON keys
label_to_key = {
    "Hours Spent Debugging 🧠": "debugging_hours_per_day",
    "Cans of Celsius vs. Lines of Code ☕💻": "celsius_vs_loc_per_day",
    "Tabs Opened in Chrome 🌐": "tabs_opened_per_day",
    "Times You Checked BuzzPort 🐝": "buzzport_checks_per_day",
    "Emails Ignored 📩": "emails_ignored_per_day",
    "Moments of Academic Enlightenment 💡": "lightbulb_moments_per_day",
    "Procrastination Level (1–10) ⏰": "procrastination_level_per_day",
    "Spotify Playlists Created 🎧": "spotify_playlists_created_per_week",
    "Unfinished Canvas Assignments 📢": "unfinished_canvas_assignments_per_week",
    "Other (because life can't be boxed in) ✨": "other_metric"
}

dropdown_labels = list(label_to_key.keys())

if "metric_choice_label" not in st.session_state and dropdown_labels:
    st.session_state.metric_choice_label = dropdown_labels[0]

if dropdown_labels:
    chosen_label = st.selectbox(
        "Choose a Chaos Metric:",
        dropdown_labels,
        index=dropdown_labels.index(st.session_state.metric_choice_label)
    )
    st.session_state.metric_choice_label = chosen_label
    chosen_key = label_to_key.get(chosen_label)

    metrics = json_data.get("metrics", {}) if isinstance(json_data, dict) else {}
    series = metrics.get(chosen_key, {})

    if isinstance(series, dict) and series:
        df_json = pd.DataFrame({"label": list(series.keys()), "value": list(series.values())})
        # Keep Mon→Sun order if labels are weekdays
        dow_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if set(df_json["label"]).issubset(dow_order):
            df_json["label"] = pd.Categorical(df_json["label"], categories=dow_order, ordered=True)
            df_json = df_json.sort_values("label")

        st.line_chart(df_json.set_index("label"))
        st.caption(f"Displays **{chosen_label}** from `data.json`.")
    else:
        st.info(
            f"No data found in `data.json` for **{chosen_label}**.\n\n"
            "To add it, open `data.json` and include a section like this under `metrics`:\n\n"
            f"\"{chosen_key}\": {{ \"Mon\": 10, \"Tue\": 12, \"Wed\": 9, \"Thu\": 14, \"Fri\": 8, \"Sat\": 4, \"Sun\": 3 }}\n\n"
            "Then refresh this page!"
        )
else:
    st.warning("No metrics available yet. Add a 'metrics' section in `data.json`.")
