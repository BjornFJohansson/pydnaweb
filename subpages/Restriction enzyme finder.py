import streamlit as st
from pydna.readers import read
from Bio.Restriction import RestrictionBatch
from Bio.Restriction import CommOnly
from Bio.Restriction import AllEnzymes
from Bio.Restriction import EcoRI, SacI, KpnI, SmaI, BamHI, XbaI, SalI, PstI, SphI, HindIII
from pathlib import Path
from typing import Iterable
from itertools import batched
from jinja2 import Template

pucmcs = RestrictionBatch((EcoRI, SacI, KpnI, SmaI, BamHI, XbaI, SalI, PstI, SphI, HindIII))

batch = { "Commercially avaliable (CommOnly)": CommOnly,
          "All rebase enzymes (AllEnzymes)": AllEnzymes,
          "User defined": None}


form = """\


"""

default_enzymes = " ".join(str(e) for e in pucmcs)

default = """\
>CYC1 YJR048W S. cerevisiae Cytochrome c isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaag
ggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagat
gccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtacc
aagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa"""

st.header(Path(__file__).stem, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# Initialize session state for text area
if "enzymes" not in st.session_state:
    st.session_state.enzymes = ""

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("fill with example data"):
        st.session_state.text_area_content = default
        st.session_state.enzymes = default_enzymes

with col2:
    if st.button("clear"):
        st.session_state.text_area_content = ""
        st.session_state.enzymes = ""

def format_iterable_in_rows(data: Iterable[str], n: int) -> str:
    rows = [" ".join(str(item) for item in batch) for batch in batched(data, n)]
    return "\n".join(rows)

def analyze():
    raw_text = st.session_state.text_area_content
    s = read(raw_text)
    myenzymes = RestrictionBatch([e for e in AllEnzymes if str(e).lower() in st.session_state.enzymes.lower()])

    # s.no_cutters(batch)
    # s.twice_cutters(batch)
    # s.n_cutters(batch)
    # s.cutters(batch)

    result_text = f"{format_iterable_in_rows(sorted(s.unique_cutters(batch)), 10)}"

    st.code(result_text, language=None)


with st.form('analysis'):
    st.form_submit_button("Submit", on_click=analyze)

    st.radio("Restriction batch", batch, horizontal=True, key="batch")

    st.text_area("Enter restriction enzymes:",
                 st.session_state.enzymes,
                 height=200,
                 key="enzymes_area_content",
                 placeholder=default_enzymes)

    st.text_area("Enter a sequence to analyze:",
                 st.session_state.text_area_content,
                 height=350,
                 key="text_area_content",
                 placeholder=default)
