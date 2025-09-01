import streamlit as st
import pandas as pd
import datetime
import calendar
import re
from urllib.parse import quote

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
# GLOBAL STYLES (reverted to your original palette)
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
/* Sidebar-like container styles + make them stretch to bottom */
div.st-key-leftbox, div.st-key-rightbox {{
    background-color: black;
    color: #9CCB3B;
    padding: 0.5rem;
    border-radius: 0.5rem;
    /* Stretch to bottom (adjust 220px if your header/content spacing changes) */
    min-height: calc(100vh - 220px);
    display: flex;
    flex-direction: column;
}}
/* Checkbox + radio labels */
.stCheckbox label, .stRadio label {{
    color: {container_text_color_hex} !important;
    font-weight: 500 !important;
}}
/* Shared gradient event card (compact calendar tile) */
.event-card {{
    background: linear-gradient(135deg, #303434, #466069);
    color: white;
    padding: 6px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-weight: 500;
}}

/* ====== LIST VIEW EXPANDER (kept scoped; not used here) ====== */
#listview-container [data-testid="stExpander"] > div:first-child,
#listview-container [data-testid="stExpander"] > div > button,
#listview-container [data-testid="stExpander"] summary,
#listview-container [data-testid="stExpander"] [data-testid="stExpanderToggle"] {{
    background: linear-gradient(135deg, #466069, #9CCB3B) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin-bottom: 8px !important;
    border: none !important;
}}
#listview-container [data-testid="stExpander"] > div:first-child * {{
    color: white !important;
}}
#listview-container [data-testid="stExpander"] [data-testid="stExpanderContent"],
#listview-container [data-testid="stExpander"] > div:nth-child(2) {{
    background: linear-gradient(180deg, rgba(70,96,105,0.15), rgba(156,203,59,0.15)) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px !important;
}}
#listview-container h3 {{
    color: white !important;
}}

/* ====== MONTH SELECT (scoped) ====== */
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

/* ====== EVENT DETAIL PAGE CARDS ====== */
.detail-card {{
    background: linear-gradient(135deg, #303434, #466069);
    color: white;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
}}
.detail-meta {{
    background: linear-gradient(180deg, rgba(70,96,105,0.15), rgba(156,203,59,0.15));
    border-radius: 10px;
    padding: 10px;
    color: white;
}}
.detail-title {{
    color: {banner_text_color_hex};
    margin: 0;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stContainer"][key="leftbox"] {
        height: 650px;
        overflow-y: auto; /* scroll if content exceeds */
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
    unsafe_allow_html=True)

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
            "description": "USF Physics Alumni Talk-John Kline"
        }
    ]

# -----------------------
# UTILITIES
# -----------------------
def slugify(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def event_id(e: dict) -> str:
    return f"{e['date'].strftime('%Y%m%d')}-{slugify(e['name'])}"

def index_events_with_ids():
    for e in st.session_state["events"]:
        if "id" not in e:
            e["id"] = event_id(e)

def get_event_by_id(eid: str):
    for e in st.session_state["events"]:
        if e.get("id") == eid:
            return e
    return None

def google_calendar_url(e: dict) -> str:
    """Build a Google Calendar 'Add event' URL. Falls back to all-day if time parse fails."""
    title = quote(e["name"])
    details = quote(f"{e['description']} (Category: {e['category']}, Type: {e['type']})")
    location = quote(e["location"])
    # Try to parse "H:MM-H:MM AM/PM" or "H-H:MM PM" styles
    start_dt = None
    end_dt = None
    try:
        # Normalize like "2:30-5:30 PM" or "2:00-3:15 PM"
        times = e["time"].strip().upper().replace("–", "-").replace("—", "-")
        # Extract AM/PM (if only one given, assume both share it)
        meridiem = "AM" if "AM" in times and "PM" not in times else ("PM" if "PM" in times else None)
        times_clean = times.replace("AM", "").replace("PM", "").strip()
        start_s, end_s = [t.strip() for t in times_clean.split("-", 1)]
        def parse_hm(s):
            if ":" in s:
                h, m = s.split(":")
            else:
                h, m = s, "00"
            return int(h), int(m)
        sh, sm = parse_hm(start_s)
        eh, em = parse_hm(end_s)
        # If original string had explicit AM/PM markers per side, refine
        def find_meridiem_for(part, default_meridiem):
            if part.endswith("AM"):
                return "AM"
            if part.endswith("PM"):
                return "PM"
            return default_meridiem
        start_mer = find_meridiem_for(times.split("-",1)[0], meridiem)
        end_mer = find_meridiem_for(times.split("-",1)[1], meridiem)
        def to24(h, mer):
            if mer == "AM":
                return 0 if h == 12 else h
            if mer == "PM":
                return 12 if h == 12 else h + 12
            return h
        sh24 = to24(sh, start_mer)
        eh24 = to24(eh, end_mer)
        start_dt = datetime.datetime.combine(e["date"], datetime.time(sh24, sm))
        end_dt = datetime.datetime.combine(e["date"], datetime.time(eh24, em))
        # If end < start (crosses midnight), add one day
        if end_dt <= start_dt:
            end_dt = end_dt + datetime.timedelta(days=1)
        dates_param = f"{start_dt.strftime('%Y%m%dT%H%M%S')}/{end_dt.strftime('%Y%m%dT%H%M%S')}"
    except Exception:
        # All-day fallback
        day = e["date"].strftime("%Y%m%d")
        next_day = (e["date"] + datetime.timedelta(days=1)).strftime("%Y%m%d")
        dates_param = f"{day}/{next_day}"
    return (
        "https://www.google.com/calendar/render"
        f"?action=TEMPLATE&text={title}&dates={dates_param}&details={details}&location={location}"
    )

# Index IDs once
index_events_with_ids()

# -----------------------
# RENDER HELPERS
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

def render_event_detail_page(e):
    st.button("← Back to calendar", type="secondary", on_click=lambda: (st.experimental_set_query_params(), st.experimental_rerun()))
    st.markdown(
        f"""
        <div class="detail-card" style="margin-top:10px;margin-bottom:12px;">
            <h2 class="detail-title">{e['name']}</h2>
            <div class="detail-meta" style="margin-top:8px;">
                <div><b>Date:</b> {e['date'].strftime('%A, %B %d, %Y')}</div>
                <div><b>Time:</b> {e['time']}</div>
                <div><b>Location:</b> {e['location']}</div>
                <div><b>Organization:</b> {e['category']}</div>
                <div><b>Type:</b> {e['type']}</div>
            </div>
            <div style="margin-top:12px;">
                <p style="margin:0;"><b>Description:</b> {e['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # Action buttons/links
    cal_url = google_calendar_url(e)
    cols = st.columns([1,1,4])
    with cols[0]:
        st.link_button("Add to Google Calendar", cal_url)
    with cols[1]:
        st.button("Back to calendar", on_click=lambda: (st.experimental_set_query_params(), st.experimental_rerun()))

    st.markdown("---")
    st.subheader("Request an Event")
    st.markdown("[Click here to open request form](https://forms.gle/rqTyiU4EXt2mowg6A)")

# -----------------------
# ROUTING (Calendar vs Event Detail)
# -----------------------
qp = st.experimental_get_query_params()
selected_event_id = qp.get("event", [None])[0]

if selected_event_id:
    # Detail page
    e = get_event_by_id(selected_event_id)
    if not e:
        st.warning("That event wasn't found. Returning to the calendar.")
        st.experimental_set_query_params()
        st.experimental_rerun()
    else:
        render_event_detail_page(e)
else:
    # -------------------
    # CALENDAR PAGE (with filters)
    # -------------------
    col1, col2 = st.columns([1, 3])

    with col1:
        with st.container(key="leftbox", border=True):
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
                                if e["date"] == day and e["category"] in selected_categories and e["type"] in selected_types
                            ]
                            for e in todays_events:
                                st.markdown(render_event_card(e, compact=True), unsafe_allow_html=True)
                                # Detail navigation button (routes via URL param)
                                if st.button("View details", key=f"view_{e['id']}"):
                                    st.experimental_set_query_params(event=e["id"])
                                    st.experimental_rerun()
                        else:
                            st.write(" ")

    st.markdown("---")
    st.subheader("Request an Event")
    st.markdown("[Click here to open request form](https://forms.gle/rqTyiU4EXt2mowg6A)")




















