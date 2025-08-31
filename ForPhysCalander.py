import streamlit as st
import pandas as pd
import datetime
import calendar

# -----------------------
# 🔧 MASTER SETTINGS
# -----------------------
st.set_page_config(layout="wide")

CATEGORY_OPTIONS = ["Department of Physics", "PGSC", "SPS", "GAU", "Other"]
TYPE_OPTIONS = ['Academic/Professional', 'Recreational', 'Interdisciplinary', 'Other']

start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2025, 12, 31)
all_dates = pd.date_range(start_date, end_date).to_list()

# -----------------------
# Banner Title (ALWAYS FIRST)
# -----------------------
#banner_text_color_hex = st.color_picker("Banner Text Color", "#9CCB3B")  # default white
#banner_bg_color_hex = st.color_picker("Banner Background Color", "#303434")  # default navy
#event_card_text_color_hex = st.color_picker("Event Card Text Color", "#000000")  # default black
#event_card_bg_color_hex = st.color_picker("Event Card Background Color", "#E0E0E0")  # default light gray
banner_text_color_hex = "#9CCB3B"       # white text
banner_bg_color_hex = '#303434' #"#466069"         # 
event_card_text_color_hex = "#000000"   # black text for event cards
event_card_bg_color_hex = "#E0E0E0"     # light gray background for event cards
filter_accent_color_hex = "#9CCB3B"
container_bg_color_hex = "#466069"
container_text_color_hex = "#9CCB3B"

st.markdown(
    f"""
    <div style='background-color:{banner_bg_color_hex}; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;'>
        <h1 style='color:{banner_text_color_hex}; margin:0;'>USF Physics Calendar - Fall 2025</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <style>
    /* Streamlit form elements primary color */
    :root {{
        --primary-color: {filter_accent_color_hex};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------
# EVENTS (Hard-coded for now)
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
            cat for cat in CATEGORY_OPTIONS if st.checkbox(cat, value=True, key=f"cat_{cat}")
        ]

        # Type filters
        st.markdown("**Filter by Event Type:**")
        select_all_types = st.checkbox("Select/Deselect All Event Types", value=True)
        selected_types = TYPE_OPTIONS if select_all_types else [
            t for t in TYPE_OPTIONS if st.checkbox(t, value=True, key=f"type_{t}")
        ]

        # View selector
        st.subheader("View Options")
        view_mode = st.radio("Choose view:", ["List View", "Grid View"], horizontal=True)

st.html("""
<style>
/* Target the container by its key-generated class */
div.st-key-leftbox {
    background-color: #303434;   /* your color */
    color: #9CCB3B;                 /* text color for contrast */
    padding: 0.5rem;              /* optional */
}
div.st-key-leftbox * {{
    color: {container_text_color_hex} !important;
}}
</style>
""")

# -------------------
# LIST VIEW
# -------------------
with col2:
    with st.container(key="rightbox", border=True, height=650):
        if view_mode == "List View":
            st.subheader("🗓 Events")
            for d in all_dates:
                day = d.date()
                events_today = [
                    e for e in st.session_state["events"]
                    if e["date"] == day and e["category"] in selected_categories and e["type"] in selected_types
                ]
                if events_today:
                    st.markdown(f"### {d.strftime('%A, %B %d, %Y')}")
                    for e in events_today:
                        with st.expander(f"**{e['name']}** ({e['category']}, {e['type']})"):
                            st.write(f"**Time:** {e['time']}")
                            st.write(f"**Location:** {e['location']}")
                            st.write(f"**Description:** {e['description']}")

    # -------------------
    # GRID VIEW
    # -------------------
        else:
            st.subheader("📆 Events")

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

            # Render grid
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
                                if e["date"] == day and e["category"] in selected_categories and e["type"] in selected_types
                            ]
                            for e in todays_events:
                                st.markdown(
                                    f"""
                                    <div style='background-color:#e6f2ff; padding:6px; 
                                    border-radius:6px; margin-bottom:6px;'>
                                        <b>{e['name']}</b><br>
                                        <small>{e['time']} @ {e['location']}</small>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                        else:
                            st.write(" ")

st.html("""
<style>
/* Target the container by its key-generated class */
div.st-key-rightbox {
    background-color: #303434;   /* your color */
    color: #9CCB3B;                 /* text color for contrast */
    padding: 0.5rem;              /* optional */
}
div.st-key-leftbox * {{
    color: {container_text_color_hex} !important;
}}
</style>
""")


