import streamlit as st
from pydna.readers import read
from pathlib import Path
from pydna.crispr import cas9
from pydna.crispr import protospacer
from pydna.dseqrecord import Dseqrecord
from textwrap import dedent

guide = """\
>minimal sgRNA construct
GTTACTTTACCCGACGTCCCgttttagagctagaaatagcaagttaaaataagg
"""

default = """\
>target
GTTACTTTACCCGACGTCCCaGG
"""
cutoff_detailed_figure = 5

title = Path(__file__).stem

st.header(title, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# Initialize session state for text area
if "guide" not in st.session_state:
    st.session_state.guide = ""

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
        st.session_state.guide = guide

if submit and st.session_state.text_area_content and st.session_state.guide:
    result_text = ""
    guideconstruct = read(st.session_state.guide)
    ps, = protospacer(guideconstruct)
    c9 = cas9(ps)
    target = read(st.session_state.text_area_content)
    frag_repr = "´´´"
    sequences = ""
    for fragment in target.cut(c9):
        frag_repr += f"\n{repr(fragment.seq)}\n"
        sequences += fragment.format("fasta-2line") + "\n\n"
    frag_repr += "´´´"
    result_text = dedent("""\
    # crispr

    {frag_repr}

    {sequences}""").format(frag_repr=frag_repr,
                           sequences=sequences)
    st.code(result_text, language=None)

st.text_area("guide construct:",
             st.session_state.guide,
             height=250,
             key="guide",
             placeholder=guide)

st.text_area("Enter at least one sequence:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
