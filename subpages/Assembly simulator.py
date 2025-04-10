import streamlit as st
from pydna.parsers import parse
from pydna.assembly import Assembly
from pathlib import Path

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

st.header(title, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# Buttons to fill or clear the text area
col1, col2 = st.columns(2)

with col1:
    st.number_input("Recombination limit", min_value=0, value=13, key="limit")
with col2:
    st.radio("topology", ["circular", "linear"], horizontal=True, key="topology")


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
    if len(sequences) < 2:
        result_text += f"Expected at least two sequences, found {len(sequences)}\n"
    else:
        asm = Assembly(sequences, limit=st.session_state.limit)
        if st.session_state.topology == "circular":
            candidates = asm.assemble_circular()
        else:
            candidates = asm.assemble_linear()

        result_text = "\n".join(f"""\
Figure:

{candidate.figure()}

Detailed figure:

{candidate.detailed_figure()}

Resulting sequence:

>{candidate.name} { {False:'linear',True:'circular'}[candidate.circular] }
{candidate.seq}
    """ for candidate in candidates) or "No assembly result.\n\nTry a shorter homology limit."

    st.code(result_text, language=None)




st.text_area("Enter at least two sequences:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
