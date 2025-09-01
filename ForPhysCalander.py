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

# -----------------------
# COLORS
# -----------------------
banner_text_color_hex = "#9CCB3B"        # title/main heading
banner_bg_color_hex = "black"
container_text_color_hex = "#9CCB3B"

# -----------------------
# GLOBAL STYLES
# -----------------------
st.markdown(f"""
<style>
/* App background gradient */
.stApp {{
  background: linear-gradient(135deg, #CAD2D8, #7E96A0, #303434);
}}
.stApp > header {{ background-color: transparent; }}

/* Fixed header at top */
#fixed-header {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}}

/* Push main content below header */
main .block-container {{
  padding-top: 100px !important;
  max-width: 100% !important;
}}

/* Two fixed side-by-side panels */
.fixed-columns {{
  display: flex;
  gap: 1rem;
  height: calc(100vh - 120px); /* viewport height minus header */
}}

.left-panel, .right-panel {{
  flex: 1;
  background-color: black;
  border-radius: 10px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  overflow-y: auto;  /* independent scroll */
}}

.left-panel {{
  max-width: 280px;
  color: {container_text_color_hex};
}}

.right-panel {{
  flex: 3;
  color: white;
}}

/* Checkbox + radio labels */
.stCheckbox label, .stRadio label {{
    color: {container_text_color_hex} !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}}

/* Gradient event card */
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
def render_event_card(e):
    return f"""
    <div class="event-card">
        <b>{e['name']}</b><br>
        <small>{e['time']} @ {e['location']}</small><br>
        <small>{e['description']}</small>
    </div>
    """

# -----------------------
# FIXED TWO-COLUMN LAYOUT
# -----------------------
st.markdown('<div class="fixed-columns">', unsafe_allow_html=True)

# LEFT PANEL
with st.container():
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    st.subheader("Filters")
    select_all_categories = st.checkbox("All Organizations", value=True)
    selected_categories = CATEGORY_OPTIONS if select_all_categories else [
        cat for cat in CATEGORY_OPTIONS if st.checkbox(cat, value=True, key=f"cat_{cat}")]
    st.markdown("**Filter by Event Type:**")
    select_all_types = st.checkbox("All Event Types", value=True)
    selected_types = TYPE_OPTIONS if select_all_types else [
        t for t in TYPE_OPTIONS if st.checkbox(t, value=True, key=f"type_{t}")]
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT PANEL
with st.container():
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
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

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close fixed-columns







