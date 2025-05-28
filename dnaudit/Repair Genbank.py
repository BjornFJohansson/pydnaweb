import streamlit as st
from pydna.readers import read
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent
from pydna.genbankfixer import gbtext_clean

default = """\
LOCUS       mysequence   8 bp    DNA     linear   UNK 01-JAN-1980
DEFINITION  DEFINITION
ACCESSION   ACCESSION
VERSION     VERSION
KEYWORDS    KEYWORDS
SOURCE      SOURCE
  ORGANISM  ORGANISM
COMMENT     This file is malformed. Can not be read by Bio.SeqIO.read()
COMMENT     https://biopython.org/docs/latest/api/Bio.SeqIO.html#input-single-records
COMMENT     All fields but LOCUS and FEATURES are removed.
FEATURES             Location/Qualifiers
     misc_feature    3..6
                     /locus_tag="NewFeature"
                     /label="NewFeature"
                     /ApEinfo_label="NewFeature"
                     /ApEinfo_fwdcolor="cyan"
                     /ApEinfo_revcolor="green"
                     /ApEinfo_graphicformat="arrow_data {{0 0.5 0 1 2 0 0 -1 0
                     -0.5} {} 0} width 5 offset 0"
ORIGIN   1 gatacgta  //
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

if submit and st.session_state.text_area_content:
    result_text = ""

    s = st.session_state.text_area_content
    gbtext, json = gbtext_clean(s)

    result_text = read(gbtext).format()

    st.code(result_text, language=None)

st.text_area("Enter two primers and one template:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
