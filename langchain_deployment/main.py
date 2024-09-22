import streamlit as st
from streamlit_option_menu import option_menu
import try_  # Importing try.py where the app function is defined
import home 

# Set page configuration
st.set_page_config(page_title="Deployment Script Generator", page_icon=":rocket:", layout="wide")

# CSS for dark theme (optional, you can modify or remove it)
def render_dark_theme():
    st.markdown("""
        <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton>button {
            background-color: #00aaff;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 12em;
            margin: 30px auto;
            display: block;
        }
        .stButton>button:hover {
            background-color: #55C667;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, div, span {
            color: white !important;
        }
        .block-container {
            background-color: #1e1e1e;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Function to render the main application with a sidebar
def run_main_app():
    # Sidebar with options "Deploy Script" and "GitHub Assistant"
    with st.sidebar:
        selected_page = option_menu(
            menu_title='Options',  # Sidebar title
            options=['Get Script','Deploy App'],  # Added GitHub Assistant option
            icons=['rocket','github'],  # Proper GitHub icon from Bootstrap Icons
            menu_icon='menu-up',  # Sidebar menu icon
            default_index=0,  # Default selection
            styles={
                "container": {"padding": "5px", "background-color": '#1e1e1e'},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "color": "white", 
                    "font-size": "18px", 
                    "text-align": "left", 
                    "margin": "0px", 
                    "--hover-color": "#444444"
                },
                "nav-link-selected": {"background-color": "#00aaff"},
            }
        )

    # Logic to render the selected option
    if selected_page == 'Get Script':
        try_.app()  # Calls the app function from try.py

# Main flow control
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Check if the session is still on the home page or if the user clicked on a button
if st.session_state["page"] == "home":
    next_action = home.home_page()
    if next_action == "validate":
        st.session_state["page"] = "main"  # Change session state to the main app
elif st.session_state["page"] == "main":
    render_dark_theme()  # Call dark theme (optional)
    run_main_app()  # Run the main app
