# pydnaweb

is a flask app that make selected pydna functionality available as a web service. Specifically:

- The WebPCR simulator.
- Primer Tm calculator based on The [Bio.SeqUtils.MeltingTemp](https://biopython.org/docs/1.81/api/Bio.SeqUtils.MeltingTemp.html) module.
- Primer designer. Design two flanking primers, given a template sequence.
- Assembly primer designer. Design tailed primers for assembly by HR.
- Assembly simulator. Assemble a series of sequences by shared homology.

pydnaweb is built on top of [pydna](https://github.com/BjornFJohansson/pydna).

[![webpcr](static/webpcr.png)](http://pydna.pythonanywhere.com/#)

Available online [here](http://pydna.pythonanywhere.com/#).

[blogpost](https://ochsavidare.blogspot.com/2013/12/webpcr-pcr-product-simulation.html)

Installed on [pythonanywhere](https://www.pythonanywhere.com) like this:

	mkvirtualenv --python=/usr/bin/python3.9 my-virtualenv
	pip install --upgrade flask flask-wtf wtforms pydna
	git clone https://github.com/BjornFJohansson/pydnaweb.git


![settings](static/settings.png)


![wsgi](static/bjornfjohansson_pythonanywhere_com_wsgi_py.png)