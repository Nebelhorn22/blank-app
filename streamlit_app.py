import streamlit as st
import pandas as pd
from datetime import datetime

# Define categories and subcategories
categories = {
    "Defective weld seams": {
        "1": "leak on the longitudinal weld",
        "2": "leak on the circumferential weld",
        "5": "leak at welded elements in the bottom plate",
        "7": "incorrectly welded tank element (eye, sleeve, etc.)"
    },
    "Defective connections": {
        "3": "leak at the bottom flange (bottom plate)",
        "4": "leak at the bottom flange (bottom plate)",
        "6": "leak at water connections in the jacket - buffers",
        "8": "improvement of the water connection dimension - buffers"
    },
    "Material defect": {
        "9": "material damage",
        "10": "material defect"
    },
    "Surface failure": {
        "11": "damage to the tank's paint coating (scratches)",
        "13": "defect in the paint coating",
        "14": "defect in the tank's surface"
    },
    "Incorrect packaging": {
        "12": "damage to the tank's packaging"
    }
}

# Session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "selected_main" not in st.session_state:
    st.session_state.selected_main = None
if "rework_log" not in st.session_state:
    st.session_state.rework_log = []

st.title("🔧 Rework Time Tracker")

# Start and End buttons in one row
col1, col2 = st.columns(2)
with col1:
    if st.session_state.start_time is None:
        if st.button("▶️ Start Rework"):
            st.session_state.start_time = datetime.now()
            st.session_state.end_time = None
            st.session_state.selected_main = None
            st.success(f"Started at {st.session_state.start_time.strftime('%H:%M:%S')}")
    else:
        st.button("▶️ Start Rework", disabled=True)

with col2:
    if st.session_state.start_time and st.session_state.end_time is None:
        if st.button("⏹️ End Rework"):
            st.session_state.end_time = datetime.now()
            st.info("Please select a main category:")
    else:
        st.button("⏹️ End Rework", disabled=True)

# Main category selection
if st.session_state.end_time and st.session_state.selected_main is None:
    st.subheader("Select a main category:")
    for main_cat in categories.keys():
        if st.button(main_cat, key=f"main_{main_cat}"):
            st.session_state.selected_main = main_cat
            break

# Subcategory selection
if st.session_state.selected_main:
    st.subheader(f"Select a subcategory for '{st.session_state.selected_main}'")
    for code, label in categories[st.session_state.selected_main].items():
        if st.button(f"{code} – {label}", key=f"sub_{code}"):
            duration = (st.session_state.end_time - st.session_state.start_time).total_seconds() / 60
            st.session_state.rework_log.append({
                "Start": st.session_state.start_time,
                "End": st.session_state.end_time,
                "Duration (min)": round(duration, 2),
                "Main Category": st.session_state.selected_main,
                "Subcategory Code": code,
                "Subcategory Description": label
            })
            st.success(f"Saved: {round(duration, 2)} min, {st.session_state.selected_main} > {code} – {label}")
            # Reset state
            st.session_state.start_time = None
            st.session_state.end_time = None
            st.session_state.selected_main = None
            break

# Display log
if st.session_state.rework_log:
    df = pd.DataFrame(st.session_state.rework_log)
    st.subheader("📋 Rework Sessions")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Log as CSV", data=csv, file_name="rework_log.csv", mime="text/csv")
