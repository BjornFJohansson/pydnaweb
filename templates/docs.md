Pydnaweb and Pydna development is led by Björn Johansson at the Department of Biology,
University of Minho. If you have question not answered below, ask in the [Google group](https://groups.google.com/g/pydna)
or create an issue on [GitHub](https://github.com/BjornFJohansson/pydnaweb/issues).

### WebPCR simulator

WebPCR is a web service that can simulate PCR given primers and a template sequence.
The WebPCR window accepts a list of sequences in [FASTA or Genbank](https://github.com/MetabolicEngineeringGroupCBMA/MetabolicEngineeringGroupCBMA.github.io/wiki/sequence_formats) format (or a mixture of both formats).

The **last** of the sequences in this list is assumed to be the **template** sequence while all preceding ones are assumed to be PCR primers.

The simulator will return a text based report describing the PCR product formed.

The input is a list of sequences in FASTA or Genbank format. Different formats within the list are accepted.

The last sequence in the list is interpreted as the template sequence, and all preceding
sequences are primer sequences

in the example below, MyTemplate is the template and ForwardPrimer and ReversePrimer are primers.

```
>ForwardPrimer
gctactacacacgtactgactg

>ReversePrimer
tgtggttactgactctatcttg

>MyTemplate
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca
```

A report is generated as detailed below.

```
Template MyTemplate 48 nt linear:
ForwardPrimer anneals forward (--->) at 22
ReversePrimer anneals reverse (<---) at 26
--------------------------------------------------------------------------------

5gctactacacacgtactgactg...caagatagagtcagtaaccaca3
                          ||||||||||||||||||||||
                         3gttctatctcagtcattggtgt5
5gctactacacacgtactgactg3
 ||||||||||||||||||||||
3cgatgatgtgtgcatgactgac...gttctatctcagtcattggtgt5



>48bp_PCR_prod
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca



Taq DNA polymerase
|95°C|95°C               |    |tmf:62.4
|____|_____          72°C|72°C|tmr:59.1
|3min|30s  \ 48.7°C _____|____|45s/kb
|    |      \______/ 0:30|5min|GC 47%
|    |       30s         |    |48bp

Pfu-Sso7d DNA polymerase
|98°C|98°C               |    |tmf:56.7
|____|_____          72°C|72°C|tmr:53.8
|30s |10s  \ 56.8°C _____|____|15s/kb
|    |      \______/ 0:10|5min|GC 47%
|    |       10s         |    |48bp
```

WebPCR should handle circular templates well.
A circular template can be indicated by the Genbank file in the LOCUS line
or by supplying the keyword "circular" in the template fasta header
like this:
```
>ForwardPrimer
gatagagtcagtaacc

>ReversePrimer
cagtcagtacgtgtgt

>MyTemplate circular
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca
```

```
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca
                             ||||||||||||||||
     <acacacgtactgactg       gatagagtcagtaacc>
      ||||||||||||||||
cgatgatgtgtgcatgactgacggaggttctatctcagtcattggtgt
```

### Primer Tm calculator

https://biopython.org/docs/1.75/api/Bio.SeqUtils.MeltingTemp.html


https://github.com/BjornFJohansson/tm


https://www.youtube.com/watch?v=OblPqlOOgew


https://www.youtube.com/watch?v=NufigSvIfA4


https://www.youtube.com/watch?v=mcOwlFVEino
