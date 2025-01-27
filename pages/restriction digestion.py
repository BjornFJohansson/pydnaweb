import re
from pathlib import Path
from textwrap import dedent
import streamlit as st
from pydna.readers import read
from Bio.Restriction import AllEnzymes, RestrictionBatch

default = """\
>CYC1 YJR048W S. cerevisiae Cytochrome c isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaag
ggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagat
gccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtacc
aagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa"""

st.set_page_config(layout="wide")
title = Path(__file__).stem
st.header(title, divider="rainbow")

value = ""

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if st.session_state.clicked:
    value = default
    st.session_state.clicked = False

enzymes = st.text_input("Enzymes separated by space or comma:")

myenzymes = RestrictionBatch([e for e in AllEnzymes if str(e).lower() in re.split(r"\W+", enzymes.lower())])

text_entered = st.text_area("Enter a sequence to be digested:",
                            height = 300,
                            placeholder=default,
                            value = value)

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    submit = st.button("submit")
with col2:
    clear = st.button("clear")
# with col3:
#     clear = st.link_button("go to pydnaweb", "https://pydnaweb.streamlit.app")
with col4:
    example = st.button('example data')
    # st.session_state.clicked = True

if clear:
    st.empty()
    st.session_state.clicked = False
elif example:
    st.session_state.clicked = True
elif submit and text_entered and myenzymes:
    target = read(text_entered)
    results = target.cut(myenzymes)
    frag_repr = "´´´"
    sequences = ""
    for result in results:
        frag_repr += f"\n{repr(result.seq)}\n"
        sequences += result.format("fasta-2line") + "\n\n"
    frag_repr += "´´´\n\n"
    result_text = dedent("""\
    # cut

    enzymes: {enzymes}

    {frag_repr}

    >{target.name} {enzymes}
    {target.seq}

    {sequences}""").format(frag_repr=frag_repr,
                           enzymes=" ".join(str(e) for e in myenzymes),
                           target=target,
                           sequences=sequences)
    st.code(result_text, language=None)
