import streamlit as st

col1, col2, col3 = st.columns(3)
with col2:
    st.image("pydna_logo_769x1057.png", caption="pydna", width=300)

st.markdown("""

[Pydnaweb](https://github.com/BjornFJohansson/pydnaweb) exposes some of the functionality of
the [pydna](https://github.com/pydna-group/pydna?tab=readme-ov-file#-pydna)
package as an online service.

All tools accept sequences in FASTA or Genbank format. Formats can generally be mixed.

If you have questions not answered [here](pages/Documentation) or suggestions, create an [issue](https://github.com/BjornFJohansson/pydnaweb/issues)
on the Github repository for Pydnaweb.

Development of Pydna & Pydnaweb is led by Björn Johansson at the
Department of Biology, University of Minho.
""")




#| WebPCR simulator                 | Simulate PCR if you already have a pair of primers and a template sequence.                                       |
#| Primer designer                  | Design a new primer pair for a template sequence or list of template sequences.                                   |
#| Matching primer                  | Design a primer to match an existing primer for a primer/template pair or list of such pairs.                     |
#| Assembly designer                | Design primers for linear or circular assembly of a list of amplicons or sequence fragments.                      |
#| Assembly simulator               | Simulator for linear or circular assembly of a list of sequence fragments.                                        |
#| Primer Tm calculator             | Melting temperature calculator for PCR primers. Uses the Bio.SeqUtils.MeltingTemp.Tm_NN function from Biopython.  |
#| Restriction simulator            | Simulate restriction digestion.                                                                                   |
#| CRISPr simulator                 | Simulate CRISPr digestion.                                                                                        |
#| Toggle format                    | Reformat sequences in GenBank or FASTA format.                                                                    |
#| Repair GenBank                   | Repair malformed GenBank files.                                                                                   |
#| Gateway                          | Simulate Gateway cloning.                                                                                         |
#| SEGUID                           | Calculate SEGUID checksums for protein or DNA sequences.                                                          |
#| Fusion PCR                       | Simulate fusion PCR.                                                                                              |
#| Primer enumerator                | Assign numbers to primers in a list (FASTA or GenBank format). Nunmber will be prepended to identifier.           |
#| Format primer list in TAB format | Format primer list in TAB format. Required for many companies selling oligonucleotides.                           |
#| Documentation                    | Documentation and examples.
