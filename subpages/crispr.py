import streamlit as st
from pydna.parsers import parse
from pathlib import Path
from pydna.crispr import cas9
from pydna.crispr import protospacer
from pydna.dseqrecord import Dseqrecord
from textwrap import dedent
from jinja2 import Template

form = """\

# CrispR

´´´
{{ guideconstruct.format("fasta-2line") }}

{{ target.format("fasta-2line") }}
´´´



´´´
{% for fragment in target.cut(c9) %}
{{ fragment.format("fasta-2line") }}
{% endfor %}
´´´
"""

default = """\
>sgRNA construct (must contain a complete sgRNA)
GTTACTTTACCCGACGTCCCgttttagagctagaaatagcaagttaaaataagg

>cutting target
GTTACTTTACCCGACGTCCCaGG
"""
# cutoff_detailed_figure = 5

title = Path(__file__).stem

st.header(title, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# # Initialize session state for text area
# if "guide" not in st.session_state:
#     st.session_state.guide = ""

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
    guideconstruct, target = parse(st.session_state.text_area_content)
    ps, = protospacer(guideconstruct)
    c9 = cas9(ps)
    frag_repr = "´´´"
    sequences = ""
    for fragment in target.cut(c9):
        frag_repr += f"\n{repr(fragment.seq)}\n"
        sequences += fragment.format("fasta-2line") + "\n\n"
    frag_repr += "´´´"
    result_text = Template(form).render(**locals())
    st.code(result_text, language=None)

# st.text_area("guide construct:",
#              st.session_state.guide,
#              height=250,
#              key="guide",
#              placeholder=guide)

st.text_area("Enter at least one sequence:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
