import streamlit as st
import importlib.util

st.set_page_config(
    page_title="pydnaweb",
    page_icon="favicon.ico",
    layout="wide")

pydnaweb_page = st.Page("utilities/pydnaweb.py", title="home", icon=":material/home:", default=True)

pcr_page = st.Page("dnaudit/pcr.py", title="pcr", icon=":material/content_copy:")
cut_page = st.Page("dnaudit/cut.py", title="cut", icon=":material/content_cut:")
crispr_page = st.Page("dnaudit/crispr.py", title="crispr", icon=":material/download_2:")
ligation_page = st.Page("dnaudit/ligation.py", title="ligation", icon=":material/link:")
assembly_page = st.Page("dnaudit/assembly.py", title="assembly", icon=":material/polyline:")
fusion_pcr_page = st.Page("dnaudit/fusion_pcr.py", title="fusion pcr", icon=":material/genetics:")
gateway_page = st.Page("dnaudit/gateway.py", title="gateway", icon=":material/door_open:")

primer_design_page = st.Page("utilities/primer designer.py", title="Primer design", icon="🎨")
assembly_designer_page = st.Page("utilities/assembly designer.py", title="Assembly design", icon="📐")
matching_primer_page = st.Page("utilities/matching primer.py", title="Design matching primer", icon=":material/sync_alt:")
melting_temperature_page = st.Page("utilities/melting temperature.py", title="Melting", icon=":material/device_thermostat:")
primer_enumerator_page = st.Page("utilities/primer enumerator.py", title="Enumerate primer list", icon=":material/pin:")
repair_Genbank_file_page = st.Page("utilities/repair genbank.py", title="Repair Genbank file", icon=":material/healing:")
restriction_enzyme_finder_page = st.Page("utilities/restriction enzyme finder.py", title="Restriction enzyme finder", icon="🔎")
seguid_page = st.Page("utilities/seguid.py", title="Seguid calculator", icon="🗝️")
tab_format_page = st.Page("utilities/tab format.py", title="tab format", icon=":material/keyboard_tab:")
toggle_format_page = st.Page("utilities/toggle format.py", title="Toggle format", icon="🖲️")

doc_page = st.Page("documentation/documentation.py", title="docs", icon=":material/docs:")
about_page = st.Page("documentation/about.py", title="about", icon=":material/info:")

pg = st.navigation(
    {
        "home": [pydnaweb_page],

        "simulate": [pcr_page,
                     cut_page,
                     crispr_page,
                     ligation_page,
                     assembly_page,
                     fusion_pcr_page,
                     gateway_page],

        "design": [primer_design_page,
                   assembly_designer_page,
                   matching_primer_page],

        "utilities": [primer_enumerator_page,
                      repair_Genbank_file_page,
                      restriction_enzyme_finder_page,
                      seguid_page,
                      tab_format_page,
                      toggle_format_page,
                      melting_temperature_page],

        "documentation": [doc_page,
                          about_page],
    }
)

pg.run()















# import streamlit as st
# import importlib.util
# # from PIL import Image
# from sidebar import sidebar  # Import sidebar function

# # im = Image.open("favicon.ico")
# st.set_page_config(
#     page_title="pydnaweb",
#     page_icon="favicon.ico",
#     layout="wide")

# # Detect page changes
# if "last_selected_page" not in st.session_state:
#     st.session_state.last_selected_page = None

# # Hide Streamlit's default multi-page listing
# st.sidebar.empty()

# # Get selected page from sidebar
# selected_page = sidebar()

# # Reset session state when the page changes
# if st.session_state.last_selected_page != selected_page:
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]  # Clears all session variables
#     st.session_state.last_selected_page = selected_page  # Store new page

# # Function to load a page dynamically
# def load_page(page_name):
#     file_path = f"subpages/{page_name}.py"

#     try:
#         spec = importlib.util.spec_from_file_location("page_module", file_path)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#     except Exception as e:
#         st.error(f"Error loading page: {e}")

# # Load the selected page
# load_page(selected_page)
