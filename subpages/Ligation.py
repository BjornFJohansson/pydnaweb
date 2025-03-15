import streamlit as st
from pydna.parsers import parse
from pathlib import Path

default = """\
>fragment1 linear alphabet=dsiupac
aaaPEXI

>fragment2 linear alphabet=dsiupac
QFZJccc
"""
cutoff_detailed_figure = 5

title = Path(__file__).stem

st.header(title, divider="rainbow")

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
    if len(sequences) < 2:
        result_text += f"Expected at least two sequences, found {len(sequences)}\n"
    else:
        sequences = parse(st.session_state.text_area_content)

        from pydna.ligate import ligate

        csequences, lsequences = ligate(sequences)

        result_text = "\n".join(f"""\
{s.format('fasta-2line')}
    """ for s in csequences)

        result_text += "\n".join(f"""\
{s.format('fasta-2line')}
    """ for s in lsequences)

        st.code(result_text, language=None)

st.text_area("Enter at least one sequence:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
