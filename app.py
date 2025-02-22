#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""docstring.


>65bp_PCR_prod
CTTTCGAGAATACCAGAAAAAATGATTACTGAATTGTGCAATTCTTGTACGATTTCCTTTTGGAT

>b
GATTTCCTTTTGGATACCTGAAACAAAGCCCATCGTGGTCCTTAGACTT



65bp_PCR_prod|15
              \/
              /\
              15|b

Detailed figure:

CTTTCGAGAATACCAGAAAAAATGATTACTGAATTGTGCAATTCTTGTACGATTTCCTTTTGGAT
                                                  GATTTCCTTTTGGAT
                                                  GATTTCCTTTTGGATACCTGAAACAAAGCCCATCGTGGTCCTTAGACTT



"""


# import datetime
import re
from itertools import chain
from textwrap import dedent


from flask_wtf import FlaskForm

from flask import Flask
from flask import render_template
from flask import request

from werkzeug.datastructures import MultiDict

# from wtforms import widgets
from wtforms.fields import SelectField
from wtforms.fields import SelectMultipleField
from wtforms.fields import DecimalField
from wtforms.fields import TextAreaField
from wtforms.fields import StringField
from wtforms.fields import SubmitField
from wtforms.fields import RadioField
from wtforms.fields import IntegerField

from Bio.SeqUtils import MeltingTemp as _mt
from Bio.SeqUtils.MeltingTemp import Tm_NN
from Bio import __version__ as bpversion
from Bio.Restriction import AllEnzymes, CommOnly
from Bio.Restriction import RestrictionBatch

from pydna import __version__ as version
from pydna.parsers import parse
from pydna.parsers import parse_primers
from pydna.readers import read
from pydna.readers import read_primer
from pydna.myprimers import PrimerList
from pydna.amplify import Anneal
from pydna.design import primer_design
from pydna.design import assembly_fragments
from pydna.design import circular_assembly_fragments
from pydna.assembly import Assembly
from pydna.tm import tm_default
from pydna.genbankfixer import gbtext_clean
from seguid import lsseguid as _lsseguid
from seguid import csseguid as _csseguid
from seguid import ldseguid as _ldseguid
from seguid import cdseguid as _cdseguid

tab = str.maketrans("GATCRYWSMKHBVDNgatcrywsmkhbvdn",
                    "CTAGYRWSKMDVBHNctagyrwskmdvbhn")

table = "GC,AT,TA,CG,RY,YR,WW,SS,MK,KM,HD,BV,VB,DH,NN"

def rc(s):
    """doctring."""
    return s.translate(tab)[::-1]


def seqfilter(seq):
    """doctring."""
    return "".join(b for b in seq.upper() if b in "GATCRYWSMKHBVDN")


def lsseguid(s):
    return _lsseguid(s.upper(), table = table)


def csseguid(s):
    return _csseguid(s.upper(), table = table)


def ldseguid(s):
    return _ldseguid(s.upper(), rc(s.upper()), 0, table = table)


def cdseguid(s):
    return _cdseguid(s.upper(), rc(s.upper()), table = table)






allenzymes = sorted(AllEnzymes, key=str)
commonly = sorted(CommOnly, key=str)
sixcutters = [e for e in commonly if e.size == 6]
morethansixcutters = [e for e in commonly if e.size > 6]
lessthansixcutters = [e for e in commonly if e.size < 6]


pcrlimit = 12
recombinationlimit = 25
proteinlimit = 100


default = {
    "Biopython_version": bpversion,
    "func": f"{Tm_NN.__module__}.{Tm_NN.__name__}",
    "nn_table": 4,
    "dnac1": 250,
    "dnac2": 250,
    "Na": 40,
    "K": 0,
    "Tris": 75.0,
    "Mg": 1.5,
    "dNTPs": 0.8,
    "saltcorr": 7,
}


nn_tableoptions = [
    (1, "DNA_NN1 - Breslauer et al. (1986), " "Proc Natl Acad Sci USA 83: 3746-3750"),
    (2, "DNA_NN2 - Sugimoto et al. (1996)," " Nuc Acids Res 24 : 4501-4505"),
    (3, "DNA_NN3 - Allawi and SantaLucia (1997)," " Biochemistry 36: 10581-10594"),
    (
        4,
        "DNA_NN4 - SantaLucia & Hicks (2004)," " Annu. Rev. Biophys. Biomol. Struct 33: 415-440",
    ),
]


saltoptions = [
    (1, "1. 16.6 x log[Na+] (Schildkraut & Lifson" " (1965), Biopolymers 3: 195-208)"),
    (
        2,
        "2. 16.6 x log([Na+]/(1.0 + 0.7*[Na+])) (Wetmur" " (1991), Crit Rev Biochem Mol Biol 126: 227-259)",
    ),
    (3, "3. 12.5 x log(Na+] (SantaLucia et al. (1996)," " Biochemistry 35: 3555-3562"),
    (
        4,
        "4. 11.7 x log[Na+] (SantaLucia (1998)," " Proc Natl Acad Sci USA 95: 1460-1465",
    ),
    (
        5,
        "5. Correction for deltaS: 0.368 x (N-1) x ln[Na+] (Santa"
        "Lucia (1998), Proc Natl Acad Sci USA 95: 1460-1465)",
    ),
    (
        6,
        "6. (4.29(%GC)-3.95)x1e-5 x ln[Na+] + 9.40e-6 x ln[Na+]^2"
        " (Owczarzy et al. (2004), Biochemistry 43: 3537-3554)",
    ),
    (7, "7. Complex formula with decision tree and" " 7 empirical constants."),
]


crispr_systems = [
    ("cas9", "cas9 system"),
]


class FusionPCRForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
    >fp
    ggatccAGGGGCTGTTAGTTATGG

    >rp
    ggatccTTTTGATACGGACCCGCA

    >left_fragment
    AGGGGCTGTTAGTTATGGCCTGCGAGGATTCAAAAAGGGCCGATCCGGAG

    >right_fragment
    AAGGGCCGATCCGGAGAGACGGGCTTCAAAGCTGCCTGACGACGGTTGCGGGTCCGTATCAAAA
    """
    )

    sequences = TextAreaField("primer_text", default=default)

    limit = IntegerField("limit", default=pcrlimit)

    send = SubmitField("submit")


class WebPCRForm(FlaskForm):
    """docstring."""

    default = dedent("""\
    >1_5CYC1clone
    GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

    >2_3CYC1clon
    CGATGTCGACTTAGATCTCACAGGCTTTTTTCAAG

    >CYC1 YJR048W S. cerevisiae Cytochrome c, isoform 1
    atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaagggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagatgccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtaccaagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa
    """)

    sequences = TextAreaField("primer_text", default=default)

    limit = IntegerField("limit", default=pcrlimit)

    send = SubmitField("submit")


class TranslationForm(FlaskForm):
    """docstring."""

    default = dedent("""\
    >359bp_PCR_prod
    GATCGGCCGGATCCAAATGACTGAATTCAAGGCCGgttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaagggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagatgccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtaccaagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctaCTTGAAAAAAGCCTGTGAGATCTAAGTCGACATCG
    """)

    sequence = TextAreaField("sequence_text", default=default)

    limit = IntegerField("protein length limit (aa)", default=proteinlimit)

    send = SubmitField("submit")


class RepairForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
        LOCUS       mysequence   8 bp    DNA     linear   UNK 01-JAN-1980
        DEFINITION  DEFINITION
        ACCESSION   ACCESSION
        VERSION     VERSION
        KEYWORDS    KEYWORDS
        SOURCE      SOURCE
          ORGANISM  ORGANISM
        COMMENT     This file is malformed. Can not be read by Bio.SeqIO.read()
        COMMENT     https://biopython.org/docs/latest/api/Bio.SeqIO.html#input-single-records
        COMMENT     All fields but LOCUS and FEATURES are removed.
        FEATURES             Location/Qualifiers
             misc_feature    3..6
                             /locus_tag="NewFeature"
                             /label="NewFeature"
                             /ApEinfo_label="NewFeature"
                             /ApEinfo_fwdcolor="cyan"
                             /ApEinfo_revcolor="green"
                             /ApEinfo_graphicformat="arrow_data {{0 0.5 0 1 2 0 0 -1 0
                             -0.5} {} 0} width 5 offset 0"
        ORIGIN   1 gatacgta  //

    """
    )

    sequence = TextAreaField("gbsequence", default=default)

    send = SubmitField("submit")


class ToggleForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
        >myfastasequence
        acgtctaggtcatttgctgatc

        LOCUS       seq_8bp                    8 bp    DNA     linear   UNK 01-JAN-1980
        DEFINITION  seq_8bp.
        ACCESSION   seq_8bp
        VERSION     seq_8bp
        KEYWORDS    .
        SOURCE      .
          ORGANISM  .
                    .
        FEATURES             Location/Qualifiers
        ORIGIN
                1 gatacgta
        //

    """
    )

    sequence = TextAreaField("sequences", default=default)

    send = SubmitField("submit")


class ToTABForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
        >5_5NUC1clon(N)
        GATAGATCTAGACTAGTCAAATGTGCAGTAGGATACTCTTG

        >4_3CCP1clon
        CGATGTCGACTTAGATCTCTAAACCTTGTTCCTCT

        >3_5CCP1clon
        GATCGGCCGGATCCAAATGACTACTGCTGTTAGGC

        >2_3CYC1clon
        CGATGTCGACTTAGATCTCACAGGCTTTTTTCAAG

        >1_5CYC1clone
        GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

        >0_S1 67bp primer for amplification of GFP from pFA6a-GFPS65T-kanMX6.
        GATTCGAACGTCTCAAAGACATATGAGGAGCATATTGAGACCGTTAGTAAAGGAGAAGAACTTTTC

        """
    )

    sequences = TextAreaField("sequences", default=default)

    send = SubmitField("submit")


class EnumForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
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
    )

    startnumber = StringField("startnumber", default=1)
    sequences = TextAreaField("sequences", default=default)

    send = SubmitField("submit")


MultiCheckboxField = SelectMultipleField


class DigestForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
>pUCmu 1669bp circular
ACGCGTCGCGAGGCCATATGGGTTAACCCATGGCCAAGCTTGCATGCCTGCAGGTCGACTCTAGAGGATCCCGGGTACCGAGCTCGAATTCGGATATCCTCGAGACTAGTGGGCCCGTTTAAACACATGTGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCCTGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTCAGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAGCGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATCTGCGCTCTGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGGTGGTTTTTTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAAGAAGATCCTTTGATCTTTTCTACTACCAATGCTTAATCAGTGAGGCACCTATCTCAGCGATCTGTCTATTTCGTTCATCCATAGTTGCCTGACTCCCCGTCGTGTAGATAACTACGATACGGGAGGGCTTACCATCTGGCCCCAGTGCTGCAATGATACCGCGAGACCCACGCTCACCGGCTCCAGATTTATCAGCAATAAACCAGCCAGCCGGAAGGGCCGAGCGCAGAAGTGGTCCTGCAACTTTATCCGCCTCCATCCAGTCTATTAATTGTTGCCGGGAAGCTAGAGTAAGTAGTTCGCCAGTTAATAGTTTGCGCAACGTTGTTGCCATTGCTACAGGCATCGTGGTGTCACGCTCGTCGTTTGGTATGGCTTCATTCAGCTCCGGTTCCCAACGATCAAGGCGAGTTACATGATCCCCCATGTTGTGCAAAAAAGCGGTTAGCTCCTTCGGTCCTCCGATCGTTGTCAGAAGTAAGTTGGCCGCAGTGTTATCACTCATGGTTATGGCAGCACTGCATAATTCTCCTACTGTCATGCCATCCGTAAGATGCTTTTCTGTGACTGGTGAGTACTCAACCAAGTCATTCTGAGAATAGTGTATGCGGCGACCGAGTTGCTCTTGCCCGGCGTCAATACGGGATAATACCGCGCCACATAGCAGAACTTTAAAAGTGCTCATCATTGGAAAACGTTCTTCGGGGCGAAAACTCTCAAGGATCTTACCGCTGTTGAGATCCAGTTCGATGTAACCCACTCGTGCACCCAACTGATCTTCAGCATCTTTTACTTTCACCAGCGTTTCTGGGTGAGCAAAAACAGGAAGGCAAAATGCCGCAAAAAAGGGAATAAGGGCGACACGGAAATGTTGAATACTCATACTCTTCCTTTTTCAATATTATTGAAGCATTTATCAGGGTTATTGTCTCATGAGCGGATACATA
"""
    )

    allenzymesfield = MultiCheckboxField("AllEnzymes", choices=allenzymes)
    commonlyfield = MultiCheckboxField("CommOnly", choices=commonly)
    sixcuttersfield = MultiCheckboxField("Sixcutters", choices=sixcutters)
    morethansixcuttersfield = MultiCheckboxField(">Sixcutters", choices=morethansixcutters)
    lessthansixcuttersfield = MultiCheckboxField("<Sixcutters", choices=lessthansixcutters)

    sequence = TextAreaField("sequence", default=default)
    given_enzymes = TextAreaField("enzymes")

    send = SubmitField("submit")


class TmForm(FlaskForm):
    """docstring."""

    nn_table = SelectField("nn_table", choices=nn_tableoptions, default=default["nn_table"])
    saltcorr = SelectField("saltcorr", choices=saltoptions, default=default["saltcorr"])
    Na = DecimalField("Na", default=default["Na"])
    Mg = DecimalField("Mg", default=default["Mg"])
    dnac1 = DecimalField("dnac1", default=default["dnac1"])
    dnac2 = DecimalField("dnac2", default=default["dnac2"])
    K = DecimalField("K", default=default["K"])
    Tris = DecimalField("Tris", default=default["Tris"])
    dNTPs = DecimalField("dNTPs", default=default["dNTPs"])

    primer_text = TextAreaField(
        "primer_text",
        default=">MyPrimer\nATGGCAGTTGAGAAGA\n\n>another\nagtgtgctagtagtacgtcgta",
    )
    send = SubmitField("submit")
    clear = SubmitField("clear")


class CrisprForm(FlaskForm):
    """docstring."""

    system = SelectField("system", choices=crispr_systems)
    sgrna = TextAreaField(
        "sgRNA construct",
        default=">sgRNA_construct\nGTTACTTTACCCGACGTCCCgttttagagctagaaatagcaagttaaaataagg",
    )
    target = TextAreaField(
        "Target DNA",
        default=">Target_DNA\nGTTACTTTACCCGACGTCCCaGG",
    )
    send = SubmitField("submit")
    clear = SubmitField("clear")


class PrimerDesignForm(FlaskForm):
    default = dedent(
        """\
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
    )
    sequences = TextAreaField("sequences", default=default)

    send = SubmitField("submit")
    clear = SubmitField("clear")


class MatchingPrimerForm(FlaskForm):
    default = dedent(
        """\
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
    )
    sequences = TextAreaField("sequences", default=default)

    send = SubmitField("submit")
    clear = SubmitField("clear")


class AssemblyDesignForm(FlaskForm):
    """docstring."""

    topology = RadioField(
        "Topology",
        choices=[("linear", "linear"), ("circular", "circular")],
        default="linear",
    )
    tails = IntegerField("Tails", default=30)
    maxlink = IntegerField("maxlink", default=30)
    overlap = IntegerField("overlap", default=30)
    separator = StringField("separator", default="<======>")

    default = dedent(
        f"""\

        >f50 21-mer
        CTTTCGAGAATACCAGAAAAA

        >r50 21-mer
        GTACAAGAATTGCACAATTCA

        >a
        CTTTCGAGAATACCAGAAAAAATGATTACTGAATTGTGCAATTCTTGTAC

        {separator.kwargs.get("default")}

        >b
        GATTTCCTTTTGGATACCTGAAACAAAGCCCATCGTGGTCCTTAGACTT

        {separator.kwargs.get("default")}

        >f48 22-mer
        CTTCATAAATAGATTGCCATAC

        >r48 22-mer
        ACTTTTTACTGATTCATAAGCT

        >c
        CTTCATAAATAGATTGCCATACATAGAGCTTATGAATCAGTAAAAAGT


    """
    )

    sequences = TextAreaField("sequences", default=default)
    send = SubmitField("submit")
    clear = SubmitField("clear")


class AssemblyForm(FlaskForm):
    """docstring."""

    topology = RadioField(
        "Topology",
        choices=[("linear", "linear"), ("circular", "circular")],
        default="linear",
    )
    limit = IntegerField("limit", default=recombinationlimit)

    default = dedent(
        """\
    >a
    atgaggcgcttttaaatatggcgaaAtaagtgatttaacgctttgaatatg

    >b
    taagtgatttaacgctttgaatatgCCactatatacttaaatttgatttcgt

    >c
    actatatacttaaatttgatttcgtGGGatgaggcgcttttaaatatggcgaa
    """
    )

    sequences = TextAreaField("sequences", default=default)
    send = SubmitField("submit")
    clear = SubmitField("clear")


class SeguidForm(FlaskForm):
    """docstring."""
    sequence = TextAreaField("sequence", default="")
    calc = SubmitField("calc")
    reverse = SubmitField("reverse")
    complement = SubmitField("complement")
    reverse_complement = SubmitField("reverse_complement")
    send = SubmitField("submit")
    clear = SubmitField("clear")

    lsseguid = StringField("lsseguid")
    csseguid = StringField("csseguid")
    ldseguid = StringField("ldseguid")
    cdseguid = StringField("cdseguid")
    length = StringField("length")
    charset = StringField("charset"),


nn_tables = {"1": _mt.DNA_NN1, "2": _mt.DNA_NN2, "3": _mt.DNA_NN3, "4": _mt.DNA_NN4}

app = Flask(__name__)

app.config.update(dict(SECRET_KEY="powerful_secretkey", WTF_CSRF_SECRET_KEY="a_csrf_secret_key"))

separator = "-" * 80


@app.route("/", methods=["GET", "POST"])
def index():
    """docstring."""
    return render_template("index.html", version=version, bpversion=bpversion)


@app.route("/docs", methods=["GET", "POST"])
def docs():
    """docstring."""
    return render_template("docs.html")


@app.route("/gateway", methods=["GET", "POST"])
def gateway():
    """docstring."""
    return render_template("gateway.html")


@app.route("/seguid", methods=["GET", "POST"])
def seguid():
    """docstring."""
    user_data = request.form or MultiDict()
    form = SeguidForm(formdata=MultiDict(user_data))
    s = user_data.get("sequence")
    if not s:
        return render_template("seguid.html", form=form)
    sequence = seqfilter(s) or ""
    if 'calc' in request.form:
        pass
    elif 'reverse' in request.form:
        sequence = sequence[::-1]
    elif 'complement' in request.form:
        sequence = rc(sequence)[::-1]
    elif 'reverse_complement' in request.form:
        sequence = rc(sequence)
    elif 'clear' in request.form:
        return render_template("seguid.html")
    print(request.form)

    if sequence:
        slseg = lsseguid(sequence)
        scseg = csseguid(sequence)
        dlseg = ldseguid(sequence)
        dcseg = cdseguid(sequence)
    else:
        slseg = ""
        scseg = ""
        dlseg = ""
        dcseg = ""

    form.csseguid = scseg,
    form.ldseguid = dlseg,
    form.cdseguid = dcseg,
    form.length = len(sequence) or "",
    form.charset = " ".join(sorted(set(sequence.upper()))),
    #form.sequence = sequence
    return render_template("seguid.html", form=form)


@app.route("/fusionpcr", methods=["GET", "POST"])
def fusionpcr():
    """docstring."""
    user_data = request.form or MultiDict()
    form = FusionPCRForm(formdata=MultiDict(user_data))
    s = user_data.get("sequences")
    if not s:
        return render_template("fusionpcr.html", form=form)

    from pydna.fusionpcr import fuse_by_pcr, list_parts

    fp, rp, *frags = parse(s)

    limit = int(user_data.get("limit")) or pcrlimit
    results = fuse_by_pcr(frags, limit=limit)

    result_text = ""

    for result in results:
        result_text += list_parts(result)

        ann = Anneal((fp, rp), result, limit=limit)

        for amplicon in ann.products:

            result_text += f"""\
Forward: {amplicon.forward_primer.name} Reverse: {amplicon.reverse_primer.name}

{amplicon.figure()}

>{amplicon.name}
{amplicon.seq}


"""

    return render_template("result.html", result=result_text)


@app.route("/crispr", methods=["GET", "POST"])
def crispr():
    """docstring."""
    user_data = request.form or MultiDict()
    form = CrisprForm(formdata=MultiDict(user_data))
    system = user_data.get("system")
    sgrna = user_data.get("sgrna")
    target = user_data.get("target")
    if not sgrna or not target:
        return render_template("crispr.html", form=form)
    sgrna_dsr = read(sgrna)
    target_dsr = read(target)

    from pydna.crispr import cas9, protospacer

    result_text = "CRISPR simulation\n\n"

    guidelist = []
    for ps in protospacer(sgrna_dsr):
        gd = cas9(ps)
        result_text += f"{str(gd)}\n\n"
        guidelist.append(gd)

    msg = ""
    for f in target_dsr.cut(guidelist):
        msg += f">CRISPr_fragment_{len(f)}bp\n{f.seq}\n\n"
    result_text += msg or "No CRISPr digestion."

    return render_template("result.html", result=result_text)


@app.route("/digest", methods=["GET", "POST"])
def digest():
    """docstring."""
    user_data = request.form or MultiDict()

    form = DigestForm(formdata=MultiDict(user_data))

    s = user_data.get("sequence")

    result_text = "digestion result "

    enzymes = RestrictionBatch(
        list(
            chain.from_iterable(
                user_data.getlist(x)
                for x in (
                    "allenzymesfield",
                    "commonlyfield",
                    "morethansixcuttersfield",
                    "sixcuttersfield",
                    "lessthansixcuttersfield",
                )
            )
        )
    )

    custom_enzymes = RestrictionBatch(
        [e for e in AllEnzymes if str(e).lower() in str(user_data.get("given_enzymes")).lower()]
    )

    enzymes.update(custom_enzymes)

    if not s or not enzymes:
        return render_template("digest.html", form=form)

    sequences = parse(s)

    *inserts, backbone = sequences

    if inserts:
        bb_once_cutters = backbone.once_cutters(enzymes)

        i_no_cutters = RestrictionBatch.intersection(*[i.no_cutters(enzymes) for i in inserts])
        i_once_cutters = RestrictionBatch.intersection(*[i.once_cutters(enzymes) for i in inserts])
        i_twice_cutters = RestrictionBatch.intersection(*[i.twice_cutters(enzymes) for i in inserts])

        # print(bb_once_cutters, i_no_cutters)
        # print([i.no_cutters(enzymes) for i in inserts])
        # print(RestrictionBatch().intersection(*[i.no_cutters(enzymes) for i in inserts]))

        result_text = f"""\
Restriction analysis of {len(inserts)+1} sequences
--------------------------------------------------
The following enzymes cut once in the last sequence and absent from all preceding sequences(s):
{" ".join(str(e) for e in sorted(bb_once_cutters&i_no_cutters)) or '-'}

The following enzymes cut once in the last sequence and twice in all preceding sequences(s):
{" ".join(str(e) for e in sorted(bb_once_cutters&i_twice_cutters)) or '-'}

The following enzymes cut once in each sequence:
{" ".join(str(e) for e in sorted(bb_once_cutters&i_once_cutters)) or '-'}

All enzymes used in the analysis:
{" ".join(str(e) for e in sorted(enzymes))}
"""
    else:
        frags = backbone.cut(enzymes)
        for i, f in enumerate(frags):
            f.id = f"fragment#{i+1}"
            f.description = f"{len(f)} bp"

        result_text = f"""\
Restriction analysis of a single sequence
-----------------------------------------

{(chr(10)*2).join(f.format('fasta') for f in frags) or '-'}


The following enzymes do *not* cut:
{" ".join(str(e) for e in sorted(backbone.no_cutters(enzymes))) or '-'}

The following enzymes cut once:
{" ".join(str(e) for e in sorted(backbone.once_cutters(enzymes))) or '-'}

The following enzymes cut twice:
{" ".join(str(e) for e in sorted(backbone.twice_cutters(enzymes))) or '-'}

The following enzymes cut three times:
{" ".join(str(e) for e in sorted(backbone.n_cutters(3, enzymes))) or '-'}

The following enzymes cut one or more times:
{" ".join(str(e) for e in sorted(backbone.cutters(enzymes))) or '-'}

All enzymes used in the analysis:
{" ".join(str(e) for e in sorted(enzymes))}

"""

    return render_template("result.html", result=result_text)

@app.route("/restrictionligation", methods=["GET", "POST"])
def restrictionligation():
    result_text = "hejej"
    return render_template("result.html", result=result_text)

@app.route("/translation", methods=["GET", "POST"])
def translation():

    user_data = request.form or MultiDict()
    form = TranslationForm(formdata=MultiDict(user_data))
    s = user_data.get("sequence")
    if not s:
        return render_template("translation.html", form=form)

    from pydna.readers import read

    s = read(s)
    result_text = "\n"
    for orf in s.orfs():
        prt = orf.translate()
        prt.id = f"{len(prt)}aa"
        result_text += prt.format("fasta-2line") + "\n\n"

    s.orfs_to_features()

    s.features = s.orfs_to_features() + s.features

    result_text += s.format("gb")

    return render_template("result.html", result=result_text)


@app.route("/repair", methods=["GET", "POST"])
def repair():
    """docstring."""
    user_data = request.form or MultiDict()

    form = RepairForm(formdata=MultiDict(user_data))

    s = user_data.get("sequence")

    if not s:
        return render_template("repair.html", form=form)

    gbtext, json = gbtext_clean(s)

    result_text = read(gbtext).format()

    return render_template("result.html", result=result_text)


@app.route("/toggle", methods=["GET", "POST"])
def toggle():
    """docstring."""
    user_data = request.form or MultiDict()

    form = ToggleForm(formdata=MultiDict(user_data))

    s = user_data.get("sequence")

    if not s:
        return render_template("toggle.html", form=form)

    pattern = r"(?:>.+\n^(?:^[^>]+?)(?=\n\n|>|LOCUS|ID))|(?:(?:LOCUS|ID)(?:(?:.|\n)+?)^//)"
    result_text = ""
    rawseqs = re.findall(pattern, dedent(s + "\n\n"), flags=re.MULTILINE)
    if rawseqs:
        for rawseq in rawseqs:
            if rawseq.startswith(">"):
                outformat = "gb"
            else:
                outformat = "fasta"
            seq = read(rawseq)
            result_text += seq.format(outformat) + "\n\n"
    else:
        outformat = "fasta"
        chunk = "".join(c for c in s if c in "GATCRYWSMKHBVDNgatcrywsmkhbvdn")
        result_text = f">seq_{len(chunk)}bp\n{chunk}"

    return render_template("result.html", result=result_text)


@app.route("/totab", methods=["GET", "POST"])
def totab():
    """docstring."""
    user_data = request.form or MultiDict()

    form = ToTABForm(formdata=MultiDict(user_data))

    s = user_data.get("sequences")

    if not s:
        return render_template("totab.html", form=form)

    result_text = ""

    new_sequences = parse(s)

    for seq in new_sequences:
        result_text += seq.format("tab") + "\n"

    return render_template("result.html", result=result_text)


@app.route("/enum", methods=["GET", "POST"])
def enum():
    """docstring."""
    user_data = request.form or MultiDict()

    form = EnumForm(formdata=MultiDict(user_data))

    s = user_data.get("sequences")

    if not s:
        return render_template("enum.html", form=form)

    result_text = ""

    try:
        startnumber = int(user_data.get("startnumber"))
    except ValueError:
        startnumber = 1

    pl = PrimerList([read_primer(f">{startnumber-1}_fakeprimer\na")])

    result_text += pl.assign_numbers(parse_primers(s))

    return render_template("result.html", result=result_text)


@app.route("/pcr", methods=["GET", "POST"])
def pcr():
    """docstring."""
    user_data = request.form or MultiDict()

    form = WebPCRForm(formdata=MultiDict(user_data))

    s = user_data.get("sequences")

    if not s:
        return render_template("pcr.html", form=form)

    sequences = parse(s)

    template = sequences.pop()

    primer_sequences = sequences

    homology_limit = int(user_data.get("limit")) or pcrlimit

    cutoff_detailed_figure = 5

    ann = Anneal(primer_sequences, template, limit=homology_limit)

    products = ann.products

    result_text = ""

    if len(products) == 0:
        result_text += ann.report().strip()

    elif 1 <= len(products) <= cutoff_detailed_figure:
        result_text += f"{ann.report()}\n---\n"

        for amplicon in products:
            result_text += dedent(
                f"""\
Forward: {amplicon.forward_primer.name} Reverse: {amplicon.reverse_primer.name}

{amplicon.figure()}

Taq DNA pol
{amplicon.program()}
DNA pol w DNA binding domain (PHUSION)
{amplicon.dbd_program()}

>{amplicon.name}
{amplicon.seq}
---
"""
            )

    else:
        result_text += "\n" + ann.template.format("gb")

    return render_template("result.html", result=result_text)


@app.route("/primerdesign", methods=["GET", "POST"])
def primerdesign():
    """docstring."""

    user_data = request.form or MultiDict()

    form = PrimerDesignForm(formdata=MultiDict(user_data))

    if request.method == "GET" or not user_data.get("sequences"):
        return render_template("primerdesign.html", form=form)

    templates = parse(user_data["sequences"])

    amplicon = None
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
---
"""

    return render_template("result.html", form=form, result=result_text)


@app.route("/matchingprimer", methods=["GET", "POST"])
def matchingprimer():
    """docstring."""

    user_data = request.form or MultiDict()

    form = MatchingPrimerForm(formdata=MultiDict(user_data))

    if request.method == "GET" or not user_data.get("sequences"):
        return render_template("matchingprimer.html", form=form, result="")

    templates = parse(user_data["sequences"])

    amplicon = None

    result_text = ""

    for p, template in zip(templates[::2], templates[1::2]):
        try:
            amplicon = primer_design(template, fp=p, limit=pcrlimit)  # TODO Tm_NN
        except ValueError:  # ValueError
            pass
        try:
            amplicon = primer_design(template, rp=p, limit=pcrlimit)  # TODO Tm_NN
        except ValueError:  # ValueError
            pass

        if not amplicon:
            result_text = "Primer does not anneal."
        else:
            result_text += f"""\

>{amplicon.forward_primer.name} {len(amplicon.forward_primer)}-mer
{amplicon.forward_primer.seq}
>{amplicon.reverse_primer.name} {len(amplicon.reverse_primer)}-mer
{amplicon.reverse_primer.seq}
>{amplicon.template.name}
{amplicon.template.seq}

{amplicon.figure()}

>{amplicon.name}
{amplicon.seq}

---

"""

    return render_template("result.html", form=form, result=result_text)


@app.route("/asmdesign", methods=["GET", "POST"])
def asmdesign():
    """docstring."""

    user_data = request.form or MultiDict()

    form = AssemblyDesignForm(formdata=MultiDict(user_data))

    if request.method == "GET" or not user_data.get("sequences"):
        return render_template("asmdesign.html", form=form, result="")

    separator = user_data["separator"]
    items = user_data["sequences"].split(separator)
    sequences = []

    #     item = """
    # >f50 21-mer
    # CTTTCGAGAATACCAGAAAAA

    # >r50 21-mer
    # GTACAAGAATTGCACAATTCA

    # >a
    # CTTTCGAGAATACCAGAAAAAATGATTACTGAATTGTGCAATTCTTGTAC"""

    # item = """
    # >b
    # GATTTCCTTTTGGATACCTGAAACAAAGCCCATCGTGGTCCTTAGACTT

    # """

    # alg = circular_assembly_fragments
    # user_data = {"topology":"circular",
    #              "overlap":15,
    #              "maxlink":5}

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

    alg = {
        "linear": assembly_fragments,  # TODO Tm_NN
        "circular": circular_assembly_fragments,
    }[
        user_data["topology"]
    ]  # TODO Tm_NN

    fragments = alg(
        sequences,
        overlap=int(user_data["overlap"]),
        maxlink=int(user_data["maxlink"]),
    )

    result_items = []
    for item in fragments:
        if hasattr(item, "template"):
            result_items.append(
                (
                    f"""\
>{item.forward_primer.name} {len(item.forward_primer)}-mer
{item.forward_primer.seq}
>{item.reverse_primer.name} {len(item.reverse_primer)}-mer
{item.reverse_primer.seq}
>{item.template.name}
{item.template.seq}
"""
                )
            )
        else:
            result_items.append(item.format("primer"))

    result_text = f"\n{separator}\n".join(result_items)
    return render_template("result.html", form=form, result=result_text)


@app.route("/assembly", methods=["GET", "POST"])
def assembly():
    """docstring."""
    form = AssemblyForm()

    user_data = request.form or MultiDict()

    if request.method == "GET" or not user_data.get("sequences"):
        form.topology.data = user_data.get("topology", "linear")
        form.limit.data = user_data.get("limit", recombinationlimit)
        return render_template("assembly.html", form=form, result="")

    sequences = parse(user_data["sequences"])
    asm = Assembly(sequences, limit=int(user_data["limit"]))
    if user_data["topology"] == "circular":
        candidates = asm.assemble_circular()
    else:
        candidates = asm.assemble_linear()

    assembly_results = (
        "\n".join(
            f"""\
Figure:

{candidate.figure()}

Detailed figure:

{candidate.detailed_figure()}

Resulting sequence:

>{candidate.name} { {False:'linear',True:'circular'}[candidate.circular] }
{candidate.seq}
---"""
            for candidate in candidates
        )
        or "\n\n\n\n\n\nNo assembly result.\n\nTry a shorter homology limit.\n\n\n\n"
    )

    # return redirect(url_for('assembly'))
    return render_template("result.html", form=form, result=assembly_results)


@app.route("/tm", methods=["GET", "POST"])
def tm():
    """docstring."""

    user_data = request.form or MultiDict()

    form = TmForm(formdata=MultiDict(user_data))

    if request.method == "GET":
        return render_template("tm.html", form=form, result="")

    primers = parse(user_data["primer_text"])

    tm_results = f"Biopython v{default['Biopython_version']} "
    tm_results += f"{default['func']} Arguments("
    tm_results += ", ".join(f"{k}: {user_data[k]}" for k in default.keys() if k in user_data.keys())
    tm_results += ")\n\n"

    for primer in primers:
        tm = tm_default(
            primer.seq,
            check=True,
            strict=True,
            c_seq=None,
            shift=0,
            nn_table=nn_tables[user_data["nn_table"]],
            tmm_table=None,
            imm_table=None,
            de_table=None,
            dnac1=float(user_data["dnac1"]),
            dnac2=float(user_data["dnac2"]),
            selfcomp=False,
            Na=float(user_data["Na"]),
            K=float(user_data["K"]),
            Tris=float(user_data["Tris"]),
            Mg=float(user_data["Mg"]),
            dNTPs=float(user_data["dNTPs"]),
            saltcorr=int(user_data["saltcorr"]),
        )
        primer.description = f"tm={round(tm, 3)}"

    tm_results += "\n".join(p.format("primer") for p in primers)

    return render_template("result.html", form=form, result=tm_results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
