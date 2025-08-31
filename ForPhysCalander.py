import streamlit as st
import pandas as pd
import datetime
import calendar

# -----------------------
#  MASTER SETTINGS
# -----------------------
st.set_page_config(layout="wide")
CATEGORY_OPTIONS = ["PGSC", "SPS", "Department of Physics", "GAU", "Other"]
TYPE_OPTIONS = ["Recreational", "Academic/Professional", "Interdisciplinary"]
start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()
if "events" not in st.session_state:
    st.session_state["events"] = []  # {"date": date, "name": str, "category": str, "type": str}

st.title("📅 USF Physics Calendar – Fall 2025")

# -----------------------
# Add Event (Owner, ST or PGSC members, Only)
# -----------------------
with st.form("add_event"):
    st.subheader("➕ Add Event (Owner Only)")
    event_date = st.date_input("Date", min_value=start_date, max_value=end_date, value=start_date)
    event_name = st.text_input("Event Name")
    event_category = st.selectbox("Organization", CATEGORY_OPTIONS)
    event_type = st.selectbox("Type", TYPE_OPTIONS)
    submitted = st.form_submit_button("Add Event")

    if submitted and event_name.strip():
        st.session_state["events"].append({
            "date": event_date,
            "name": event_name,
            "category": event_category,
            "type": event_type
        })
        st.success(f"✅ Added '{event_name}' on {event_date} under '{event_category}' ({event_type})")

# -----------------------
# Filters
# -----------------------
st.sidebar.header("Calendar Filters")

# Category filters
st.sidebar.markdown("Filter by organization:")
select_all_categories = st.sidebar.checkbox("Select/Deselect All", value=True, key="all_cats")
selected_categories = CATEGORY_OPTIONS if select_all_categories else [
    cat for cat in CATEGORY_OPTIONS if st.sidebar.checkbox(cat, value=True, key=f"cat_{cat}")
]

# Type filters
st.sidebar.markdown("Filter by event type:")
select_all_types = st.sidebar.checkbox("Select/Deselect All", value=True, key="all_types")
selected_types = TYPE_OPTIONS if select_all_types else [
    t for t in TYPE_OPTIONS if st.sidebar.checkbox(t, value=True, key=f"type_{t}")
]

# -----------------------
# View Selector
# -----------------------
st.subheader("View Options")
view_mode = st.radio("Choose view:", ["List View", "Grid View"], horizontal=True)

# -----------------------
# List View
# -----------------------
def render_list_view():
    st.subheader("📝 Events (List View)")
    events_found = False
    for d in all_dates:
        events_today = [
            e for e in st.session_state["events"]
            if e["date"] == d.date()
            and e["category"] in selected_categories
            and e["type"] in selected_types
        ]
        if events_today:
            events_found = True
            st.markdown(f"### {d.strftime('%A, %B %d, %Y')}")
            for e in events_today:
                st.write(f"- **{e['name']}** _(Org: {e['category']}, Type: {e['type']})_")
    if not events_found:
        st.info("No events match the current filters.")

# -----------------------
# 🔹 Grid View
# -----------------------
def render_grid_view():
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
                        and e["type"] in selected_types
                    ]
                    for e in todays_events:
                        st.markdown(f"- {e['name']} ({e['category']}, {e['type']})")
                else:
                    st.markdown(" ")

# -----------------------
# Render chosen view
# -----------------------
if view_mode == "List View":
    render_list_view()
else:
    render_grid_view()
