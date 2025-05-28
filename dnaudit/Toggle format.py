import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent

default = """\
>myfastasequence
acgtctaggtcatttgctgatc

LOCUS       seq_8bp                    8 bp    DNA     linear   UNK 01-JAN-1980
DEFINITION  seq_8bp.
ACCESSION   seq_8bp
VERSION     seq_8bp
KEYWORDS    .
SOURCE      .
  ORGANISM  .
            .
FEATURES             Location/Qualifiers
ORIGIN
        1 gatacgta
//
"""

st.header(Path(__file__).stem, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""
col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("submit")
with col2:
    if st.button("clear"):
        st.session_state.text_area_content = ""
with col3:
    if st.button("fill with example data"):
        st.session_state.text_area_content = default

st.text_area("Enter two primers and one template:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
