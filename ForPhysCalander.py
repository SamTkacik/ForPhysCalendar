import streamlit as st
import pandas as pd
import datetime as dt
import calendar

# =====================
# Page & Header
# =====================
st.set_page_config(layout="wide")

st.markdown(
    """
    <div style='background-color:#e6f0ff; padding:25px; border-radius:12px;'>
        <h1 style='text-align: center; color:#003366; margin:0;'>
            USF Physics Calendar for Fall 2025
        </h1>
    </div>
    <br>
    """,
    unsafe_allow_html=True,
)

# =====================
# Master Settings
# =====================
CATEGORY_OPTIONS = ["PGSC", "SPS", "Department of Physics", "GAU", "CAS", "Other"]
TYPE_OPTIONS = ["Recreational", "Academic/Professional", "Interdisciplinary"]

start_date = dt.date(2025, 8, 1)
end_date = dt.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

# Helper: list of first-of-month dates between start and end (inclusive)
months = []
cur = dt.date(start_date.year, start_date.month, 1)
while cur <= dt.date(end_date.year, end_date.month, 1):
    months.append(cur)
    if cur.month == 12:
        cur = dt.date(cur.year + 1, 1, 1)
    else:
        cur = dt.date(cur.year, cur.month + 1, 1)

# =====================
# Master Event List (code-defined)
# =====================
# You can edit/add events here. Each event supports: date, name, category, type, time, location, description.
DEFAULT_EVENTS = [
    {
        "date": dt.date(2025, 8, 15),
        "name": "PGSC Welcome Party",
        "category": "PGSC",
        "type": "Recreational",
        "time": "6:00 PM – 9:00 PM",
        "location": "ISA Lobby",
        "description": "Kickoff celebration with food, games, and networking for new and returning students.",
    },
    {
        "date": dt.date(2025, 9, 1),  # 👇 Your requested hard-coded event
        "name": "Labor Day Test Event",
        "category": "Other",
        "type": "Recreational",
        "time": "All Day",
        "location": "USF Campus",
        "description": "Test holiday entry for Labor Day.",
    },
    {
        "date": dt.date(2025, 9, 10),
        "name": "SPS Guest Lecture",
        "category": "SPS",
        "type": "Academic/Professional",
        "time": "3:30 PM – 5:00 PM",
        "location": "ISA 2015",
        "description": "Invited speaker discusses cutting-edge particle physics research.",
    },
    {
        "date": dt.date(2025, 10, 5),
        "name": "Physics Dept. Research Symposium",
        "category": "Department of Physics",
        "type": "Academic/Professional",
        "time": "9:00 AM – 4:00 PM",
        "location": "ISA 101",
        "description": "A day of talks and posters from department research groups.",
    },
    {
        "date": dt.date(2025, 11, 2),
        "name": "GAU Outreach Event",
        "category": "GAU",
        "type": "Interdisciplinary",
        "time": "11:00 AM – 2:00 PM",
        "location": "Tampa Museum Courtyard",
        "description": "Community outreach and physics demos organized by GAU.",
    },
]

if "events" not in st.session_state:
    st.session_state["events"] = DEFAULT_EVENTS.copy()

# =====================
# Layout: Filters (left) + Calendar (right)
# =====================
left, right = st.columns([1, 3], gap="large")

with left:
    st.subheader("Filters & View")

    # Organization filter
    st.markdown("**Organization:**")
    org_select_all = st.checkbox("Select/Deselect All Organizations", value=True, key="org_all")
    selected_categories = CATEGORY_OPTIONS if org_select_all else []
    if not org_select_all:
        for cat in CATEGORY_OPTIONS:
            if st.checkbox(cat, value=True, key=f"cat_{cat}"):
                selected_categories.append(cat)

    # Event type filter
    st.markdown("**Event Type:**")
    type_select_all = st.checkbox("Select/Deselect All Event Types", value=True, key="type_all")
    selected_types = TYPE_OPTIONS if type_select_all else []
    if not type_select_all:
        for t in TYPE_OPTIONS:
            if st.checkbox(t, value=True, key=f"type_{t}"):
                selected_types.append(t)

    # View mode
    view_mode = st.radio("View Mode", ["List View", "Grid View"], key="view_mode")

    # Month selector appears only for Grid View
    chosen_month_date = None
    if view_mode == "Grid View":
        month_labels = [m.strftime("%B %Y") for m in months]
        # default to the month that contains 'today' if in range, else start month
        today = dt.date.today()
        if start_date <= today <= end_date:
            default_idx = next((i for i, m in enumerate(months) if m.year == today.year and m.month == today.month), 0)
        else:
            default_idx = 0
        chosen_label = st.selectbox("Month", month_labels, index=default_idx)
        chosen_month_date = months[month_labels.index(chosen_label)]

# Filter function
filtered = [
    e for e in st.session_state["events"]
    if e["category"] in selected_categories
    and e["type"] in selected_types
    and start_date <= e["date"] <= end_date
]

# =====================
# Rendering Helpers
# =====================
WEEKDAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]  # Sunday start


def render_event_details_html(e: dict) -> str:
    """HTML for a single event line with collapsible details.
    Keeps cells compact but lets users click to read more."""
    return (
        "<details style='margin-top:6px;'>"
        f"<summary style='cursor:pointer; font-size:0.9rem;'>{e['name']}</summary>"
        "<div style='font-size:0.85rem; line-height:1.35;'>"
        f"<div><b>Org:</b> {e['category']} &nbsp; • &nbsp; <b>Type:</b> {e['type']}</div>"
        f"<div><b>Time:</b> {e['time']}</div>"
        f"<div><b>Location:</b> {e['location']}</div>"
        f"<div style='margin-top:4px;'><b>Description:</b> {e['description']}</div>"
        "</div>"
        "</details>"
    )


# =====================
# Main Panel
# =====================
with right:
    if view_mode == "List View":
        st.subheader("🗒️ Event List")
        if not filtered:
            st.info("No events match your filters.")
        else:
            # Group by date
            by_date = {}
            for e in filtered:
                by_date.setdefault(e["date"], []).append(e)
            for date_key in sorted(by_date.keys()):
                st.markdown(f"### {date_key.strftime('%A, %B %d, %Y')}")
                for e in sorted(by_date[date_key], key=lambda x: (x["time"], x["name"])):
                    with st.expander(f"{e['name']}  —  {e['time']} @ {e['location']}"):
                        st.write(f"**Organization:** {e['category']}")
                        st.write(f"**Type:** {e['type']}")
                        st.write(f"**Description:** {e['description']}")

    else:  # Grid View
        # Require a month selection from left; fallback to first month
        if not chosen_month_date:
            chosen_month_date = months[0]

        year, month = chosen_month_date.year, chosen_month_date.month
        st.subheader(f"📆 {chosen_month_date.strftime('%B %Y')}")

        # Header row for weekdays
        hdr_cols = st.columns(7)
        for i, name in enumerate(WEEKDAY_NAMES):
            hdr_cols[i].markdown(
                f"<div style='text-align:center; font-weight:700; opacity:0.8;'>{name}</div>",
                unsafe_allow_html=True,
            )

        cal = calendar.Calendar(firstweekday=6)  # 6 => Sunday first
        weeks = cal.monthdatescalendar(year, month)

        for week in weeks:
            cols = st.columns(7)
            for i, day in enumerate(week):
                in_range = (start_date <= day <= end_date)
                in_month = (day.month == month)

                # Events for this cell
                day_events = []
                if in_range:
                    day_events = [e for e in filtered if e["date"] == day]

                # Style
                bg = "#ffffff" if in_month else "#f6f7fb"
                border = "#e5e7eb"
                day_num_style = "color:#111827;" if in_month else "color:#9ca3af;"

                # Build HTML for the cell
                if in_range:
                    events_html = "".join(render_event_details_html(e) for e in day_events)
                else:
                    events_html = ""

                cell_html = f"""
                    <div style="
                        border:1px solid {border}; border-radius:10px; padding:8px; min-height:120px; 
                        background:{bg}; overflow:auto;">
                        <div style="font-weight:700; {day_num_style}">{day.day}</div>
                        <div style="font-size:0.9rem;">{events_html}</div>
                    </div>
                """
                cols[i].markdown(cell_html, unsafe_allow_html=True)

