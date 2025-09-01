# -----------------------
# GLOBAL STYLES (replace that block with this)
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

/* ====== FLEX COLUMN FIX ====== */
.stColumns {{
    display: flex;
    align-items: stretch;
}}
.stColumn > div {{
    height: 100%; /* make containers fill column height */
}}

/* Sidebar-like container styles */
div.st-key-leftbox, div.st-key-rightbox {{
    background-color: black;
    color: #9CCB3B;
    padding: 0.5rem;
    border-radius: 0.5rem;
    flex: 1; /* equal height columns */
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

/* ====== LIST VIEW EXPANDER ====== */

/* Force gradient on the clickable header button */
#listview-container button[data-testid="stExpanderToggle"] {{
    background: linear-gradient(135deg, #466069, #9CCB3B) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin-bottom: 8px !important;
    border: none !important;
}}
#listview-container button[data-testid="stExpanderToggle"] * {{
    color: white !important;
}}

/* Expander body */
#listview-container [data-testid="stExpanderContent"] {{
    background: linear-gradient(180deg, rgba(70,96,105,0.15), rgba(156,203,59,0.15)) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px !important;
}}

/* Day headers in list view */
#listview-container h3 {{
    color: white !important;
}}

/* ====== MONTH SELECT: keep gradient ====== */
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






