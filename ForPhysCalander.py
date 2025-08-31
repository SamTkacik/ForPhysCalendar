import streamlit as st
import pandas as pd
import datetime

# -----------------------
# MASTER SETTINGS
# -----------------------
CATEGORY_OPTIONS = ["PGSC", "SPS", "Department of Physics", "GAU", "Other"]
TYPE_OPTIONS = ['Recreational', 'Academic/Professional', 'Interdisciplinary']

start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

# -----------------------
# MASTER EVENT LIST
# -----------------------
if "events" not in st.session_state:
    st.session_state["events"] = [
        {
            "date": datetime.date(2025, 9, 7),
            "name": "PGSC Welcome Party",
            "category": "PGSC",
            "type": "Recreational",
            "time": "2:00 PM – 5:00 PM",
            "location": "ISA 5010",
            "description": "Kickoff the semester with friends, food, and fun physics trivia!"
        },
        {
            "date": datetime.date(2025, 9, 10),
            "name": "Test",
            "category": "SPS",
            "type": "Academic/Professional",
            "time": "NA",
            "location": "Virtual",
            "description": "test"
        }
    ]

# -----------------------
# PAGE LAYOUT
# -----------------------
st.set_page_config(layout="wide")

# Banner / Header
st.markdown(
    """
    <div style="background-color:#004d99; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:white;">USF Physics Calendar – Fall 2025</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# SIDEBAR CONTROLS
# -----------------------
st.sidebar.header("Filters & View Options")

# Organization filters
st.sidebar.subheader("Organization")
org_select_all = st.sidebar.checkbox("Select/Deselect All Orgs", value=True)
if org_select_all:
    selected_categories = CATEGORY_OPTIONS
else:
    selected_categories = [cat for cat in CATEGORY_OPTIONS if st.sidebar.checkbox(cat, value=True)]

# Event type filters
st.sidebar.subheader("Event Types")
type_select_all = st.sidebar.checkbox("Select/Deselect All Types", value=True)
if type_select_all:
    selected_types = TYPE_OPTIONS
else:
    selected_types = [etype for etype in TYPE_OPTIONS if st.sidebar.checkbox(etype, value=True)]

# View mode
view_mode = st.sidebar.radio("View Mode", ["List View", "Grid View"])

# -----------------------
# FILTER EVENTS
# -----------------------
events = [
    e for e in st.session_state["events"]
    if e["category"] in selected_categories and e["type"] in selected_types
]

# -----------------------
# LIST VIEW
# -----------------------
if view_mode == "List View":
    st.subheader("📋 Event List")
    if not events:
        st.info("No events match your filters.")
    else:
        for event in sorted(events, key=lambda x: x["date"]):
            with st.expander(f"📅 {event['date']} — {event['name']}"):
                st.write(f"**Organization:** {event['category']}")
                st.write(f"**Type:** {event['type']}")
                st.write(f"**Time:** {event['time']}")
                st.write(f"**Location:** {event['location']}")
                st.write(f"**Description:** {event['description']}")

# -----------------------
# GRID VIEW
# -----------------------
elif view_mode == "Grid View":
    st.subheader("📅 Calendar Grid")
    current_month = None
    month_cols = 7  # days of the week

    for date in all_dates:
        # New month section
        if current_month != (date.month, date.year):
            current_month = (date.month, date.year)
            st.markdown(f"### {date.strftime('%B %Y')}")
            st.markdown("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
            st.markdown("|-----|-----|-----|-----|-----|-----|-----|")

        # Collect events for this date
        day_events = [e for e in events if e["date"] == date.date()]
        event_texts = []
        for e in day_events:
            event_texts.append(
                f"<details><summary>{e['name']} ({e['category']})</summary>"
                f"<p><b>Type:</b> {e['type']}<br>"
                f"<b>Time:</b> {e['time']}<br>"
                f"<b>Location:</b> {e['location']}<br>"
                f"<b>Description:</b> {e['description']}</p></details>"
            )

        # Print day cell (inline markdown hack for grid)
        day_str = f"**{date.day}**<br>" + "<br>".join(event_texts) if event_texts else str(date.day)
        st.markdown(day_str, unsafe_allow_html=True)

