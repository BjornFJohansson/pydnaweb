import streamlit as st
import importlib.util
from sidebar import sidebar  # Import sidebar function

st.set_page_config(page_title="pydnaweb", layout="wide")

# Detect page changes
if "last_selected_page" not in st.session_state:
    st.session_state.last_selected_page = None

# Hide Streamlit's default multi-page listing
st.sidebar.empty()

# Get selected page from sidebar
selected_page = sidebar()

# Reset session state when the page changes
if st.session_state.last_selected_page != selected_page:
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # Clears all session variables
    st.session_state.last_selected_page = selected_page  # Store new page

# Function to load a page dynamically
def load_page(page_name):
    file_path = f"subpages/{page_name}.py"

    try:
        spec = importlib.util.spec_from_file_location("page_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        st.error(f"Error loading page: {e}")

# Load the selected page
load_page(selected_page)
