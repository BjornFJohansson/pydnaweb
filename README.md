# webpcr

is a flask app that contains a PCR simulator and a Tm calculator.
It is built on top of [pydna](https://github.com/BjornFJohansson/pydna).

[![webpcr](static/webpcr.png)](http://bjornfjohansson.pythonanywhere.com/#)

It is available online [here](http://bjornfjohansson.pythonanywhere.com/#).

or here: https://bit.ly/pydnawebpcr

Installed on [pythonanywhere](https://www.pythonanywhere.com) like this:

	mkvirtualenv --python=/usr/bin/python3.9 my-virtualenv
	pip install flask flask-wtf wtforms
	pip install pydna==4.0.0a10
	git clone https://github.com/BjornFJohansson/webpcr.git


![settings](static/settings.png)


![wsgi](static/bjornfjohansson_pythonanywhere_com_wsgi_py.png)