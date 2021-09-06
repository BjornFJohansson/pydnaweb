from flask_wtf import FlaskForm
from wtforms.fields import SelectField, DecimalField, TextAreaField, SubmitField

nn_tableoptions = [(1, "DNA_NN1 - Breslauer et al. (1986), Proc Natl Acad Sci USA 83: 3746-3750"),
                   (2, "DNA_NN2 - Sugimoto et al. (1996), Nuc Acids Res 24 : 4501-4505"),
                   (3, "DNA_NN3 - Allawi and SantaLucia (1997), Biochemistry 36: 10581-10594"),
                   (4, "DNA_NN4 - SantaLucia & Hicks (2004), Annu. Rev. Biophys. Biomol. Struct 33: 415-440"),]


saltoptions = [(1, "16.6 x log[Na+] (Schildkraut & Lifson (1965), Biopolymers 3: 195-208)"),
               (2, "16.6 x log([Na+]/(1.0 + 0.7*[Na+])) (Wetmur (1991), Crit Rev Biochem Mol Biol 126: 227-259)"),
               (3, "12.5 x log(Na+] (SantaLucia et al. (1996), Biochemistry 35: 3555-3562"),
               (4, "11.7 x log[Na+] (SantaLucia (1998), Proc Natl Acad Sci USA 95: 1460-1465"),
               (5, "Correction for deltaS: 0.368 x (N-1) x ln[Na+] (SantaLucia (1998), Proc Natl Acad Sci USA 95: 1460-1465)"),
               (6, "(4.29(%GC)-3.95)x1e-5 x ln[Na+] + 9.40e-6 x ln[Na+]^2 (Owczarzy et al. (2004), Biochemistry 43: 3537-3554)"),
               (7, "Complex formula with decision tree and 7 empirical constants.")]


class CustomForm(FlaskForm):
    """docstring."""
    table = SelectField('nn_table',
                       choices=nn_tableoptions,
                       default=4)
    salt = SelectField('saltcorr',
                       choices=saltoptions,
                       default=7)
    Na = DecimalField("Na", default = 40)
    Mg = DecimalField("Mg", default = 1.5)
    dnac1 = DecimalField("dnac1", default = 250)
    dnac2 = DecimalField("dnac2", default = 250)

    K = DecimalField("K", default = 0)
    Tris = DecimalField("Tris", default = 75.0)
    dNTPs = DecimalField("dNTPs", default = 0.8)

    primer_text = TextAreaField('primer_text', 
                                default = ">MyPrimer\ngctactacacacgtactgactg")
    send = SubmitField('send')
    clear = SubmitField('clear')
    home = SubmitField('clear')
