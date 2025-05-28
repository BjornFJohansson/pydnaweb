import streamlit as st
from pathlib import Path
from Bio.SeqUtils import MeltingTemp as _mt
import Bio
from pydna.tm import tm_default
from pydna.parsers import parse_primers

saltdict = {"1. 16.6 x log[Na+] (Schildkraut & Lifson (1965), Biopolymers 3: 195-208)": 1,
            "2. 16.6 x log([Na+]/(1.0 + 0.7*[Na+])) (Wetmur (1991), Crit Rev Biochem Mol Biol 126: 227-259)": 2,
            "3. 12.5 x log(Na+] (SantaLucia et al. (1996), Biochemistry 35: 3555-3562": 3,
            "4. 11.7 x log[Na+] (SantaLucia (1998), Proc Natl Acad Sci USA 95: 1460-1465": 4,
            "5. Correction for deltaS: 0.368 x (N-1) x ln[Na+] (SantaLucia (1998), Proc Natl Acad Sci USA 95: 1460-1465)": 5,
            "6. (4.29(%GC)-3.95)x1e-5 x ln[Na+] + 9.40e-6 x ln[Na+]^2 (Owczarzy et al. (2004), Biochemistry 43: 3537-3554)": 6,
            "7. Complex formula with decision tree and 7 empirical constants. Mg2+ is corrected for dNTPs binding (if present) (Owczarzy et al. (2008), Biochemistry 47: 5336-5353)": 7, }

nntabledict = {"DNA_NN1: values from Breslauer et al. (1986)": _mt.DNA_NN1,
               "DNA_NN2: values from Sugimoto et al. (1996)": _mt.DNA_NN2,
               "DNA_NN3: values from Allawi & SantaLucia (1997)": _mt.DNA_NN3,
               "DNA_NN4: values from SantaLucia & Hicks (2004)": _mt.DNA_NN4, }

title = Path(__file__).stem

st.header(title, divider="rainbow")

st.write("""[Bio.SeqUtils.MeltingTemp.Tm_NN](https://biopython.org/docs/1.75/api/Bio.SeqUtils.MeltingTemp.html#Bio.SeqUtils.MeltingTemp.Tm_NN)
         """)

# Define the structure of the matrix

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

default = """\
>MyPrimer
ATGGCAGTTGAGAAGA

>another
agtgtgctagtagtacgtcgta"""

defaults = {"check": True,
            "strict": True,
            "c_seq": None,
            "shift": 0,
            "nn_table": _mt.DNA_NN4,  # DNA_NN4: values from SantaLucia & Hicks (2004)
            "tmm_table": None,
            "imm_table": None,
            "de_table": None,
            "dnac1": 500 / 2,  # I assume 500 µM of each primer in the PCR mix
            "dnac2": 500 / 2,  # This is what MELTING and Primer3Plus do
            "selfcomp": False,
            "Na": 40,
            "K": 0,
            "Tris": 75.0,  # We use the 10X Taq Buffer with (NH4)2SO4 (above)
            "Mg": 1.5,  # 1.5 mM Mg2+ is often seen in modern protocols
            "dNTPs": 0.8,  # I assume 200 µM of each dNTP
            "saltcorr": 7,  # Tm ":  81.5 + 0.41(%GC) - 600/N + 16.6 x log[Na+]
            "func": _mt.Tm_NN, }  # Used by Primer3Plus to calculate the product Tm.

with st.form(key="matrix_form"):

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            submit = st.form_submit_button("Submit")
        with col2:
            if st.form_submit_button("clear"):
                st.session_state.text_area_content = ""
        with col3:
            if st.form_submit_button("fill with example data"):
                st.session_state.text_area_content = default

    with st.container():
        nn_table = st.selectbox("nn_table", list(nntabledict.keys()), index=3)
        saltcorr = st.selectbox("saltcorr", list(saltdict.keys()), index=6)

    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])

        with col1:
            Na = st.number_input("Na (mM)", min_value=0, key="Na", value=defaults["Na"])

        with col2:
            Tris = st.number_input("Tris (mM)", key="Tris", value=defaults["Tris"])

        with col3:
            Mg = st.number_input("Mg (mM)", key="Mg", value=defaults["Mg"])

        with col4:
            K = st.number_input("K (mM)", key="K", value=defaults["K"])

        with col5:
            dNTPs = st.number_input("dNTPs (mM)", key="dNTPs", value=defaults["dNTPs"])

        with col6:
            dnac1 = st.number_input("dnac1 (µM)", key="dnac1", value=defaults["dnac1"])

        with col7:
            dnac2 = st.number_input("dnac2 (µM)", key="dnac2", value=defaults["dnac2"])

        sequences = st.text_area("Enter at least one primer:",
                                 st.session_state.text_area_content,
                                 height=300,
                                 key="text_area_content",
                                 placeholder=default)


if submit:
    tm_results = ""

    primers = parse_primers(sequences)

    for primer in primers:
        tm = tm_default(primer.seq,
                        check=True,
                        strict=True,
                        c_seq=None,
                        shift=0,
                        nn_table=nntabledict[nn_table],
                        tmm_table=None,
                        imm_table=None,
                        de_table=None,
                        dnac1=dnac1,
                        dnac2=dnac2,
                        selfcomp=False,
                        Na=Na,
                        K=K,
                        Tris=Tris,
                        Mg=Mg,
                        dNTPs=dNTPs,
                        saltcorr=int(saltdict[saltcorr]), )

        primer.description = f" tm={round(tm, 2)} "

    argument = f"Biopython v{Bio.__version__}\n"
    argument += ", ".join(f"{k}: {globals()[k]}" for k in defaults.keys() if k in globals())
    argument += ")"

    st.code(argument, language=None)

    st.code("\n".join(p.format("primer") for p in primers), language=None)
