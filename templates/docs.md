# Pydnaweb

Pydnaweb is a flask application that exposes some of the functionality of the [pydna](https://github.com/BjornFJohansson/pydna#readme) Python package as an online service.

Development of Pydna/Pydnaweb is led by [Björn Johansson]() at the Department of Biology, University of Minho.

If you have question not answered below or suggestions, please ask in the [Google group](https://groups.google.com/g/pydna) (preferred)
or create an issue on [GitHub](https://github.com/BjornFJohansson/pydnaweb/issues).

All tools accept sequences in [FASTA or Genbank](https://github.com/MetabolicEngineeringGroupCBMA/MetabolicEngineeringGroupCBMA.github.io/wiki/sequence_formats) format. The formats can be mixed.

### WebPCR simulator

WebPCR simulates PCR given at least two primers and a template sequence as
a list.

The **last** of the sequences in this list is assumed to be the **template**
sequence while all preceding sequences are assumed to be primers.

The example below, shows the template MyTemplate, ForwardPrimer and ReversePrimer.

```
>ForwardPrimer
gctactacacacgtactgactg

>ReversePrimer
tgtggttactgactctatcttg

>MyTemplate
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca
```

A report is generated as detailed below:


```

Template MyTemplate 48 bp linear limit=16:
ForwardPrimer anneals forward (--->) at 22
ReversePrimer anneals reverse (<---) at 26


5gctactacacacgtactgactg...caagatagagtcagtaaccaca3
                          ||||||||||||||||||||||
                         3gttctatctcagtcattggtgt5
5gctactacacacgtactgactg3
 ||||||||||||||||||||||
3cgatgatgtgtgcatgactgac...gttctatctcagtcattggtgt5


Taq DNA polymerase
|95°C|95°C               |    |tmf:62.4
|____|_____          72°C|72°C|tmr:59.1
|3min|30s  \ 48.7°C _____|____|45s/kb
|    |      \______/ 0:30|5min|GC 47%
|    |       30s         |    |48bp
```

WebPCR can handle circular templates. A circular template can be indicated by the Genbank file on the LOCUS line or by supplying the keyword "circular" in the FASTA header like this:


```
>ForwardPrimer
gatagagtcagtaacc

>ReversePrimer
cagtcagtacgtgtgt

>MyTemplate circular
gctactacacacgtactgactgcctccaagatagagtcagtaaccaca
```

As the forward primer anneals after the reverse primer, no PCR product would be
formed on a linear template. On a circular template, the amplification occurs
across the origin of the sequence.

```

Template MyTemplate 48 bp circular limit=16:
ForwardPrimer anneals forward (--->) at 45
ReversePrimer anneals reverse (<---) at 6


5gatagagtcagtaacc...acacacgtactgactg3
                    ||||||||||||||||
                   3tgtgtgcatgactgac5
5gatagagtcagtaacc3
 ||||||||||||||||
3ctatctcagtcattgg...tgtgtgcatgactgac5


Taq DNA polymerase
|95°C|95°C               |    |tmf:48.5
|____|_____          72°C|72°C|tmr:53.7
|3min|30s  \ 43.4°C _____|____|45s/kb
|    |      \______/ 0:30|5min|GC 46%
|    |       30s         |    |41bp


Pfu-Sso7d DNA polymerase
|98°C|98°C               |    |tmf:42.1
|____|_____          72°C|72°C|tmr:48.9
|30s |10s  \ 45.1°C _____|____|15s/kb
|    |      \______/ 0:10|5min|GC 46%
|    |       10s         |    |41bp


>41bp_PCR_prod
gatagagtcagtaaccacagctactacacacgtactgactg



```



### Primer Tm calculator

Calculates the melting temperature for a list of primer sequences using
data and a the [Bio.SeqUtils.MeltingTemp.Tm_NN](https://biopython.org/docs/1.75/api/Bio.SeqUtils.MeltingTemp.html#Bio.SeqUtils.MeltingTemp.Tm_NN) function.

There are many online primer melting calculators available [online](https://www.google.com/search?q=primer+melting+temperature+calculator), but they rarely expose all the details of algorithms and data used.


For details on the decisions for the default values see [here](https://github.com/BjornFJohansson/tm/blob/master/tm.ipynb).


[![](/static/yt.png)](https://www.youtube.com/watch?v=NufigSvIfA4)


### Primer designer

Designs primers for one or more template sequences.
Three sequences are returned for each input sequence, representing the
two primers and the original sequence, followed by a suggested PCR program.

```

>f40 12-mer
GTCCCCGAGGCG
>r40 19-mer
CTTCTACAAAACCGCGTCA
>seq
GTCCCCGAGGCGGACACTGATTGACGCGGTTTTGTAGAAG

Taq DNA polymerase
|95°C|95°C               |    |tmf:59.9
|____|_____          72°C|72°C|tmr:59.8
|3min|30s  \ 49.7°C _____|____|45s/kb
|    |      \______/ 0:30|5min|GC 57%
|    |       30s         |    |40bp

>40bp_PCR_prod
GTCCCCGAGGCGGACACTGATTGACGCGGTTTTGTAGAAG

```


### Matching primer



### Assembly primer designer

### Assembly simulator
