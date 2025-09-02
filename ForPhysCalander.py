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
/* Shared gradient event card */
.event-card {{
    background: linear-gradient(135deg, #303434, #466069);
    color: white;
    padding: 6px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-weight: 500;
}}
/* ====== LIST VIEW EXPANDER: robust header + body styling ====== */
/* Header clickable area – match several Streamlit variants */
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
/* Ensure header text/icons inside the header are white */
#listview-container [data-testid="stExpander"] > div:first-child * {{
    color: white !important;
}}
/* Body/content area (expander content) – match variants */
#listview-container [data-testid="stExpander"] [data-testid="stExpanderContent"],
#listview-container [data-testid="stExpander"] > div:nth-child(2) {{
    background: linear-gradient(180deg, rgba(70,96,105,0.15), rgba(156,203,59,0.15)) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px !important;
}}
/* Day headers in list view */
#listview-container h3 {{
    color: white !important;
}}
/* ====== MONTH SELECT: restore gradient styling, scoped to container key ====== */
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

#########################################################################################################################################
############## For updating events on site ###########################################################################################################################
#########################################################################################################################################
def mkevent(date, name, category, type, time, location, description):
    info = [date, name, time, location, description]
    for i in info:
        if i is None:
            i = 'N/A'
    if category not in CATEGORY_OPTIONS:
        category = 'Other'
    if type not in TYPE_OPTIONS:
        type = 'Other'
    return {'date':date, 'name':name,
            'category':category, 'type':type,
            'time':time,'location':location,
            'description':description}
def dt(year, month, day):
    return datetime.date(year, month, day)

if "events" not in st.session_state:
    st.session_state["events"] = [
        mkevent(dt(2025, 9, 5),'Welcome Party',
                'PGSC','Recreational',
                '2:30-5:30 PM','ISA 5010',
                "A great way to start the semester with pizza (that's free!), friends, and \
                        fun physics trivia!"),
        mkevent(dt(2025, 9, 3),'Colloquium',
                'Department of Physics', 'Academic/Professional',
                '2:00-3:15 PM', 'ISA 2023',
                'USF Physics Alumni Talk-John Kline')
    ]
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

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
# FILTERS 
# -----------------------
col1, col2 = st.columns([1, 3])
with col1:
    # removed fixed height=650 so CSS min-height can stretch to viewport
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
        
def card_click(event, card_html):
    key = f"{event['name']}_{event['date']}"
    container = st.container()
    with container:
        st.markdown(card_html, unsafe_allow_html=True)
        # Instead of invisible overlay, use a small visible button
        if st.button("View Details", key=f"btn_{key}"):
            st.session_state["selected_event"] = event


# -------------------
# RIGHT COLUMN
# -------------------
with col2:
    with st.container(key="rightbox", border=True):
            st.subheader("📆 Events")

            months = sorted(set((d.year, d.month) for d in all_dates))
            # Scope the selectbox in a keyed container so CSS only affects this widget
            with st.container(key="monthbox"):
                chosen_month = st.selectbox("Select Month",
                    [datetime.date(y, m, 1).strftime("%B %Y") for y, m in months])
            chosen_year, chosen_month_num = [(y, m) for (y, m) in months
                if datetime.date(y, m, 1).strftime("%B %Y") == chosen_month][0]

            cal = calendar.Calendar(firstweekday=6)  # Sunday start
            month_days = cal.monthdatescalendar(chosen_year, chosen_month_num)

            weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            # Header row using same column structure
            cols = st.columns(7, gap="medium")
            for i, d in enumerate(weekdays):
                with cols[i]:
                    st.markdown(f"**{d}**")  # bold weekday name
            st.write("---" * 15)  # optional separator

            for week in month_days:
                cols = st.columns(7, gap="medium")
                for i, day in enumerate(week):
                    with cols[i]:
                        if start_date <= day <= end_date:
                            st.markdown(f"### {day.day}")
                            todays_events = [e for e in st.session_state["events"]
                                if e["date"] == day and e["category"] in selected_categories and e["type"] in selected_types]
                            for e in todays_events:
                                #st.markdown(render_event_card(e, compact=True), unsafe_allow_html=True)
                                if card_click(e, render_event_card(e, compact=True)):
                                    st.session_state["selected_event"] = e
                        else:
                            st.write(" ")

st.markdown("---")
st.subheader("Request an Event")
st.markdown(
    "[Click here to open request form](https://forms.gle/rqTyiU4EXt2mowg6A)")

# =====================
# MODAL POPUP OVERLAY
# =====================
if st.session_state.get("selected_event"):
    e = st.session_state["selected_event"]

    st.markdown("""
    <style>
      /* Fullscreen dark overlay */
      .modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
      }
      /* Modal box */
      .modal-box {
        background: linear-gradient(135deg, #303434, #466069);
        color: white;
        padding: 20px 24px;
        border-radius: 12px;
        width: min(520px, 92vw);
        position: relative;
        box-shadow: 0 8px 28px rgba(0,0,0,0.45);
      }
      /* Close button */
      .modal-close {
        position: absolute;
        top: 10px;
        right: 12px;
        background: #9CCB3B;
        color: black;
        border: none;
        border-radius: 8px;
        padding: 2px 10px;
        font-weight: 700;
        cursor: pointer;
      }
    </style>
    """, unsafe_allow_html=True)

    # Modal HTML with close button using a Streamlit button
    st.markdown(f"""
    <div class="modal-overlay">
      <div class="modal-box">
        <button class="modal-close" onclick="window.parent.postMessage({{type: 'closeModal'}}, '*')">✕</button>
        <h3>{e['name']}</h3>
        <p><b>Date:</b> {e['date']}</p>
        <p><b>Time:</b> {e['time']}</p>
        <p><b>Location:</b> {e['location']}</p>
        <p>{e['description']}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Small JS snippet to clear modal without a full rerun
    st.markdown("""
    <script>
    window.addEventListener('message', (event) => {
      if (event.data.type === 'closeModal') {
        const streamlitEvent = new Event("streamlit:closeModal");
        window.dispatchEvent(streamlitEvent);
      }
    });
    </script>
    """, unsafe_allow_html=True)

    # Listen for the event and clear session state
    import streamlit as st_js_event  # avoid name clash
    if st_js_event.session_state.get("_closeModal_triggered"):
        st.session_state.pop("selected_event", None)
        st.session_state["_closeModal_triggered"] = False
    else:
        # Register the custom event listener only once
        st_js_event.session_state["_closeModal_triggered"] = False



    with st.container(key="modal_overlay"):
        with st.container(key="modal_box"):
            if st.button("✕", key="modal_close"):
                st.session_state.pop("selected_event", None)
                st.rerun()

            st.markdown(f"### {e['name']}")
            st.write(f"**Date:** {e['date']}")
            st.write(f"**Time:** {e['time']}")
            st.write(f"**Location:** {e['location']}")
            st.write(e['description'])
























