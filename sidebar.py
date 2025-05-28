import streamlit as st
from streamlit_option_menu import option_menu


options = [
    "pcr",
    "cut",
    "crispr",
    "ligation",
    "assembly",
    "fusion_pcr",
    "gateway",
    "",
    "Experiment",
    "Primer designer",
    "Assembly designer",
    "Matching primer",
    "Melting temperature",
    "Primer enumerator",
    "Repair Genbank",
    "Restriction enzyme finder",
    "Seguid Calculator",
    "TAB format",
    "Toggle format",
    "Documentation",
    "About",]


def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="dnaudit",
            options=options,
            menu_icon="menu-button-wide",
            default_index=0,
        )

    return selected
