import streamlit as st
import pandas as pd
import datetime
import calendar

# -----------------------
# MASTER SETTINGS
# -----------------------
st.set_page_config(layout="wide")

CATEGORY_OPTIONS = ["Department of Physics", "PGSC", "SPS", "GAU", "Other"]
TYPE_OPTIONS = ['Academic/Professional', 'Recreational', 'Interdisciplinary', 'Other']

start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

banner_text_color_hex = "#9CCB3B"
banner_bg_color_hex = "black"
event_card_text_color_hex = "#FFFFFF"
filter_accent_color_hex = "#9CCB3B"
container_bg_color_hex = "#466069"
container_text_color_hex = "#9CCB3B"

# -----------------------
# GLOBAL STYLES
# -----------------------
st.markdown("""
<style>
/* App background gradient */
.stApp {
  background: linear-gradient(135deg, #CAD2D8, #7E96A0, #303434);
}
.stApp > header {background-color: transparent;}

/* Gradient event card (shared) */
.event-card {
    background: linear-gradient(135deg, #303434, #466069);
    color: white;
    padding: 6px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-weight: 500;
}

/* Expander header */
div[data-testid="stExpander"] > div:first-child {
    background: linear-gradient(135deg, #466069, #9CCB3B) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin-bottom: 8px !important;
}
/* Expander body */
div[data-testid="stExpander"] > div:nth-child(2) {
    background: linear-gradient(180deg, rgba(70,96,105,0.15), rgba(156,203,59,0.15)) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

/* Sidebar-like container styles */
div.st-key-leftbox, div.st-key-rightbox {
    background-color: black;
    color: #9CCB3B;
    padding: 0.5rem;
}

/* Checkbox + radio labels */
.stCheckbox label, .stRadio label {
    color: %s !important;
    font-weight: 500 !important;
}
</style>
""" % container_text_color_hex, unsafe_allow_html=True)

# -----------------------
# BANNER TITLE
# -----------------------
st.markdown(
    f"""
    <div style='background-color:{banner_bg_color_hex}; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;'>
        <h1 style='color:{banner_text_color_hex}; margin:0;'>USF Physics Fall 25 Calendar</h1>
    </div>
    """,
    unsafe_allow_html=True)

# -----------------------
# SESSION STATE EVENTS
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

# -----------------------
# HELPER: Render Event Card
# -----------------------
def render_event_card(e, compact=False):
    """Return HTML for an event card with gradient background."""
    if compact:
        return f"""
        <div class="event-card">
            <b>{e['name']}</b><br>
            <small>{e['time']} @ {e['location']}</small>
        </div>
        """
    else:
        return f"""
        <div class="event-card">
            <b>{e['name']}</b><br>
            <p><b>Time:</b> {e['time']}</p>
            <p><b>Location:</b> {e['location']}</p>
            <p><b>Description:</b> {e['description']}</p>
        </div>
        """

# -----------------------
# FILTERS + VIEW OPTIONS
# -----------------------
col1, col2 = st.columns([1, 3])
with col1:
    with st.container(key="leftbox", border=True, height=650):
        st.subheader("Filters")
        # Org filters
        st.markdown("**Filter by Organization:**")
        select_all_categories = st.checkbox("Select/Deselect All Organizations", value=True)
        selected_categories = CATEGORY_OPTIONS if select_all_categories else [
            cat for cat in CATEGORY_OPTIONS if st.checkbox(cat, value=True, key=f"cat_{cat}")]
        # Type filters
        st.markdown("**Filter by Event Type:**")
        select_all_types = st.checkbox("Select/Deselect All Event Types", value=True)
        selected_types = TYPE_OPTIONS if select_all_types else [
            t for t in TYPE_OPTIONS if st.checkbox(t, value=True, key=f"type_{t}")]

with col2:
    with st.container(key="rightbox", border=True, height=650):
# -----------------------
# GRID VIEW
# -----------------------
        st.subheader("Events")

        months = sorted(set((d.year, d.month) for d in all_dates))
        chosen_month = st.selectbox(
            "Select Month",
            [datetime.date(y, m, 1).strftime("%B %Y") for y, m in months])
        chosen_year, chosen_month_num = [
            (y, m) for (y, m) in months
        if datetime.date(y, m, 1).strftime("%B %Y") == chosen_month][0]

        cal = calendar.Calendar(firstweekday=6)  # Sunday start
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
                            st.markdown(render_event_card(e, compact=True), unsafe_allow_html=True)
                    else:
                        st.write(" ")











