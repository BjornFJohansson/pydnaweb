import streamlit as st
from pathlib import Path
from pydna.parsers import parse
from pydna.readers import read
from pydna.amplify import Anneal
from pydna.design import assembly_fragments
from pydna.design import circular_assembly_fragments

default = """\
>f50 21-mer
CTTTCGAGAATACCAGAAAAA
>r50 21-mer
GTACAAGAATTGCACAATTCA
>a
CTTTCGAGAATACCAGAAAAAATGATTACTGAATTGTGCAATTCTTGTAC

<======>

>b
GATTTCCTTTTGGATACCTGAAACAAAGCCCATCGTGGTCCTTAGACTT

<======>

>f48 22-mer
CTTCATAAATAGATTGCCATAC
>r48 22-mer
ACTTTTTACTGATTCATAAGCT
>c
CTTCATAAATAGATTGCCATACATAGAGCTTATGAATCAGTAAAAAGT
"""

st.header(Path(__file__).stem, divider="rainbow")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.number_input("Overlap (bp)", min_value=4, value=25, key="overlap")
with col2:
    st.number_input("Maxlink (bp)", min_value=4, value=30, key="maxlink")
with col3:
    st.text_input("Separator", value="<======>", key="separator")
with col4:
    st.radio("topology", ["circular", "linear"], key="topology")
with col5:
    st.number_input("pcr limit (bp)", min_value=8, value=12, key="pcrlimit")

with col1:
    submit = st.button("submit")
with col2:
    if st.button("clear"):
        st.session_state.text_area_content = ""
with col3:
    if st.button("example data"):
        st.session_state.text_area_content = default


# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

st.text_area(f"Enter at least two sequences separated by {st.session_state.separator}",
             st.session_state.text_area_content,
             height=550,
             key="text_area_content",
             placeholder=default)


if submit and st.session_state.text_area_content:
    result_text = ""
    text = st.session_state.text_area_content

    separator = st.session_state.separator
    topology = st.session_state.topology
    overlap = st.session_state.overlap
    maxlink = st.session_state.maxlink
    pcrlimit = st.session_state.pcrlimit

    items = text.split(separator)
    sequences = []

    for item in items:
        try:
            fp, rp, tp = parse(item)
        except ValueError:
            try:
                seq = read(item)
            except ValueError:
                pass
        else:
            ann = Anneal((fp, rp), tp, limit=pcrlimit)  # TODO Tm_NN
            seq, *rest = ann.products

        sequences.append(seq)

    fragments = assembly_fragments(sequences,
                                   overlap=overlap,
                                   maxlink=maxlink,
                                   circular={"circular": True,
                                             "linear": False}[topology])

    result_items = []
    for item in fragments:

        if hasattr(item, "template"):
            result_items.append(

                    f"""\
>{item.forward_primer.name} {len(item.forward_primer)}-mer
{item.forward_primer.seq}
>{item.reverse_primer.name} {len(item.reverse_primer)}-mer
{item.reverse_primer.seq}
>{item.template.name}
{item.template.seq}"""

            )
        else:
            result_items.append(item.format("primer"))

    result_text = f"\n{separator}\n".join(result_items)
    st.code(result_text, language=None)
