from pathlib import Path
import streamlit as st
from pydna.readers import read
from Bio.Restriction import CommOnly, EcoRI, KpnI # AllEnzymes

default = """\
>CYC1 YJR048W S. cerevisiae Cytochrome c, isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaagggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagatgccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtaccaagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa
"""

st.set_page_config(layout="wide")
title = Path(__file__).stem
st.header(title, divider="rainbow")

value = ""

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if st.session_state.clicked:
    value = default
    st.session_state.clicked = False

text_entered = st.text_area("Enter two primers and one template:",
                            height = 300,
                            placeholder=default,
                            value = value)

col1, col2, col3 = st.columns([1,1,1])

with col1:
    submit = st.button("submit")
with col2:
    clear = st.button("clear")
with col3:
    example = st.button('example data')
    st.session_state.clicked = True

if clear:
    st.empty()
    st.session_state.clicked = False
elif example:
    st.session_state.clicked = True
elif submit and text_entered:
    sequence = read(text_entered)
    results = sequence.cut(EcoRI, KpnI)
    for result in results:
        st.code(f"´´´\n{repr(result.seq)}\n´´´", language=None)
        st.code(result.format("fasta-2line"), language=None)
        st.divider()
