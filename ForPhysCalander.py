import streamlit as st
import pandas as pd
import datetime
import calendar

# -----------------------
# SETTINGS
# -----------------------
st.set_page_config(layout="wide")

CATEGORY_OPTIONS = ["Department of Physics", "PGSC", "SPS", "GAU", "Other"]
TYPE_OPTIONS = ['Academic/Professional', 'Recreational', 'Interdisciplinary', 'Other']

start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

banner_text_color_hex = "#9CCB3B"
banner_bg_color_hex = "black"
container_text_color_hex = "#9CCB3B"

# -----------------------
# CSS
# -----------------------
st.markdown(f"""
<style>
/* Background gradient */
.stApp {{
  background: linear-gradient(135deg, #CAD2D8, #7E96A0, #303434);
}}
.stApp > header {{ background-color: transparent; }}

/* Fixed header */
#fixed-header {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}}
main .block-container {{
  padding-top: 100px !important; /* push content below header */
  max-width: 100% !important;
}}

/* Columns equal height */
.stColumns {{
    display: flex !important;
    align-items: stretch !important;
    gap: 1rem !important;
}}
.stColumn > div {{
    background-color: black;
    border-radius: 10px;
    padding: 0.75rem;
    display: flex;
    flex-direction: column;
    overflow-y: auto;  /* independent scroll */
    height: calc(100vh - 140px); /* full viewport minus header */
}}

/* Left column text */
.stColumn:first-child > div {{
    color: {container_text_color_hex};
    max-width: 280px;
}}

/* Right column text */
.stColumn:last-child > div {{
    color: white;
}}

/* Event cards */
.event-card {{
    background: linear-gradient(135deg, #303434, #466069);
    color: white;
    padding: 6px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-size: 0.9rem;
}}

/* Month select styling */
div.st-key-monthbox [data-baseweb="select"] > div {{
    background: linear-gradient(135deg, #466069, #9CCB3B) !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500;
    min-height: 32px !important;
    font-size: 0.9rem !important;
    display: flex;
    align-items: center;
}}
div.st-key-monthbox ul[role="listbox"] {{
    background: linear-gradient(135deg, #303434, #466069) !important;
    border-radius: 8px !important;
}}
div.st-key-monthbox ul[role="listbox"] li {{
    color: white !important;
    font-size: 0.9rem !important;
    padding: 4px 8px !important;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# FIXED HEADER
# -----------------------
st.markdown(
    f"""
    <div id="fixed-header" style='background-color:{banner_bg_color_hex}; padding:12px; text-align:center; border-radius:0 0 10px 10px;'>
        <h2 style='color:{banner_text_color_hex}; margin:0;'>USF Physics Fall 25 Calendar</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# EVENTS
# -----------------------
if "events" not in st.session_state:
    st.session_state["events"] = [
        {
            "date": datetime.date(2025, 9, 1),
            "name": "Labor Day Test Event",
            "category": "Department of Physics",
            "type": "Recreational",
            "time": "12:00 PM",
            "location": "USF Physics Building",
            "description": "A test event for Labor Day."
        }
    ]

def render_event_card(e):
    return f"""
    <div class="event-card">
        <b>{e['name']}</b><br>
        <small>{e['time']} @ {e['location']}</small><br>
        <small>{e['description']}</small>
    </div>
    """

# -----------------------
# LAYOUT
# -----------------------
left, right = st.columns([1,3], gap="medium")

# Left filters
with left:
    st.subheader("Filters")
    select_all_categories = st.checkbox("All Organizations", value=True)
    selected_categories = CATEGORY_OPTIONS if select_all_categories else [
        cat for cat in CATEGORY_OPTIONS if st.checkbox(cat, value=True, key=f"cat_{cat}")]
    st.markdown("**Filter by Event Type:**")
    select_all_types = st.checkbox("All Event Types", value=True)
    selected_types = TYPE_OPTIONS if select_all_types else [
        t for t in TYPE_OPTIONS if st.checkbox(t, value=True, key=f"type_{t}")]

# Right calendar
with right:
    st.subheader("📆 Events")

    months = sorted(set((d.year, d.month) for d in all_dates))
    with st.container(key="monthbox"):
        chosen_month = st.selectbox(
            "Select Month",
            [datetime.date(y, m, 1).strftime("%B %Y") for y, m in months]
        )
    chosen_year, chosen_month_num = [
        (y, m) for (y, m) in months
        if datetime.date(y, m, 1).strftime("%B %Y") == chosen_month][0]

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdatescalendar(chosen_year, chosen_month_num)

    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    st.write(" | ".join([f"**{d}**" for d in weekdays]))
    st.write("---" * 15)

    for week in month_days:
        cols = st.columns(7, gap="medium")
        for i, day in enumerate(week):
            with cols[i]:
                if start_date <= day <= end_date:
                    st.markdown(f"### {day.day}")
                    todays_events = [
                        e for e in st.session_state["events"]
                        if e["date"] == day and e["category"] in selected_categories and e["type"] in selected_types]
                    for e in todays_events:
                        st.markdown(render_event_card(e), unsafe_allow_html=True)
                else:
                    st.write(" ")










