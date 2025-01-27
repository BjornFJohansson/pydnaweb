import streamlit as st
from PIL import Image

im = Image.open("favicon.ico")
st.set_page_config(
    page_title="Pydnaweb!",
    page_icon=im,
    layout="wide")

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("pydna_512x512_trsp.png", caption="pydna", width=300)

st.markdown("""

[Pydnaweb](https://github.com/BjornFJohansson/pydnaweb) exposes some of the functionality of
the [pydna](https://github.com/pydna-group/pydna?tab=readme-ov-file#-pydna)
package as an online service.

All tools accept sequences in FASTA or Genbank format. Formats can generally be mixed.

If you have question not answered below or suggestions, create an [issue](https://github.com/BjornFJohansson/pydnaweb/issues)
on the Github repository for Pydnaweb.

Development of Pydna & Pydnaweb is led by Björn Johansson at the
Department of Biology, University of Minho.
""")
