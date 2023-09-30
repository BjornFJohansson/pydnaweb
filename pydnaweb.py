#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""docstring."""

import datetime

from textwrap import dedent

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from werkzeug.datastructures import MultiDict

from wtforms.fields import SelectField
from wtforms.fields import DecimalField
from wtforms.fields import TextAreaField
from wtforms.fields import SubmitField
from wtforms.fields import RadioField
from wtforms.fields import IntegerField

from Bio.SeqUtils import MeltingTemp as _mt

from pydna import __version__ as version
from Bio import __version__ as bpversion
from pydna.parsers import parse
from pydna.amplify import Anneal
from pydna.design import primer_design
from pydna.design import assembly_fragments
from pydna.design import circular_assembly_fragments
from pydna.assembly import Assembly
from pydna.tm import tm_default

# from pydna.parsers import parse_assembly_xml

from flask_wtf import FlaskForm

nn_tableoptions = [
    (1, "DNA_NN1 - Breslauer et al. (1986), " "Proc Natl Acad Sci USA 83: 3746-3750"),
    (2, "DNA_NN2 - Sugimoto et al. (1996)," " Nuc Acids Res 24 : 4501-4505"),
    (3, "DNA_NN3 - Allawi and SantaLucia (1997)," " Biochemistry 36: 10581-10594"),
    (
        4,
        "DNA_NN4 - SantaLucia & Hicks (2004),"
        " Annu. Rev. Biophys. Biomol. Struct 33: 415-440",
    ),
]


saltoptions = [
    (1, "1. 16.6 x log[Na+] (Schildkraut & Lifson" " (1965), Biopolymers 3: 195-208)"),
    (
        2,
        "2. 16.6 x log([Na+]/(1.0 + 0.7*[Na+])) (Wetmur"
        " (1991), Crit Rev Biochem Mol Biol 126: 227-259)",
    ),
    (3, "3. 12.5 x log(Na+] (SantaLucia et al. (1996)," " Biochemistry 35: 3555-3562"),
    (
        4,
        "4. 11.7 x log[Na+] (SantaLucia (1998),"
        " Proc Natl Acad Sci USA 95: 1460-1465",
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


class WebPCRForm(FlaskForm):
    """docstring."""

    default = dedent(
        """\
    >1_5CYC1clone
    GATCGGCCGGATCCAAATGACTGAATTCAAGGCCG

    >2_3CYC1clon
    CGATGTCGACTTAGATCTCACAGGCTTTTTTCAAG

    >CYC1 YJR048W S. cerevisiae Cytochrome c, isoform 1
    atgactgaattcaaggccggttctgctaagaaaggtgctacacttttcaagactagatgtctacaatgccacaccgtggaaaagggtggcccacataaggttggtccaaacttgcatggtatctttggcagacactctggtcaagctgaagggtattcgtacacagatgccaatatcaagaaaaacgtgttgtgggacgaaaataacatgtcagagtacttgactaacccaaagaaatatattcctggtaccaagatggcctttggtgggttgaagaaggaaaaagacagaaacgacttaattacctacttgaaaaaagcctgtgagtaa
    """
    )

    sequences = TextAreaField("primer_text", default=default)

    limit = IntegerField("limit", default=16)

    send = SubmitField("calculate")


class TmForm(FlaskForm):
    """docstring."""

    table = SelectField("nn_table", choices=nn_tableoptions, default=4)
    salt = SelectField("saltcorr", choices=saltoptions, default=7)
    Na = DecimalField("Na", default=40)
    Mg = DecimalField("Mg", default=1.5)
    dnac1 = DecimalField("dnac1", default=250)
    dnac2 = DecimalField("dnac2", default=250)

    K = DecimalField("K", default=0)
    Tris = DecimalField("Tris", default=75.0)
    dNTPs = DecimalField("dNTPs", default=0.8)

    primer_text = TextAreaField("primer_text", default=">MyPrimer\nATGGCAGTTGAGAAGA")
    send = SubmitField("calculate")
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
    """
    )
    sequences = TextAreaField("sequences", default=default)

    send = SubmitField("calculate")
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

    send = SubmitField("calculate")
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

    default = dedent(
        """\
    <assembly>
      <amplicon>
         >f50 14-mer
         CCCGTACAAAGGGA
         >r50 12-mer
         CTGATGCCGCGC
         >a
         CCCGTACAAAGGGAACATCCACACTTTGGTGAATCGAAGCGCGGCATCAG
      </amplicon>
      <fragment>
         >b
         GATTTCCTTTTGGATACCTGAAACAAAGCCCATCGTGGTCCTTAGACTT
      </fragment>
      <amplicon>
         >f48 13-mer
         TCCCTACACCGAC
         >r48 16-mer
         ATGAAGCTCGTCACAT
         >c
         TCCCTACACCGACGTACGATGCAACTGTGTGGATGTGACGAGCTTCAT
      </amplicon>
    </assembly>
    """
    )

    xml = TextAreaField("xml", default=default)
    send = SubmitField("calculate")
    clear = SubmitField("clear")


class AssemblyForm(FlaskForm):
    """docstring."""

    topology = RadioField(
        "Topology",
        choices=[("linear", "linear"), ("circular", "circular")],
        default="linear",
    )
    limit = IntegerField("limit", default=30)

    default = dedent(
        """\
    >a
    acgatgctatactgCCCCCtgtgctgtgctcta

    >b
    tgtgctgtgctctaTTTTTtattctggctgtatc

    >c
    tattctggctgtatcGGGGGtacgatgctatactg
    """
    )

    sequences = TextAreaField("sequences", default=default)
    send = SubmitField("calculate")
    clear = SubmitField("clear")


nn_tables = {"1": _mt.DNA_NN1, "2": _mt.DNA_NN2, "3": _mt.DNA_NN3, "4": _mt.DNA_NN4}

app = Flask(__name__)

app.config.update(
    dict(SECRET_KEY="powerful_secretkey", WTF_CSRF_SECRET_KEY="a_csrf_secret_key")
)

separator = "-" * 80


@app.route("/", methods=["GET", "POST"])
def index():
    """docstring."""
    return render_template("index.html", version=version, bpversion=bpversion)


@app.route("/tm", methods=["GET", "POST"])
def tm():
    """docstring."""
    # if 'clear' in request.form:
    #     tm_results.clear()
    #     return redirect(url_for('tm'))

    user_data = request.form or {}

    form = TmForm(formdata=MultiDict(user_data))

    if request.method == "GET":
        return render_template("tm.html", form=form, result="")

    primers = parse(user_data["primer_text"])

    for primer in primers:
        tm = tm_default(
            primer.seq,
            check=True,
            strict=True,
            c_seq=None,
            shift=0,
            nn_table=nn_tables[user_data["table"]],
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
            saltcorr=int(user_data["salt"]),
        )
        primer.description = f"tm={round(tm, 3)}"
        tm_results = primer.format("fasta")
    # return redirect(url_for('tm'))
    return render_template("tm.html", form=form, result=tm_results)


@app.route("/pcr", methods=["GET", "POST"])
def pcr():
    """docstring."""

    user_data = request.form or {}

    form = WebPCRForm(formdata=MultiDict(user_data))

    s = user_data.get("sequences")

    if not s:
        return render_template("pcr.html", form=form, result="")

    sequences = parse(s)

    template = sequences.pop()

    primer_sequences = sequences

    homology_limit = 12
    cutoff_detailed_figure = 6
    cutoff_detailed_figure = 5

    ann = Anneal(primer_sequences, template, limit=homology_limit)

    products = ann.products

    result_text = ""

    if len(products) == 0:
        result_text += ann.report().strip()

    elif 1 <= len(products) <= cutoff_detailed_figure:
        result_text += f"{ann.report()}\n" f"{separator}"
        for amplicon in products:
            result_text += dedent(
                f"""

            {{}}



            >{amplicon.name}
            {amplicon.seq}



            Taq DNA polymerase
            {{}}

            Pfu-Sso7d DNA polymerase
            {{}}
            """
            )
    result_text = result_text.format(
        amplicon.figure(), amplicon.program(), amplicon.dbd_program()
    )

    # import html
    # result_text = html.escape(result_text).replace('\n', '<br />')

    return render_template("pcr.html", form=form, result=result_text)


@app.route("/primerdesign", methods=["GET", "POST"])
def primerdesign():
    """docstring."""
    # if 'clear' in request.form:
    #     primer_design_results.clear()
    #     return redirect(url_for('primerdesign'))

    user_data = request.form or {}

    form = PrimerDesignForm(formdata=MultiDict(user_data))

    if request.method == "GET":
        return render_template("primerdesign.html", form=form, result="")

    templates = parse(user_data["sequences"])

    homology_limit = 12

    amplicon = None

    for template in templates:
        amplicon = primer_design(template, limit=homology_limit)

        if amplicon:
            result_text = dedent(
                f"""
            >{amplicon.forward_primer.name} {len(amplicon.forward_primer)}-mer
            {amplicon.forward_primer.seq}
            >{amplicon.reverse_primer.name} {len(amplicon.reverse_primer)}-mer
            {amplicon.reverse_primer.seq}
            >{amplicon.template.name}
            {amplicon.template.seq}

            """
            )
            result_text = result_text.format(
                amplicon.figure(), amplicon.program(), amplicon.dbd_program()
            )

    return render_template("primerdesign.html", form=form, result=result_text)


@app.route("/matchingprimer", methods=["GET", "POST"])
def matchingprimer():
    """docstring."""
    # if 'clear' in request.form:
    #     matching_primer_results.clear()
    #     return redirect(url_for('matchingprimer'))

    user_data = request.form or {}

    form = MatchingPrimerForm(formdata=MultiDict(user_data))

    if request.method == "GET":
        return render_template("matchingprimer.html", form=form, result="")

    templates = parse(user_data["sequences"])

    homology_limit = 12

    amplicon = None

    for p, template in zip(templates[::2], templates[1::2]):
        try:
            amplicon = primer_design(template, fp=p, limit=homology_limit)
        except IndexError:  # ValueError
            pass
        try:
            amplicon = primer_design(template, rp=p, limit=homology_limit)
        except IndexError:  # ValueError
            pass

        if not amplicon:
            result_text = "Primer does not anneal."
        else:
            result_text = dedent(
                f"""

            >{amplicon.forward_primer.name} {len(amplicon.forward_primer)}-mer
            {amplicon.forward_primer.seq}
            >{amplicon.reverse_primer.name} {len(amplicon.reverse_primer)}-mer
            {amplicon.reverse_primer.seq}
            >{amplicon.template.name}
            {amplicon.template.seq}

            """
            )

    return render_template("matchingprimer.html", form=form, result=result_text)


@app.route("/asmdesign", methods=["GET", "POST"])
def asmdesign():
    """docstring."""
    # if 'clear' in request.form:
    #     asmdesign_results.clear()
    #     return redirect(url_for('asmdesign'))

    user_data = request.form or {}

    form = AssemblyDesignForm(formdata=MultiDict(user_data))

    if request.method == "GET":
        return render_template("asmdesign.html", form=form, result="")

    sequences = parse_assembly_xml(user_data["xml"])

    if user_data["topology"] == "linear":
        fragments = assembly_fragments(
            sequences,
            overlap=int(user_data["overlap"]),
            maxlink=int(user_data["maxlink"]),
        )
    else:
        fragments = circular_assembly_fragments(
            sequences,
            overlap=int(user_data["overlap"]),
            maxlink=int(user_data["maxlink"]),
        )

    result_text = "\n".join(item.format("fasta") for item in fragments)

    return render_template("asmdesign.html", form=form, result=result_text)


@app.route("/assembly", methods=["GET", "POST"])
def assembly():
    """docstring."""

    form = AssemblyForm()

    user_data = request.form or {}

    if request.method == "GET":
        form.topology.data = user_data.get("topology", "linear")
        form.limit.data = user_data.get("limit", 30)
        return render_template("assembly.html", form=form, result="")

    sequences = parse(user_data["sequences"])
    asm = Assembly(sequences, limit=int(user_data["limit"]))
    if user_data["topology"] == "circular":
        candidates = asm.assemble_circular()
    else:
        candidates = asm.assemble_linear()

    assembly_results = "\n".join(
        f"{candidate.figure()}\n\n" f"{candidate.format('fasta')}"
        for candidate in candidates
    )
    print(assembly_results)
    # return redirect(url_for('assembly'))
    return render_template("assembly.html", form=form, result=assembly_results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
