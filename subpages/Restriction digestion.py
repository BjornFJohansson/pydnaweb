import re
from pathlib import Path
from textwrap import dedent
import streamlit as st
from pydna.readers import read
from Bio.Restriction import AllEnzymes, RestrictionBatch

default_enzymes = "KpnI"

default = """\
>CYC1 YJR048W S. cerevisiae Cytochrome c isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaag
ggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagat
gccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtacc
aagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa"""

title = Path(__file__).stem
st.header(title, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

if "enzymes" not in st.session_state:
    st.session_state.enzymes = ""

st.text_input("Restriction enzymes separated by space or comma:",
              st.session_state.enzymes,
              key="enzymes",
              placeholder=default_enzymes)

col1, col2, col3, col4 = st.columns(4)
# Buttons to fill or clear the text area
with col1:
    submit = st.button("submit")
with col2:
    if st.button("clear"):
        st.session_state.text_area_content = ""
with col3:
    if st.button("fill with example data"):
        st.session_state.text_area_content = default
        #st.session_state.enzymes = default_enzymes

if submit and st.session_state.text_area_content and st.session_state.enzymes:
    target = read(st.session_state.text_area_content)
    myenzymes = RestrictionBatch([e for e in AllEnzymes if str(e).lower() in re.split(r"\W+", st.session_state.enzymes.lower())])
    results = target.cut(myenzymes)
    frag_repr = "´´´"
    sequences = ""
    for result in results:
        frag_repr += f"\n{repr(result.seq)}\n"
        sequences += result.format("fasta-2line") + "\n\n"
    frag_repr += "´´´"
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



st.text_area("Enter a sequence to be digested:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
