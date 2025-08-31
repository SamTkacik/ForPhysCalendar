import streamlit as st
import pandas as pd
import datetime
import calendar

# -----------------------
# 🔧 MASTER SETTINGS
# -----------------------
CATEGORY_OPTIONS = ["PGSC", "SPS", "Department of Physics", "GAU", "CAS", "Other"]
TYPE_OPTIONS = ['Recreational', 'Academic/Professional', 'Interdisciplinary']

# Calendar range
start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)

# -----------------------
# EVENT DEFINITIONS
# -----------------------
if "events" not in st.session_state:
    st.session_state["events"] = [
        {
            "date": datetime.date(2025, 9, 1),
            "name": "Labor Day Test Event",
            "category": "Other",
            "type": "Recreational",
            "time": "10:00 AM - 2:00 PM",
            "location": "USF Campus Lawn",
            "description": "A placeholder event for Labor Day."
        },
        {
            "date": datetime.date(2025, 9, 10),
            "name": "SPS Guest Lecture",
            "category": "SPS",
            "type": "Academic/Professional",
            "time": "4:00 PM - 6:00 PM",
            "location": "Physics Building, Room 101",
            "description": "Special lecture hosted by the Society of Physics Students."
        },
        {
            "date": datetime.date(2025, 10, 5),
            "name": "Physics Dept. Research Symposium",
            "category": "Department of Physics",
            "type": "Academic/Professional",
            "time": "9:00 AM - 5:00 PM",
            "location": "Science Hall Auditorium",
            "description": "Annual symposium highlighting student and faculty research."
        }
    ]

# -----------------------
# PAGE SETUP
# -----------------------
st.markdown("""
    <div style="background-color:#004d99; padding:20px; border-radius:12px; text-align:center;">
        <h1 style="color:white;">USF Physics Calendar – Fall 2025</h1>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR: Filters & Views
# -----------------------
st.sidebar.header("Filters & Views")

# Filters
st.sidebar.subheader("Filter by Organization")
select_all_org = st.sidebar.checkbox("Select/Deselect All Orgs", value=True)
if select_all_org:
    selected_categories = CATEGORY_OPTIONS
else:
    selected_categories = [c for c in CATEGORY_OPTIONS if st.sidebar.checkbox(c, value=True)]

st.sidebar.subheader("Filter by Type")
select_all_type = st.sidebar.checkbox("Select/Deselect All Types", value=True)
if select_all_type:
    selected_types = TYPE_OPTIONS
else:
    selected_types = [t for t in TYPE_OPTIONS if st.sidebar.checkbox(t, value=True)]

# View option
view_option = st.sidebar.radio("View as:", ["List View", "Grid View"])

# Month selection for grid
month = None
if view_option == "Grid View":
    month = st.sidebar.selectbox(
        "Select Month",
        ["August", "September", "October", "November", "December"]
    )
    month_to_num = {"August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    month = month_to_num[month]

# -----------------------
# FILTER EVENTS
# -----------------------
events_df = pd.DataFrame(st.session_state["events"])
filtered_events = events_df[
    events_df["category"].isin(selected_categories) &
    events_df["type"].isin(selected_types)
]

# -----------------------
# DISPLAY
# -----------------------
if view_option == "List View":
    st.subheader("📅 Events (List View)")
    if filtered_events.empty:
        st.info("No events match your filters.")
    else:
        for _, event in filtered_events.sort_values("date").iterrows():
            with st.expander(f"{event['date']} – {event['name']}"):
                st.write(f"**Organization:** {event['category']}")
                st.write(f"**Type:** {event['type']}")
                st.write(f"**Time:** {event['time']}")
                st.write(f"**Location:** {event['location']}")
                st.write(f"**Description:** {event['description']}")

elif view_option == "Grid View":
    st.subheader("📆 Events (Grid View)")

    if month is not None:
        cal = calendar.Calendar(firstweekday=6)  # Sunday-first
        month_days = cal.monthdatescalendar(2025, month)

        for week in month_days:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day.month == month:
                        st.markdown(f"**{day.day}**")
                        day_events = filtered_events[filtered_events["date"] == day]
                        for _, event in day_events.iterrows():
                            st.markdown(f"- {event['name']} ({event['time']})")


