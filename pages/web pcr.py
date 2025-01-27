import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent, indent
from PIL import Image

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
cutoff_detailed_figure = 5

report_template = """\

Forward: {amplicon.forward_primer.name} Reverse: {amplicon.reverse_primer.name}

```
{amplicon.figure()}
```

Taq DNA pol
{amplicon.program()}
DNA pol w DNA binding domain (PHUSION)
{amplicon.dbd_program()}

>{amplicon.name}
{amplicon.seq}

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

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    submit = st.button("submit")
with col2:
    clear = st.button("clear")
with col3:
    clear = st.link_button("Go to pydnaweb", "https://streamlit.io/gallery")
with col4:
    example = st.button('example data')
    st.session_state.clicked = True


if clear:
    st.empty()
    st.session_state.clicked = False
elif example:
    st.session_state.clicked = True
elif submit and text_entered:
    result_text = ""
    sequences = parse(text_entered)
    if not len(sequences) == 3:
        result_text += f"Expected three sequences, found {len(sequences)}\n"
    else:
        fp, rp, template = sequences
        fp = Primer(str(fp.seq), name=fp.name)
        rp = Primer(str(rp.seq), name=rp.name)
        ann = Anneal((fp, rp), template, limit=limit)
        products = ann.products
        result_text = ""
        if len(products) == 0:
            result_text += ann.report().strip()
        elif 1 <= len(products) <= cutoff_detailed_figure:
            result_text = ""
            for amplicon in products:
                result_text += dedent("""\
                # PCR

                Forward: {amplicon.forward_primer.name} Reverse: {amplicon.reverse_primer.name}

                {figure}

                Taq DNA pol
                {taq}

                DNA pol with an ssDNA binding domain, such as Phusion DNA pol.
                {phu}


                >{fp.name}
                {fp.seq}

                >{rp.name}
                {rp.seq}

                >{template.name}
                {template.seq}

                >{amplicon.name}
                {amplicon.seq}""").format(fp=fp,
                                          rp=rp,
                                          template=template,
                                          amplicon=amplicon,
                                          figure=amplicon.figure(),
                                          taq=amplicon.program(),
                                          phu=amplicon.dbd_program())
        else:
            result_text += "\n" + ann.template.format("gb")

        st.code(result_text, language=None)
else:
    st.session_state.clicked = False
