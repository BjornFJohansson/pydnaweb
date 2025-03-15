import streamlit as st
from streamlit_option_menu import option_menu


options = [
    "pydnaweb",
    "WebPCR",
    "Assembly designer",
    "Assembly simulator",
    "CrispR",
    "Fusion PCR",
    "Gateway",
    "Ligation",
    "Matching primer",
    "Melting temperature",
    "Primer designer",
    "Primer enumerator",
    "Repair Genbank",
    "Restriction digestion",
    "Restriction enzyme finder",
    "Seguid Calculator",
    "TAB format",
    "Toggle format",
    "Documentation",
    "about",
]


def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=options,  # Matches subpage names
            # icons=["fa-dna", "flask", "book"],  # Uses font-awesome icons
            menu_icon="menu-button-wide",
            default_index=0,
        )
    return selected
