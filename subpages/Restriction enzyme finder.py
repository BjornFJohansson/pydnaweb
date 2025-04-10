import streamlit as st
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.primer import Primer
from pathlib import Path
from textwrap import dedent

default = """\
>3CCP1clon
CGATGTCGACTTAGATCTCTAAACCTTGTTCCTCT

>5CCP1clon
GATCGGCCGGATCCAAATGACTACTGCTGTTAGGC

>3CYC1clon
CGATGTCGACTTAGATCTCACAGGCTTTTTTCAAG

>5CYC1clone
GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

>S1 67bp primer for amplification of GFP from pFA6a-GFPS65T-kanMX6.
GATTCGAACGTCTCAAAGACATATGAGGAGCATATTGAGACCGTTAGTAAAGGAGAAGAACTTTTC
"""

st.header(Path(__file__).stem, divider="rainbow")

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""
col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("submit")
with col2:
    if st.button("clear"):
        st.session_state.text_area_content = ""
with col3:
    if st.button("fill with example data"):
        st.session_state.text_area_content = default


# form = EnumForm(formdata=MultiDict(user_data))

# s = user_data.get("sequences")

# if not s:
#     return render_template("enum.html", form=form)

# result_text = ""

# try:
#     startnumber = int(user_data.get("startnumber"))
# except ValueError:
#     startnumber = 1

# pl = PrimerList([read_primer(f">{startnumber-1}_fakeprimer\na")])

# result_text += pl.assign_numbers(parse_primers(s))

# return render_template("result.html", result=result_text)


st.text_area("Enter two primers and one template:",
             st.session_state.text_area_content,
             height=350,
             key="text_area_content",
             placeholder=default)
