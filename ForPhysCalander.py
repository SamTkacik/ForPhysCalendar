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

banner_text_color_hex = "#9CCB3B"        # title/main heading
banner_bg_color_hex = "black"
event_card_text_color_hex = "#FFFFFF"
filter_accent_color_hex = "#9CCB3B"
container_bg_color_hex = "#466069"
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

/* Make page content fill viewport height so columns can stretch */
main .block-container {{
  min-height: 100vh;
}}

/* Sidebar-like container styles + stretch */
div.st-key-leftbox, div.st-key-rightbox {{
    background-color: black;
    color: #9CCB3B;
    padding: 0.5rem;
    border-radius: 0.5rem;
    min-height: calc(100vh - 220px);
    display: flex;
    flex-direction: column;
}}

/* Checkbox + radio labels */
.stCheckbox label, .stRadio label {{
    color: {container_text_color_hex} !important;
    font-weight: 500 !important;
}}

/* ====== EXPANDABLE EVENT CARDS ====== */
.event-card {{
    border-radius: 12px;
    margin-bottom: 10px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}}
/* Header (closed state) */
.event-card [data-testid="stExpander"] > div:first-child {{
    background: linear-gradient(135deg, #303434, #466069) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    border: none !important;
    transition: background 0.3s ease, transform 0.2s ease;
}}
.event-card [data-testid="stExpander"]:hover > div:first-child {{
    background: linear-gradient(135deg, #466069, #9CCB3B) !important;
    transform: scale(1.01);
}}
/* Body (expanded content) */
.event-card [data-testid="stExpanderContent"] {{
    background: linear-gradient(180deg, rgba(70,96,105,0.15), rgba(156,203,59,0.15)) !important;
    color: white !important;
    border-radius: 0 0 12px 12px !important;
    padding: 12px !important;
    animation: fadeIn 0.4s ease;
}}
/* Smooth fade for content */
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(-4px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

/* Day headers in list view */
#listview-container h3 {{
    color: white !important;
}}

/* Month select styling */
div.st-key-monthbox [data-baseweb="select"] > div {{
    background: linear-gradient(135deg, #466069, #9CCB3B) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 500;
    min-height: 38px !important;
    line-height: 1.4em !important;
    padding: 0 10px !important;
    display: flex;
    align-items: center;
}}
div.st-key-monthbox ul[role="listbox"] {{
    background: linear-gradient(135deg, #303434, #466069) !important;
    border-radius: 10px !important;
}}
div.st-key-monthbox ul[role="listbox"] li {{
    color: white !important;
    font-weight: 500;
    line-height: 1.4em !important;
    padding: 6px 10px !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stContainer"][key="leftbox"] {
        height: 650px;
        overflow-y: auto;
    }
    [data-testid="stContainer"][key="rightbox"] {
        height: 650px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# BANNER TITLE
# -----------------------
st.markdown(
    f"""
    <div style='background-color:{banner_bg_color_hex}; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;'>
        <h1 style='color:{banner_text_color_hex}; margin:0;'>USF Physics Fall 25 Calendar</h1>
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
            "date": datetime.date(2025, 9, 5),
            "name": "Welcome Party",
            "category": "PGSC",
            "type": "Recreational",
            "time": "2:30-5:30 PM",
            "location": "ISA 5010",
            "description": "A great way to start the semester with pizza (that's free!), friends, and fun physics trivia!"
        },
        {
            "date": datetime.date(2025, 9, 3),
            "name": "Colloquium",
            "category": "Department of Physics",
            "type": "Academic/Professional",
            "time": "2:00-3:15 PM",
            "location": "ISA 2023",
            "description": "USF Physics Alumni Talk – John Kline"
        }
    ]

# -----------------------
# HELPER: Render Event Card
# -----------------------
def render_event_card(e):
    """Expandable gradient card for an event."""
    st.markdown('<div class="event-card">', unsafe_allow_html=True)
    with st.expander(f"📌 {e['name']} — {e['time']} @ {e['location']}"):
        st.markdown(f"**Category:** {e['category']}")
        st.markdown(f"**Type:** {e['type']}")
        st.markdown(f"**Location:** {e['location']}")
        st.markdown(f"**Time:** {e['time']}")
        st.markdown(f"**Description:** {e['description']}")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# FILTERS 
# -----------------------
col1, col2 = st.columns([1, 3])
with col1:
    with st.container(key="leftbox", border=True):
        st.subheader("Filters")
        st.markdown("**Filter by Organization:**")
        select_all_categories = st.checkbox("Select/Deselect All Organizations", value=True)
        selected_categories = CATEGORY_OPTIONS if select_all_categories else [
            cat for cat in CATEGORY_OPTIONS if st.checkbox(cat, value=True, key=f"cat_{cat}")]
        st.markdown("**Filter by Event Type:**")
        select_all_types = st.checkbox("Select/Deselect All Event Types", value=True)
        selected_types = TYPE_OPTIONS if select_all_types else [
            t for t in TYPE_OPTIONS if st.checkbox(t, value=True, key=f"type_{t}")]

# -------------------
# RIGHT COLUMN
# -------------------
with col2:
    with st.container(key="rightbox", border=True):
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

        cal = calendar.Calendar(firstweekday=6)  # Sunday start
        month_days = cal.monthdatescalendar(chosen_year, chosen_month_num)

        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        cols = st.columns(7, gap="medium")
        for i, d in enumerate(weekdays):
            with cols[i]:
                st.markdown(f"**{d}**")
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
                            render_event_card(e)
                    else:
                        st.write(" ")

st.markdown("---")
st.subheader("Request an Event")
st.markdown(
    "[Click here to open request form](https://forms.gle/rqTyiU4EXt2mowg6A)"
)



















