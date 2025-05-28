import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent
from pydna.design import primer_design
from jinja2 import Template

form = """\
# Matching primer
```
{{ amplicon.figure() }}
```

```
>{{ amplicon.forward_primer.name }} {{ amplicon.forward_primer|length }}-mer {{ amplicon.forward_primer.seguid() }} (forward primer)
{{ amplicon.forward_primer.seq }}

>{{ amplicon.reverse_primer.name }} {{ amplicon.reverse_primer|length }}-mer {{ amplicon.forward_primer.seguid() }} (reverse primer)
{{ amplicon.reverse_primer.seq }}

>{{ amplicon.template.name }} {{ amplicon.template.seguid() }} (template)
{{ amplicon.template.seq }}
```
"""

default = """\
>1_5CYC1clone
GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

>CYC1 YJR048W S. cerevisiae Cytochrome c, isoform 1
atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagac
tagatgtctacaatgccacaccgtggaaaagggtggcccacataaggttggtc
caaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcg
tacacagatgccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtc
agagtacttgactaacccaaagaaatatattcctggtaccaagatggcctttg
gtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaa
gcctgtgagtaa
"""

st.header(Path(__file__).stem, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""
col1, col2, col3, col4 = st.columns(4)
with col1:
    limit = st.number_input("Annealing limit", min_value=1, value=13)
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

    templates = parse(st.session_state.text_area_content)

    amplicon = None

    result_text = ""

    for p, template in zip(templates[::2], templates[1::2]):
        try:
            amplicon = primer_design(template, fp=p, limit=limit)  # TODO Tm_NN
        except ValueError:  # ValueError
            pass
        try:
            amplicon = primer_design(template, rp=p, limit=limit)  # TODO Tm_NN
        except ValueError:  # ValueError
            pass

        if not amplicon:
            result_text = "Primer does not anneal."
        else:
            result_text = Template(form).render(**locals())

        st.code(result_text, language=None)


st.text_area("Enter one primers and one template:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
