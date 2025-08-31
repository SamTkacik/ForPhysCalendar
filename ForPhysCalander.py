import streamlit as st
import pandas as pd
import datetime
import calendar

# -----------------------
# 🔧 MASTER SETTINGS
# -----------------------
st.set_page_config(layout="wide")  # uses full webpage screen
col1, col2 = st.columns([1, 3])   # sidebar filters on left, calendar on right

# Define your categories here
CATEGORY_OPTIONS = ["PGSC", "SPS", "Department of Physics", "GAU", "Other"]
TYPE_OPTIONS = ["Recreational", "Academic/Professional", "Interdisciplinary"]

# Define calendar range
start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

# Store events in session state
if "events" not in st.session_state:
    st.session_state["events"] = []  # placeholder until you add import or owner form later

st.title("USF Physics Calendar for Fall 25")

# -----------------------
# FILTERS + VIEW OPTIONS
# -----------------------
with col1:
    st.subheader("Filters")
    
    # Organization filters
    st.markdown("Filter by Organization:")
    select_all_categories = st.checkbox("Select/Deselect All Organizations", value=True)
    selected_categories = []
    if select_all_categories:
        selected_categories = CATEGORY_OPTIONS
    else:
        for cat in CATEGORY_OPTIONS:
            if st.checkbox(cat, value=True, key=f"cat_{cat}"):
                selected_categories.append(cat)

    # Event type filters
    st.markdown("Filter by Event Type:")
    select_all_types = st.checkbox("Select/Deselect All Event Types", value=True)
    selected_types = []
    if select_all_types:
        selected_types = TYPE_OPTIONS
    else:
        for t in TYPE_OPTIONS:
            if st.checkbox(t, value=True, key=f"type_{t}"):
                selected_types.append(t)

    # View selector moved here
    st.subheader("View Options")
    view_mode = st.radio("Choose view:", ["List View", "Grid View"], horizontal=False)

# -----------------------
# SHOW CALENDAR
# -----------------------
with col2:
    if view_mode == "List View":
        st.subheader("🗓 Events (List View)")
        for d in all_dates:
            events_today = [
                e for e in st.session_state["events"]
                if e["date"] == d.date()
                and e["category"] in selected_categories
                # (later: add type filter too)
            ]
            if events_today:
                st.markdown(f"### {d.strftime('%A, %B %d, %Y')}")
                for e in events_today:
                    st.write(f"- **{e['name']}** _(Category: {e['category']})_")

    else:
        st.subheader("📆 Events (Grid View)")

        months = sorted(set((d.year, d.month) for d in all_dates))
        chosen_month = st.selectbox(
            "Select Month",
            [datetime.date(y, m, 1).strftime("%B %Y") for y, m in months]
        )
        chosen_year, chosen_month_num = [
            (y, m) for (y, m) in months
            if datetime.date(y, m, 1).strftime("%B %Y") == chosen_month
        ][0]

        cal = calendar.Calendar(firstweekday=6)  # Sunday start
        month_days = cal.monthdatescalendar(chosen_year, chosen_month_num)

        # Display grid
        for week in month_days:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if start_date <= day <= end_date:
                        st.markdown(f"**{day.day}**")
                        todays_events = [
                            e for e in st.session_state["events"]
                            if e["date"] == day
                            and e["category"] in selected_categories
                        ]
                        for e in todays_events:
                            st.markdown(f"- {e['name']} ({e['category']})")
                    else:
                        st.markdown(" ")  # empty cells

