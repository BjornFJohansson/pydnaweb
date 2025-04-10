import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent
from pydna.design import primer_design

default = """\
>CYC1 YJR048W S. cerevisiae Cytochrome c, isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagac
tagatgtctacaatgccacaccgtggaaaagggtggcccacataaggttggtc
caaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcg
tacacagatgccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtc
agagtacttgactaacccaaagaaatatattcctggtaccaagatggcctttg
gtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaa
gcctgtgagtaa

>CYC7 YEL039C S. cerevisiae Cytochrome c, isoform 2
ATGGCTAAAGAAAGTACGGGATTCAAACCAGGCTCTGCAAAAAAGGGTGCTAC
ATTGTTTAAAACGAGGTGTCAGCAGTGTCATACAATAGAAGAGGGTGGTCCTA
ACAAAGTTGGACCTAATTTACATGGTATTTTTGGTAGACATTCAGGTCAGGTA
AAGGGTTATTCTTACACAGATGCAAACATCAACAAGAACGTCAAATGGGATGA
GGATAGTATGTCCGAGTACTTGACGAACCCAAAGAAATATATTCCTGGTACCA
AGATGGCGTTTGCCGGGTTGAAGAAGGAAAAGGACAGAAACGATTTAATTACT
TATATGACAAAGGCTGCCAAATAG
 """

st.header(Path(__file__).stem, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# Buttons to fill or clear the text area
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.number_input("Annealing limit", min_value=0, value=13, key="pcrlimit")
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
    templates = parse(st.session_state.text_area_content)
    pcrlimit = st.session_state.pcrlimit
    result_text = ""

    for template in templates:
        amplicon = primer_design(template, limit=pcrlimit)  # TODO Tm_NN

        if amplicon:
            result_text += f"""\
>{amplicon.forward_primer.name} {len(amplicon.forward_primer)}-mer
{amplicon.forward_primer.seq}
>{amplicon.reverse_primer.name} {len(amplicon.reverse_primer)}-mer
{amplicon.reverse_primer.seq}
>{amplicon.template.name}
{amplicon.template.seq}

"""
    st.code(result_text, language=None)

st.text_area("Enter one or more sequences:",
             st.session_state.text_area_content,
             height=550,
             key="text_area_content",
             placeholder=default)
