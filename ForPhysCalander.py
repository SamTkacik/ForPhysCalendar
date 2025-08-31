import streamlit as st
import pandas as pd
import datetime
import calendar

# -------------------
# Setup
# -------------------
start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

if "events" not in st.session_state:
    st.session_state["events"] = []  # {date, name, category}

st.title("📅 Interactive Calendar (Aug–Dec 2025)")

# -------------------
# Add Event
# -------------------
with st.form("add_event"):
    st.subheader("➕ Add Event")
    event_date = st.date_input("Date", min_value=start_date, max_value=end_date, value=start_date)
    event_name = st.text_input("Event Name")
    event_category = st.text_input("Category (e.g., Work, School, Sports)")
    submitted = st.form_submit_button("Add Event")

    if submitted and event_name.strip():
        st.session_state["events"].append({
            "date": event_date,
            "name": event_name,
            "category": event_category if event_category else "General"
        })
        st.success(f"✅ Added '{event_name}' on {event_date} under '{event_category or 'General'}'")

# -------------------
# Filters
# -------------------
st.subheader("📌 Filters")
categories = sorted(set(e["category"] for e in st.session_state["events"])) or ["(none)"]

select_all = st.checkbox("Select/Deselect All", value=True)
selected_categories = []

if select_all:
    selected_categories = categories
else:
    for cat in categories:
        if st.checkbox(cat, value=True):
            selected_categories.append(cat)

# -------------------
# View Selector
# -------------------
st.subheader("👀 View Options")
view_mode = st.radio("Choose view:", ["List View", "Grid View"], horizontal=True)

# -------------------
# List View
# -------------------
if view_mode == "List View":
    st.subheader("🗓 Events (List View)")
    for d in all_dates:
        events_today = [
            e for e in st.session_state["events"]
            if e["date"] == d.date() and e["category"] in selected_categories
        ]
        if events_today:
            st.markdown(f"### {d.strftime('%A, %B %d, %Y')}")
            for e in events_today:
                st.write(f"- **{e['name']}** _(Category: {e['category']})_")

# -------------------
# Grid View
# -------------------
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
                        if e["date"] == day and e["category"] in selected_categories
                    ]
                    for e in todays_events:
                        st.markdown(f"- {e['name']} ({e['category']})")
                else:
                    st.markdown(" ")  # Empty cells
