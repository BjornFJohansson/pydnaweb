### Markdown

content


https://docs.google.com/document/d/1JgmwWSL6axFw3Ed9aKurpC_qwo_PoILAxvpbUU5nviY/edit
https://biopython.org/docs/1.75/api/Bio.SeqUtils.MeltingTemp.html
https://github.com/BjornFJohansson/tm
https://www.youtube.com/watch?v=OblPqlOOgew
https://www.youtube.com/watch?v=NufigSvIfA4


<html>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8">
<title>WebPCR help</title>

<head>
<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>

WebPCR is a web service that can simulate PCR given primers and a template sequence.<br>
<br>
The input is a list of sequences in <a href="http://en.wikipedia.org/wiki/FASTA_format">FASTA</a>
or <a href="http://quma.cdb.riken.jp/help/gbHelp.html">Genbank</a> format.
Different formats within the list are accepted.<br>
<br>
The last sequence in the list is interpreted as the template sequence, and all preceding<br>
sequences are primer sequences<br>
<br>
in the example below, MyTemplate is the template and ForwardPrimer and ReversePrimer are primers.
<br>
<br>
>ForwardPrimer<br>
gctactacacacgtactgactg<br>
<br>
>ReversePrimer<br>
tgtggttactgactctatcttg<br>
<br>
>MyTemplate<br>
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca<br>
<br>
<br>
<br>
A report is generated as detailed below.<br>
<br>
A header lists positions of annealing primers and wheter primers anneal<br>
forward or reverse<br>

<pre>

==============
PCR simulation
==============

Template MyTemplate 48 nt linear:
Primer ForwardPrimer anneals at position 21
Primer ReversePrimer anneals reverse at position 27

</pre>

Then follows a report for each PCR product formed containing<br>
the PCR product sequence.<br>
In this case a 48bp product was formed.<br>
The code
in the FASTA header (Qv+...) is the
<a href="http://bioinformatics.anl.gov/seguid/">SEGUID</a> checksum for the sequence.
<br>


<pre>
PCR product from MyTemplate:

>48bp Qv+rBG66LfFo7uEEyOqOMH3z9pI
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca

</pre>
A figure describing how the primers anneal:
<pre>

5gctactacacacgtactgactg3
 |||||||||||||||||||||| tm 52.6 (dbd) 58.3
5gctactacacacgtactgactg...caagatagagtcagtaaccaca3
3cgatgatgtgtgcatgactgac...gttctatctcagtcattggtgt5
                          |||||||||||||||||||||| tm 49.1 (dbd) 57.7
                         3gttctatctcagtcattggtgt5
</pre>

And finally two PCR programs, one for Taq polymerase and one<br>
for proofreading polymerase with DNA binding domain.<br>

<pre>
suggested PCR programs

Taq (rate 30 nt/s)
Three-step|         30 cycles     |      |SantaLucia 1998
94.0°C    |94.0°C                 |      |SaltC 50mM
__________|_____          72.0°C  |72.0°C|
04min00s  |30s  \         ________|______|
          |      \ 46.0°C/ 0min 1s|10min |
          |       \_____/         |      |
          |         30s           |      |4-8°C

Pfu-Sso7d (rate 15s/kb)
Three-step|          30 cycles   |      |Breslauer1986,SantaLucia1998
98.0°C    |98.0°C                |      |SaltC 50mM
__________|_____          72.0°C |72.0°C|Primer1C   1µM
00min30s  |10s  \ 61.0°C ________|______|Primer2C   1µM
          |      \______/ 0min 0s|10min |
          |        10s           |      |4-8°C



</pre>

WebPCR should handle circular templates well. <br>
A circular template can be indicated by the
<a href="http://www.ncbi.nlm.nih.gov/nuccore/L09137">Genbank</a>
file in the LOCUS line<br>
or by supplying the keyword "circular" in the template fasta header<br>
like this:<br>
<br>
>MyTemplate circular<br>
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca<br>
<br>
<br>
WebPCR was developed by

<a href="https://sites.google.com/site/metabolicengineeringgroup/">Björn Johansson</a>

at

<a href="http://www.bio.uminho.pt/">Dept of Biology</a>
,

<a href="http://www.uminho.pt/">University of Minho</a>.

<br>
It is a python program running in the cloud on a free Google app engine so please<br>
do not abuse the service. WebPCR depends on the excellent
<a href="http://biopython.org/wiki/Biopython">biopython</a> package.

<br>

If you have further questions or comments

<a href="mailto:bjornjobb@gmail.com?subject=WebPCR">Send me an email</a>
<br>
    <br>
        <br>
</html>
