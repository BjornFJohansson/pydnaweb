import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pydna.fusionpcr import fuse_by_pcr
from pathlib import Path
from textwrap import dedent

default = """\
>left_fragment
AGGGGCTGTTAGTTATGGCCTGCGAGGATTCAAAAAGGGCCGATCCGGAG

>right_fragment
AAGGGCCGATCCGGAGAGACGGGCTTCAAAGCTGCCTGACGACGGTTGCGGGTCCGTATCAAAA"""

title = Path(__file__).stem

st.number_input("Annealing limit", min_value=1, value=12, key="limit")

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
    result_text = st.session_state.text_area_content
    limit = int(st.session_state.limit)
    sequences = parse(st.session_state.text_area_content)
    if len(sequences) < 2:
        result_text += f"Expected at least two sequences, found {len(sequences)}\n"
    else:
        fusion_products = fuse_by_pcr(sequences, limit=limit)

        result_text = "\n".join(f"""\
```
{s.figure()}
```

>{s.name}
{s.seq}

            """ for s in fusion_products) or "No assembly result.\n\nTry a shorter homology limit."

    st.code(result_text, language=None)

st.text_area("Enter two sequences:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
