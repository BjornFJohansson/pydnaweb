import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent

default = """\
>a
atgaggcgcttttaaatatggcgaaAtaagtgatttaacgctttgaatatg

>b
taagtgatttaacgctttgaatatgCCactatatacttaaatttgatttcgt

>c
actatatacttaaatttgatttcgtGGGatgaggcgcttttaaatatggcgaa
"""
cutoff_detailed_figure = 5

title = Path(__file__).stem

st.set_page_config(layout="wide")
st.header(title, divider="rainbow")

limit = st.number_input("Annealing limit", min_value=0, value=13)

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# Buttons to fill or clear the text area
col1, col2 = st.columns(2)
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
    sequences = parse(st.session_state.text_area_content)
    if not len(sequences) < 2:
        result_text += f"Expected three sequences, found {len(sequences)}\n"
    else:

        st.code(result_text, language=None)

st.text_area("Enter at least two sequences:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
