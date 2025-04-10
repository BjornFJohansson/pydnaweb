import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent
from pydna.myprimers import PrimerList
from pydna.readers import read_primer
from pydna.parsers import parse_primers

default = """\
>3CCP1clon
CGATGTCGACTTAGATCTCTAAACCTTGTTCCTCT

>5CCP1clon
GATCGGCCGGATCCAAATGACTACTGCTGTTAGGC

>3CYC1clon
CGATGTCGACTTAGATCTCACAGGCTTTTTTCAAG

>5CYC1clone
GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

>S1 67bp primer for amplification of GFP from pFA6a-GFPS65T-kanMX6.
GATTCGAACGTCTCAAAGACATATGAGGAGCATATTGAGACCGTTAGTAAAGGAGAAGAACTTTTC
"""

st.header(Path(__file__).stem, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

col1, col2, col3, col4 = st.columns(4)
with col1:
    startnumber = st.number_input("start number", min_value=0, value=1, key="startnumber")
col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("submit")
with col2:
    if st.button("clear"):
        st.session_state.text_area_content = ""
with col3:
    if st.button("fill with example data"):
        st.session_state.text_area_content = default

if submit and st.session_state.text_area_content:
    result_text = ""

    s = st.session_state.text_area_content
    pl = PrimerList([read_primer(f">{startnumber-1}_fakeprimer\na")])
    result_text += pl.assign_numbers(parse_primers(s))

    st.code(result_text, language=None)
else:
    st.text_area("Enter a list of primers:",
                 st.session_state.text_area_content,
                 height=350,
                 key="text_area_content",
                 placeholder=default)
