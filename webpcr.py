#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""docstring."""

# https://blog.pythonanywhere.com/121
# export FLASK_APP=webpcr.py&&export FLASK_ENV=development&&flask run

# https://pypi.org/project/Bootstrap-Flask

from textwrap import dedent
from flask import Flask, redirect, render_template, request, url_for

from forms import CustomForm

import pydna
from pydna.parsers import parse
from pydna.amplify import Anneal

from Bio.SeqUtils import MeltingTemp as _mt

nn_tables = {"1":_mt.DNA_NN1,
             "2":_mt.DNA_NN2, 
             "3":_mt.DNA_NN3,
             "4":_mt.DNA_NN4}

# saltcorrs = {"1":,
#              "2":, 
#              "3":,
#              "4":
#              "5":, 
#              "6":,
#              "7":}
    

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"))
app.config["DEBUG"] = True

results = []

separator = '-'*80

@app.route("/", methods=["GET", "POST"])
def index():
    """docstring."""
    print(url_for('tm'))
    """docstring."""
    return render_template("index.html")



@app.route("/tm", methods=["GET", "POST"])
def tm():
    """docstring."""
    form = CustomForm()
    if request.method == "GET":
        return render_template("tm.html",
                               form=form)
    
    #if request.method == 'POST' and form.validate():

    if 'clear' in request.form:
        return redirect(url_for('tm'))

    user_data = request.form
    
    primers = parse(user_data['primer_text'])
    
    comments = []
    for primer in primers:
        tm = _mt.Tm_NN( primer.seq,
                        check=True,
                        strict=True,
                        c_seq=None,
                        shift=0,
                        nn_table=nn_tables[user_data['table']],
                        tmm_table=None,
                        imm_table=None,
                        de_table=None,
                        dnac1=float(user_data['dnac1']), 
                        dnac2=float(user_data['dnac2']),
                        selfcomp=False,
                        Na=float(user_data['Na']),
                        K=float(user_data['K']),
                        Tris=float(user_data['Tris']), 
                        Mg=float(user_data['Mg']),  
                        dNTPs=float(user_data['dNTPs']),  
                        saltcorr=int(user_data['salt']))
        primer.description = f"tm={tm}"
        comments.append(primer.format("fasta"))
    return render_template("tm.html",
                           form=form,
                           comments=comments)


# ImmutableMultiDict(


# [('csrf_token', 'Ijk1ZTFhODRjMzkzNDJkMGMyNDM5YzRiNGY4NzBhZjgzYTFhMzViZTgi.YKjwww.a0Lm5QJTzvACnIlf6hgQuH48W90'),
#  ('csrf_token', 'Ijk1ZTFhODRjMzkzNDJkMGMyNDM5YzRiNGY4NzBhZjgzYTFhMzViZTgi.YKjwww.a0Lm5QJTzvACnIlf6hgQuH48W90'),
#  ('table', '4'), ('Na', '40'), ('salt', '7'), ('K', '0'), ('Mg', '1.5'), ('Tris', '75.0'),
#  ('dnac1', '250'), ('dNTPs', '0.8'), ('dnac2', '250'),
#  ('contents', '>MyPrimer\r\ngctactacacacgtactgactg\r\n                    '),
#  ('run', 'Calculate')])

    # table = user_data['table']
    # Na = user_data['Na']
    # salt = user_data['salt']
    # K = user_data['K']
    # Mg = user_data['Mg']
    # Tris = user_data['Tris']
    # dnac1 = user_data['dnac1']
    # dNTPs= user_data['dNTPs']
    # dnac2= user_data['dnac2']
    # contents = user_data['contents']
    # run = user_data['run']
    #form.process()
    #form.validate_on_submit()


# def tm_default(
#     seq,
#     check=True,
#     strict=True,
#     c_seq=None,
#     shift=0,
#     nn_table=_mt.DNA_NN4,  # DNA_NN4: values from SantaLucia & Hicks (2004)
#     tmm_table=None,
#     imm_table=None,
#     de_table=None,
#     dnac1=500 / 2,  # I assume 500 µM of each primer in the PCR mix
#     dnac2=500 / 2,  # This is what MELTING and Primer3Plus do
#     selfcomp=False,
#     Na=40,
#     K=0,
#     Tris=75.0,  # We use the 10X Taq Buffer with (NH4)2SO4 (above)
#     Mg=1.5,  # 1.5 mM Mg2+ is often seen in modern protocols
#     dNTPs=0.8,  # I assume 200 µM of each dNTP
#     saltcorr=7,  # Tm = 81.5 + 0.41(%GC) - 600/N + 16.6 x log[Na+]
#     func=_mt.Tm_NN,  # Used by Primer3Plus to calculate the product Tm.
# ):





@app.route("/pcr", methods=["GET", "POST"])
def pcr():
    """docstring."""

    if request.method == "GET":
        return render_template("pcr.html",
                               results=results,
                               version=pydna.__version__)

    if 'clear' in request.form:
        results.clear()
        return redirect(url_for('pcr'))

    user_data = request.form["contents"]

    sequences = parse(user_data)

    template = sequences.pop()
    primer_sequences = sequences

    homology_limit = 12
    cutoff_detailed_figure = 6
    cutoff_detailed_figure = 5

    ann = Anneal(primer_sequences,
                 template,
                 limit=homology_limit)

    number_of_products = len(ann.forward_primers) * len(ann.reverse_primers)

    if number_of_products == 0:
        result_text = ann.report().strip()
    elif 1 <= number_of_products <= cutoff_detailed_figure:
        result_text = (f'pydna {pydna.__version__}\n'
                       f'{ann}\n'
                       f'Number of products formed: {number_of_products}\n'
                       f'{separator}')
        for amplicon in ann.products:
            result_text += dedent(f'''
            >{amplicon.forward_primer.name}
            {amplicon.forward_primer.seq}
            >{amplicon.reverse_primer.name}
            {amplicon.reverse_primer.seq}
            >{ann.template.name}
            {ann.template.seq}
            ----
            {{}}
            ----
            >{amplicon.name}
            {amplicon.seq}
            ----
            {{}}''')
            result_text = result_text.format(amplicon.figure(),
                                             amplicon.program())

    results.append(result_text)

    return redirect(url_for('pcr'))
