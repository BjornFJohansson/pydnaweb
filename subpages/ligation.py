import streamlit as st
from pydna.parsers import parse
from pathlib import Path
from jinja2 import Template

form = """\
---
topology: {{ topology }}
---
# ligate
{% for s in sequences: %}
{{ s.format('fasta-2line') }}
{% endfor %}
<!-- ligation products below this comment -->
{% for s in newsequences: %}
{{ s.format('fasta-2line') }}
{% endfor %}
"""




default = """\
>fragment1 linear alphabet=dsiupac
QFZaaaPEXI

>fragment2 linear alphabet=dsiupac
QFZJcccPEX
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
    topology = st.session_state.topology
    result_text = ""
    sequences = parse(st.session_state.text_area_content)
    if len(sequences) < 2:
        result_text += f"Expected at least two sequences, found {len(sequences)}\n"
    else:
        sequences = parse(st.session_state.text_area_content)

        from pydna.ligate import ligate

        csequences, lsequences = ligate(sequences)

        newsequences = csequences if topology == "circular" else lsequences

        for s in newsequences:
            s.stamp()

        result_text = Template(form).render(**locals())

        st.code(result_text, language=None)

st.text_area("Enter at least one sequence:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
