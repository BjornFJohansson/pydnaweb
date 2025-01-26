import streamlit as st
from pydna.parsers import parse
from pydna.amplify import pcr
from pydna.primer import Primer
from pathlib import Path

default = """\
>1_5CYC1clone
GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

>2_3CYC1clon
CGATGTCGACTTAGATCTCACAGGCTTTTTTCAAG

>CYC1 YJR048W S. cerevisiae Cytochrome c isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaag
ggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagat
gccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtacc
aagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa
"""

title = Path(__file__).stem

st.set_page_config(layout="wide")
st.header(title, divider="rainbow")

value = ""

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if st.session_state.clicked:
    value = default
    st.session_state.clicked = False

limit = st.number_input("Annealing limit", min_value = 0, value=13)

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
    fp, rp, template = parse(text_entered)
    fp = Primer(str(fp.seq))
    rp = Primer(str(rp.seq))
    result = pcr(fp, rp, template, limit=limit)
    st.code(f"´´´\n{result.figure()}\n´´´", language=None)
    st.divider()
    st.code(result.format("fasta"), language=None)
else:
    st.session_state.clicked = False
