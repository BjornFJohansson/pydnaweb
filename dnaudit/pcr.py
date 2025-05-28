import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent
from jinja2 import Template

from tabulate import tabulate


form = """\
---
limit: {{ limit }}
---
# pcr

{{ md_table }}

```
{{ amplicon.figure() }}
```

Suggested program for Taq DNA polymerase.
```
{{ amplicon.program()}}
```

```
>{{ fp.name }} {{ fp.seguid() }} (fw)
{{ fp.seq }}

>{{ rp.name }} {{ rp.seguid() }} (rv)
{{ rp.seq }}

>{{ template.name }} {{ template.seguid() }} (template)
{{ template.seq }}

>{{ amplicon.name }} {{ amplicon.seguid() }} (pcr product)
{{ amplicon.seq }}

"""




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

st.header(Path(__file__).stem, divider="rainbow")

limit = st.number_input("Annealing limit", min_value=0, value=13)

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

# Buttons to fill or clear the text area
# col1, col2 = st.columns(2)
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
    sequences = parse(st.session_state.text_area_content)
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
                data = [
                    ["fw primer", fp.name, len(fp), fp.seguid()],
                    ["rv primer", rp.name, len(rp), rp.seguid()],
                    ["template", template.name, len(template), template.seguid()],
                    ["pcr product", amplicon.name, len(amplicon), amplicon.seguid()],
                ]
                headers = ["Component", "Name", "Size", "Seguid"]
                md_table = tabulate(data,
                                    headers,
                                    tablefmt="github",
                                    colalign=("left", "left", "left", "left"))
                result_text += Template(form).render(**locals())

        else:
            result_text += "\n" + ann.template.format("gb")
        st.code(result_text, language=None)

st.text_area("Enter two primers and one template:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
